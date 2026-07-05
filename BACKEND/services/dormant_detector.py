from sqlalchemy import text

from APP.model import FraudAlert

from services.alert_service import (
    create_alert
)

# Real-time per-transaction dormant-account checks now live in
# services/risk_engine.py, which reads Account.last_active directly.
# This scan is a periodic safety net over recent transactions only —
# bounded by RECENT_TX_DAYS so it doesn't join every historical
# transaction against the accounts table as the data grows.

RECENT_TX_DAYS = 7
DORMANT_INACTIVITY_DAYS = 180
AMOUNT_THRESHOLD = 40000


async def detect_dormant_accounts(
    db,
    recent_tx_days: int = RECENT_TX_DAYS,
    dormant_inactivity_days: int = DORMANT_INACTIVITY_DAYS,
    amount_threshold: float = AMOUNT_THRESHOLD,
):

    query = text("""
        SELECT DISTINCT
            a.account_number

        FROM accounts a

        JOIN transactions t
        ON a.account_number =
           t.receiver_account

        WHERE

        t.timestamp >= NOW() - (:recent_tx_days || ' days')::interval

        AND

        a.last_active <
        NOW() - (:dormant_inactivity_days || ' days')::interval

        AND

        t.amount > :amount_threshold
    """)

    results = db.execute(
        query,
        {
            "recent_tx_days": recent_tx_days,
            "dormant_inactivity_days": dormant_inactivity_days,
            "amount_threshold": amount_threshold,
        }
    ).fetchall()

    alerts_created = 0

    for row in results:

        account = row.account_number

        existing = db.query(
            FraudAlert
        ).filter(
            FraudAlert.account_number == account,
            FraudAlert.alert_type == "DORMANT_ACCOUNT",
            FraudAlert.status == "OPEN"
        ).first()

        if existing:
            continue

        await create_alert(
            db=db,
            account_number=account,
            alert_type="DORMANT_ACCOUNT",
            risk_score=85
        )

        alerts_created += 1

    return alerts_created
