from sqlalchemy import text

from APP.model import FraudAlert

from services.alert_service import (
    create_alert
)

# Real-time per-transaction mule checks now live in services/risk_engine.py.
# This scan is a periodic safety net that re-aggregates recent activity —
# it catches patterns that build up gradually across many small transfers,
# which a single-transaction check can miss. Bounded to a recent window
# (backed by the ix_transactions_receiver_time index) so it stays cheap
# as the table grows, instead of scanning full transaction history.

WINDOW_HOURS = 24
SENDER_THRESHOLD = 20


async def detect_multiple_senders(db, window_hours: int = WINDOW_HOURS):

    query = text("""
        SELECT
            receiver_account,
            COUNT(DISTINCT sender_account)
                AS sender_count

        FROM transactions

        WHERE timestamp >= NOW() - (:window_hours || ' hours')::interval

        GROUP BY receiver_account

        HAVING COUNT(
            DISTINCT sender_account
        ) > :sender_threshold
    """)

    results = db.execute(
        query,
        {
            "window_hours": window_hours,
            "sender_threshold": SENDER_THRESHOLD,
        }
    ).fetchall()

    alerts_created = 0

    for row in results:

        account = row.receiver_account

        existing = db.query(
            FraudAlert
        ).filter(
            FraudAlert.account_number == account,
            FraudAlert.alert_type == "MULTIPLE_SENDERS",
            FraudAlert.status == "OPEN"
        ).first()

        if existing:
            continue

        await create_alert(
            db=db,
            account_number=account,
            alert_type="MULTIPLE_SENDERS",
            risk_score=80
        )

        alerts_created += 1

    return alerts_created
