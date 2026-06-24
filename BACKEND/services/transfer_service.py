from fastapi import HTTPException
from datetime import datetime

from APP.model import (
    Account,
    Transaction
)


def transfer_money(
    sender_account_number: str,
    receiver_account_number: str,
    amount: float,
    db
):

    sender = db.query(Account).filter(
        Account.account_number ==
        sender_account_number
    ).first()

    receiver = db.query(Account).filter(
        Account.account_number ==
        receiver_account_number
    ).first()

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
    # Amount Validation
    # -------------------------

    if amount <= 0:

        raise HTTPException(
            status_code=400,
            detail="Invalid amount"
        )

    if sender.balance < amount:

        raise HTTPException(
            status_code=400,
            detail="Insufficient balance"
        )

    # -------------------------
    # Transfer
    # -------------------------

    sender.balance -= amount

    receiver.balance += amount

    # -------------------------
    # Transaction Record
    # -------------------------

    transaction = Transaction(

        sender_account=
        sender_account_number,

        receiver_account=
        receiver_account_number,

        amount=amount,

        status="SUCCESS",

        timestamp=datetime.utcnow(),

        is_fraud=False,

        risk_score=0,

        transaction_type="TRANSFER",

        created_at=datetime.utcnow()
    )

    db.add(transaction)

    db.commit()

    db.refresh(transaction)

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
        receiver.balance
    }