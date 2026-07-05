from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from APP.model import FraudAlert
from APP.database import SessionLocal
from services.mule_detector import detect_multiple_senders
from services.rapid_movement_detector import (
    detect_rapid_movement
)
from services.dormant_detector import (
    detect_dormant_accounts
)
from services.mule_risk_service import (
    calculate_account_risk
)





router = APIRouter(
    prefix="/mule",
    tags=["Mule Detection"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/scan")

async def scan_for_mules(
    db: Session = Depends(get_db)
):

    alerts = await detect_multiple_senders(db)

    return {
        "message": "Scan completed",
        "alerts_created": alerts
    }

@router.post("/rapid-movement")
async def rapid_movement_scan(
    db: Session = Depends(get_db)
):

    count = await detect_rapid_movement(db)

    return {
        "alerts_created": count
    }

@router.post("/dormant")
async def dormant_scan(
    db: Session = Depends(get_db)
):

    count = await detect_dormant_accounts(db)

    return {
        "alerts_created": count
    }

@router.get("/risk/{account_number}")
def mule_risk(
    account_number: str,
    db: Session = Depends(get_db)
):

    risk = calculate_account_risk(
        account_number,
        db
    )

    decision = "APPROVE"

    if risk >= 85:
        decision = "BLOCK"

    elif risk >= 60:
        decision = "FACE_VERIFY"

    elif risk >= 30:
        decision = "OTP_VERIFY"

    return {
        "account_number": account_number,
        "risk_score": risk,
        "decision": decision
    }

@router.get("/top-risk")
def top_risk_accounts(
    db: Session = Depends(get_db)
):

    accounts = db.query(
        FraudAlert.account_number
    ).distinct().all()

    results = []

    for account in accounts:

        account_number = account[0]

        risk = calculate_account_risk(
            account_number,
            db
        )

        results.append({
            "account_number": account_number,
            "risk_score": risk
        })

    results.sort(
        key=lambda x: x["risk_score"],
        reverse=True
    )

    return results[:50]