from fastapi import HTTPException
from datetime import datetime

from APP.model import (
    Account,
    Transaction
)

from services.risk_engine import evaluate_transaction_risk
from services.alert_service import create_alert
from services.event_publisher import publish_event

# Transactions scoring at or above BLOCK_THRESHOLD never move money.
BLOCK_THRESHOLD = 85

# Transactions scoring at or above ALERT_THRESHOLD complete, but raise a
# fraud alert for an analyst to review.
ALERT_THRESHOLD = 60


async def transfer_money(
    sender_account_number: str,
    receiver_account_number: str,
    amount: float,
    db
):

    # -------------------------
    # Basic Input Validation
    # -------------------------

    if amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid amount"
        )

    if sender_account_number == receiver_account_number:
        raise HTTPException(
            status_code=400,
            detail="Sender and receiver account must be different"
        )

    # -------------------------
    # Row Locking
    # -------------------------
    #
    # SELECT ... FOR UPDATE locks each account row for the rest of this
    # DB transaction, so a second concurrent transfer touching the same
    # account blocks until this one commits or rolls back — this is what
    # prevents two simultaneous transfers from both reading a stale
    # balance and both passing the "sufficient balance" check below.
    #
    # Both accounts are locked in a fixed order (sorted by account number)
    # regardless of who is sender vs receiver, so that a transfer A->B and
    # a concurrent transfer B->A always acquire locks in the same order
    # and can never deadlock against each other.

    lock_order = sorted([sender_account_number, receiver_account_number])

    locked_accounts = {}

    for account_number in lock_order:
        account = (
            db.query(Account)
            .filter(Account.account_number == account_number)
            .with_for_update()
            .first()
        )
        locked_accounts[account_number] = account

    sender = locked_accounts.get(sender_account_number)
    receiver = locked_accounts.get(receiver_account_number)

    # -------------------------
    # Account Validation
    # -------------------------

    if sender is None:
        raise HTTPException(
            status_code=404,
            detail="Sender account not found"
        )

    if receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver account not found"
        )

    # -------------------------
    # Frozen Account Check
    # -------------------------

    if sender.is_frozen:
        raise HTTPException(
            status_code=403,
            detail="Sender account is frozen"
        )

    if receiver.is_frozen:
        raise HTTPException(
            status_code=403,
            detail="Receiver account is frozen"
        )

    # -------------------------
    # Balance Check
    # -------------------------

    if sender.balance < amount:
        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    # -------------------------
    # Real-Time Risk Evaluation (BEFORE money moves)
    # -------------------------
    #
    # This runs the ML model plus the mule / rapid-movement / dormant
    # rule checks scoped to just these two accounts. It's the same logic
    # a Kafka consumer will eventually run off a `transactions.created`
    # event — for now it just runs inline, synchronously, before commit.

    risk = evaluate_transaction_risk(
        sender_account_number=sender_account_number,
        receiver_account_number=receiver_account_number,
        amount=amount,
        db=db,
    )

    if risk["risk_score"] >= BLOCK_THRESHOLD:

        blocked_transaction = Transaction(
            sender_account=sender_account_number,
            receiver_account=receiver_account_number,
            amount=amount,
            status="BLOCKED",
            timestamp=datetime.utcnow(),
            is_fraud=True,
            risk_score=risk["risk_score"],
            transaction_type="TRANSFER",
            created_at=datetime.utcnow()
        )

        db.add(blocked_transaction)
        db.commit()
        db.refresh(blocked_transaction)

        for alert_type in (risk["triggered_rules"] or ["ML_RISK_SCORE"]):
            await create_alert(
                db=db,
                account_number=receiver_account_number,
                alert_type=alert_type,
                risk_score=risk["risk_score"],
            )

        raise HTTPException(
            status_code=403,
            detail=(
                f"Transaction blocked by fraud engine "
                f"(risk_score={risk['risk_score']})"
            )
        )

    # -------------------------
    # Transfer
    # -------------------------

    now = datetime.utcnow()

    sender.balance -= amount
    receiver.balance += amount
    sender.last_active = now
    receiver.last_active = now

    # -------------------------
    # Transaction Record
    # -------------------------

    transaction = Transaction(
        sender_account=sender_account_number,
        receiver_account=receiver_account_number,
        amount=amount,
        status="SUCCESS",
        timestamp=now,
        is_fraud=risk["risk_score"] >= ALERT_THRESHOLD,
        risk_score=risk["risk_score"],
        transaction_type="TRANSFER",
        created_at=now
    )

    db.add(transaction)

    # -------------------------
    # Outbox Event (future Kafka `transactions.created`)
    # -------------------------
    #
    # Written in the SAME commit as the balance updates and transaction
    # row below, so the event can never be emitted without the transfer
    # having actually happened, or vice versa.

    publish_event(
        db=db,
        topic="transactions.created",
        key=sender_account_number,
        payload={
            "sender_account": sender_account_number,
            "receiver_account": receiver_account_number,
            "amount": amount,
            "risk_score": risk["risk_score"],
            "timestamp": now.isoformat(),
        },
    )

    db.commit()
    db.refresh(transaction)

    if risk["risk_score"] >= ALERT_THRESHOLD:
        for alert_type in (risk["triggered_rules"] or ["ML_RISK_SCORE"]):
            await create_alert(
                db=db,
                account_number=receiver_account_number,
                alert_type=alert_type,
                risk_score=risk["risk_score"],
            )

    return {

        "message":
        "Transfer Successful",

        "transaction_id":
        transaction.id,

        "amount":
        amount,

        "from":
        sender_account_number,

        "to":
        receiver_account_number,

        "sender_balance":
        sender.balance,

        "receiver_balance":
        receiver.balance,

        "risk_score":
        risk["risk_score"]
    }
