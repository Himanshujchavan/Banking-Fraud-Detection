from sqlalchemy import text

from APP.model import FraudAlert

from services.alert_service import (
    create_alert
)


async def detect_rapid_movement(db):

    query = text("""
        SELECT DISTINCT
            t1.receiver_account

        FROM transactions t1

        JOIN transactions t2
        ON t1.receiver_account =
           t2.sender_account

        WHERE ABS(
            EXTRACT(
                EPOCH FROM
                (
                    t2.timestamp -
                    t1.timestamp
                )
            )
        ) < 300

        AND ABS(
            t1.amount -
            t2.amount
        ) < 5000
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
            FraudAlert.alert_type == "RAPID_MOVEMENT",
            FraudAlert.status == "OPEN"
        ).first()

        if existing:
            continue

        await create_alert(
            db=db,
            account_number=account,
            alert_type="RAPID_MOVEMENT",
            risk_score=90
        )

        alerts_created += 1

    return alerts_created