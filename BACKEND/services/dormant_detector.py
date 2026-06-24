from sqlalchemy import text

from APP.model import FraudAlert

from services.alert_service import (
    create_alert
)


async def detect_dormant_accounts(db):

    query = text("""
        SELECT DISTINCT
            a.account_number

        FROM accounts a

        JOIN transactions t
        ON a.account_number =
           t.receiver_account

        WHERE

        a.last_active <
        NOW() - INTERVAL '180 days'

        AND

        t.amount > 40000
    """)

    results = db.execute(
        query
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