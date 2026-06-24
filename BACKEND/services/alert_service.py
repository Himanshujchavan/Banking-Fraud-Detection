from APP.model import FraudAlert
from APP.websocket.alert_socket import manager


async def create_alert(
    db,
    account_number,
    alert_type,
    risk_score
):

    alert = FraudAlert(
        account_number=account_number,
        alert_type=alert_type,
        risk_score=risk_score,
        status="OPEN"
    )

    db.add(alert)

    db.commit()

    db.refresh(alert)

    await manager.broadcast({

        "event": "NEW_ALERT",

        "id": alert.id,

        "account_number":
            alert.account_number,

        "alert_type":
            alert.alert_type,

        "risk_score":
            alert.risk_score,

        "status":
            alert.status,

        "created_at":
            str(alert.created_at)

    })

    return alert