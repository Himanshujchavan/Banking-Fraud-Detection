import asyncio
import os

from APP.database import SessionLocal
from services.mule_detector import detect_multiple_senders
from services.rapid_movement_detector import detect_rapid_movement
from services.dormant_detector import detect_dormant_accounts

SCAN_INTERVAL_SECONDS = int(os.getenv("BACKGROUND_SCAN_INTERVAL_SECONDS", "300"))


async def _run_scans_once():
    db = SessionLocal()
    try:
        await detect_multiple_senders(db)
        await detect_rapid_movement(db)
        await detect_dormant_accounts(db)
    finally:
        db.close()


async def periodic_scan_loop():
    """
    Defense-in-depth alongside the real-time per-transaction risk engine
    in services/risk_engine.py: re-aggregates recent activity on a fixed
    interval to catch patterns that build up gradually across many small
    transfers. Once Kafka is in place, this loop is a natural candidate
    to retire in favor of a streaming windowed consumer — but it costs
    nothing to keep running as a periodic backstop.
    """
    while True:
        try:
            await _run_scans_once()
        except Exception as exc:
            # Never let a bad scan cycle kill the whole app.
            print(f"[background_scans] scan cycle failed: {exc}")
        await asyncio.sleep(SCAN_INTERVAL_SECONDS)
