import json

from APP.model import OutboxEvent


def publish_event(db, topic: str, key: str, payload: dict) -> OutboxEvent:
    """
    Writes an outbox row in the CALLER's transaction — it does not commit.
    This is what makes the outbox pattern work: the event row and the
    business data (e.g. the transfer + Transaction row) either both commit
    or both roll back together, so an event can never be emitted for a
    transfer that didn't actually happen, and a committed transfer can
    never silently fail to emit its event.

    outbox_publisher_worker.py polls this table and publishes unpublished
    rows. Today it just logs; swap `send_to_kafka()` in that file for a
    real producer.send() call and no other code changes.
    """

    event = OutboxEvent(
        topic=topic,
        key=key,
        payload=json.dumps(payload, default=str),
    )

    db.add(event)

    return event
