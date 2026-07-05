from sqlalchemy import text

from APP.model import FraudAlert

from services.alert_service import (
    create_alert
)

# Real-time per-transaction rapid-movement checks now live in
# services/risk_engine.py. This scan is a periodic safety net, bounded to
# a recent window so the self-join stays cheap as the table grows instead
# of joining the entire transaction history against itself.

WINDOW_HOURS = 24
RAPID_SECONDS = 300
AMOUNT_TOLERANCE = 5000


async def detect_rapid_movement(
    db,
    window_hours: int = WINDOW_HOURS,
    rapid_seconds: int = RAPID_SECONDS,
    amount_tolerance: float = AMOUNT_TOLERANCE,
):

    query = text("""
        SELECT DISTINCT
            t1.receiver_account

        FROM transactions t1

        JOIN transactions t2
        ON t1.receiver_account =
           t2.sender_account

        WHERE t1.timestamp >= NOW() - (:window_hours || ' hours')::interval
        AND t2.timestamp >= NOW() - (:window_hours || ' hours')::interval

        AND ABS(
            EXTRACT(
                EPOCH FROM
                (
                    t2.timestamp -
                    t1.timestamp
                )
            )
        ) < :rapid_seconds

        AND ABS(
            t1.amount -
            t2.amount
        ) < :amount_tolerance
    """)

    results = db.execute(
        query,
        {
            "window_hours": window_hours,
            "rapid_seconds": rapid_seconds,
            "amount_tolerance": amount_tolerance,
        }
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
            risk_score=80
        )

        alerts_created += 1

    return alerts_created
