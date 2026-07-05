"""
Consumes `fraud.alerts` and automatically opens an InvestigationCase for
anything at or above CASE_AUTO_CREATE_THRESHOLD, so an analyst has a case
queued up the moment a high-risk alert fires instead of waiting for
someone to notice it on a dashboard. Runs as its own process:

    python -m consumers.case_automation_consumer

This is a second, independent consumer group on the same topic as
consumers/audit_consumer's sibling for alerts — Kafka lets any number of
independent consumer groups read the same topic at their own pace, which
is exactly what lets you keep adding downstream behavior (this case
automation, a SIEM export, a customer-notification service, ...) without
ever touching alert_service.py again.
"""

import asyncio
import json
import os

from aiokafka import AIOKafkaConsumer

from APP.database import SessionLocal
from APP.model import InvestigationCase

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = "fraud.alerts"
GROUP_ID = os.getenv("CASE_AUTOMATION_CONSUMER_GROUP", "case-automation")

CASE_AUTO_CREATE_THRESHOLD = float(os.getenv("CASE_AUTO_CREATE_THRESHOLD", "85"))


async def handle_event(payload: dict):
    risk_score = payload.get("risk_score") or 0

    if risk_score < CASE_AUTO_CREATE_THRESHOLD:
        return

    db = SessionLocal()
    try:
        existing = (
            db.query(InvestigationCase)
            .filter(InvestigationCase.alert_id == payload.get("alert_id"))
            .first()
        )
        if existing:
            return

        db.add(InvestigationCase(
            alert_id=payload.get("alert_id"),
            account_number=payload.get("account_number"),
            analyst_name="AUTOMATED_SYSTEM",
            notes=(
                f"Auto-opened: {payload.get('alert_type')} alert scored "
                f"{risk_score} (threshold {CASE_AUTO_CREATE_THRESHOLD})."
            ),
            status="OPEN",
        ))
        db.commit()
        print(f"[case_automation_consumer] opened case for alert {payload.get('alert_id')}")
    finally:
        db.close()


async def main():
    consumer = AIOKafkaConsumer(
        TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )

    await consumer.start()
    print(f"[case_automation_consumer] listening on '{TOPIC}' as group '{GROUP_ID}'")

    try:
        async for message in consumer:
            try:
                payload = json.loads(message.value.decode("utf-8"))
                await handle_event(payload)
            except Exception as exc:
                print(f"[case_automation_consumer] failed to process message: {exc}")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
