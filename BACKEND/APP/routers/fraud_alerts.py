from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from APP.database import SessionLocal
from APP.model import FraudAlert

router = APIRouter(
    prefix="/fraud-alerts",
    tags=["Fraud Alerts"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def get_alerts(
    db: Session = Depends(get_db)
):

    alerts = db.query(
        FraudAlert
    ).order_by(
        FraudAlert.created_at.desc()
    ).all()

    return alerts