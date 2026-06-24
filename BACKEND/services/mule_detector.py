from sqlalchemy import text

from APP.model import FraudAlert

from services.alert_service import (
    create_alert
)


async def detect_multiple_senders(db):

    query = text("""
        SELECT
            receiver_account,
            COUNT(DISTINCT sender_account)
                AS sender_count

        FROM transactions

        GROUP BY receiver_account

        HAVING COUNT(
            DISTINCT sender_account
        ) > 20
    """)

    results = db.execute(
        query
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