from APP.model import FraudAlert
from APP.websocket.alert_socket import manager
from services.event_publisher import publish_event


async def create_alert(
    db,
    account_number,
    alert_type,
    risk_score
):
    """
    Two independent delivery paths, on purpose:

    1. Outbox -> Kafka `fraud.alerts` topic: durable, replayable, and for
       consumers that don't care about live UI updates at all — the audit
       log and automated case-creation consumers subscribe here.
    2. manager.broadcast() -> Redis pub/sub -> every API replica's own
       WebSocket clients: low-latency live delivery to whoever has the
       dashboard open right now. Not durable — a client that wasn't
       connected at the time simply doesn't get it, which is fine, since
       the alert is already safely persisted and in Kafka regardless.
    """

    alert = FraudAlert(
        account_number=account_number,
        alert_type=alert_type,
        risk_score=risk_score,
        status="OPEN"
    )

    db.add(alert)
    db.flush()  # populates alert.id without ending the transaction

    publish_event(
        db=db,
        topic="fraud.alerts",
        key=account_number,
        payload={
            "alert_id": alert.id,
            "account_number": alert.account_number,
            "alert_type": alert.alert_type,
            "risk_score": alert.risk_score,
            "status": alert.status,
        },
    )

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
