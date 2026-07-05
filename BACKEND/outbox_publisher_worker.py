"""
Polls the outbox_events table and publishes each unpublished row to Kafka.

Run this as its own process, separate from the API:

    python outbox_publisher_worker.py

This is intentionally the ONLY place in the whole codebase that imports
a Kafka client. transfer_service.py and alert_service.py only ever write
to the outbox table (via services/event_publisher.py) — they have no idea
Kafka exists. That's what makes it possible to swap Kafka for something
else later, or run this worker as multiple replicas, without touching
any business logic.
"""

import asyncio
import os
import signal

from datetime import datetime

from aiokafka import AIOKafkaProducer

from APP.database import SessionLocal
from APP.model import OutboxEvent

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
POLL_INTERVAL_SECONDS = float(os.getenv("OUTBOX_POLL_INTERVAL_SECONDS", "2"))
BATCH_SIZE = int(os.getenv("OUTBOX_BATCH_SIZE", "100"))

_shutdown = asyncio.Event()


def _handle_shutdown(*_args):
    _shutdown.set()


async def publish_pending(producer: AIOKafkaProducer, db) -> int:
    events = (
        db.query(OutboxEvent)
        .filter(OutboxEvent.published.is_(False))
        .order_by(OutboxEvent.id)
        .limit(BATCH_SIZE)
        .all()
    )

    for event in events:
        # key partitions the topic — using the account number (set when
        # the event was written) keeps every event for one account in
        # order on the same partition.
        await producer.send_and_wait(
            event.topic,
            key=event.key.encode("utf-8"),
            value=event.payload.encode("utf-8"),
        )
        event.published = True
        event.published_at = datetime.utcnow()

    if events:
        db.commit()

    return len(events)


async def main():
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, _handle_shutdown)

    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()
    print(f"Outbox publisher worker started, publishing to {KAFKA_BOOTSTRAP_SERVERS}")

    try:
        while not _shutdown.is_set():
            db = SessionLocal()
            try:
                count = await publish_pending(producer, db)
                if count:
                    print(f"Published {count} event(s) to Kafka.")
            except Exception as exc:
                print(f"[outbox_publisher_worker] error: {exc}")
            finally:
                db.close()

            try:
                await asyncio.wait_for(_shutdown.wait(), timeout=POLL_INTERVAL_SECONDS)
            except asyncio.TimeoutError:
                pass
    finally:
        await producer.stop()
        print("Outbox publisher worker stopped.")


if __name__ == "__main__":
    asyncio.run(main())
