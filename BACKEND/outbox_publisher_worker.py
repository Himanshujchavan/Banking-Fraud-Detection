"""
Polls the outbox_events table and publishes each unpublished row.

Run this as its own process, separate from the API:

    python outbox_publisher_worker.py

Today `send_to_kafka()` just logs. When Kafka is actually added, this is
the ONLY function that needs to change — replace its body with a real
aiokafka / confluent-kafka producer.send(topic, key=key, value=payload)
call. Nothing in transfer_service.py, event_publisher.py, or the routers
needs to know about that change.
"""

import time
import signal
import sys
from datetime import datetime

from APP.database import SessionLocal
from APP.model import OutboxEvent

POLL_INTERVAL_SECONDS = 2
BATCH_SIZE = 100

_running = True


def _handle_shutdown(signum, frame):
    global _running
    _running = False


def send_to_kafka(topic: str, key: str, payload: str) -> None:
    # TODO(kafka): replace this with a real producer call, e.g.
    #   producer.send(topic, key=key.encode(), value=payload.encode())
    print(f"[outbox->kafka] topic={topic} key={key} payload={payload}")


def publish_pending(db) -> int:
    events = (
        db.query(OutboxEvent)
        .filter(OutboxEvent.published.is_(False))
        .order_by(OutboxEvent.id)
        .limit(BATCH_SIZE)
        .all()
    )

    for event in events:
        send_to_kafka(event.topic, event.key, event.payload)
        event.published = True
        event.published_at = datetime.utcnow()

    if events:
        db.commit()

    return len(events)


def main():
    signal.signal(signal.SIGINT, _handle_shutdown)
    signal.signal(signal.SIGTERM, _handle_shutdown)

    print("Outbox publisher worker started.")

    while _running:
        db = SessionLocal()
        try:
            count = publish_pending(db)
            if count:
                print(f"Published {count} event(s).")
        except Exception as exc:
            print(f"[outbox_publisher_worker] error: {exc}", file=sys.stderr)
        finally:
            db.close()

        time.sleep(POLL_INTERVAL_SECONDS)

    print("Outbox publisher worker stopped.")


if __name__ == "__main__":
    main()
