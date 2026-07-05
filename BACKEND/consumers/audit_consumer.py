"""
Consumes `transactions.created` and writes an append-only AuditLog row
for each one. Runs as its own process:

    python -m consumers.audit_consumer

Scale this independently of the API: run more replicas in the same
consumer group (AUDIT_CONSUMER_GROUP) and Kafka will split the topic's
partitions across them automatically. A slow or crashed audit consumer
never affects transfer latency or availability — it just falls behind
and catches up from where it left off, because Kafka retains the topic
and tracks this group's committed offset independently of the API.
"""

import asyncio
import json
import os

from datetime import datetime

from aiokafka import AIOKafkaConsumer

from APP.database import SessionLocal
from APP.model import AuditLog

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = "transactions.created"
GROUP_ID = os.getenv("AUDIT_CONSUMER_GROUP", "audit-log-writer")


async def handle_event(payload: dict):
    db = SessionLocal()
    try:
        db.add(AuditLog(
            sender_account=payload.get("sender_account"),
            receiver_account=payload.get("receiver_account"),
            amount=payload.get("amount"),
            risk_score=payload.get("risk_score"),
            event_timestamp=payload.get("timestamp"),
            recorded_at=datetime.utcnow(),
        ))
        db.commit()
    finally:
        db.close()


async def main():
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        # Start from the beginning of the topic the first time this
        # consumer group ever runs; after that Kafka remembers its offset.
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    await consumer.start()
    print(f"[audit_consumer] listening on '{TOPIC}' as group '{GROUP_ID}'")

    try:
        async for message in consumer:
            try:
                payload = json.loads(message.value.decode("utf-8"))
                await handle_event(payload)
            except Exception as exc:
                # Log and move on — one malformed event should never wedge
                # the whole consumer. (For real durability guarantees,
                # route failures to a dead-letter topic instead of just
                # logging.)
                print(f"[audit_consumer] failed to process message: {exc}")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
