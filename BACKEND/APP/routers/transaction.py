from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from APP.database import SessionLocal

from APP.schemas import (
    TransferRequest,
    BalanceResponse
)

from services.transfer_service import (
    transfer_money
)

from APP.model import (
    Transaction
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =====================================
# Transfer Money
# =====================================

@router.post("/transfer")
def transfer(
    data: TransferRequest,
    db: Session = Depends(get_db)
):

    return transfer_money(
        data.sender_account,
        data.receiver_account,
        data.amount,
        db
    )


# =====================================
# Account Transactions
# =====================================

@router.get("/account/{account_number}")
def get_transactions(
    account_number: str,
    db: Session = Depends(get_db)
):

    return db.query(
        Transaction
    ).filter(

        (
            Transaction.sender_account
            == account_number
        )

        |

        (
            Transaction.receiver_account
            == account_number
        )

    ).order_by(
        Transaction.timestamp.desc()
    ).all()


# =====================================
# Latest Transactions
# =====================================

@router.get("/all")
def all_transactions(
    db: Session = Depends(get_db)
):

    return db.query(
        Transaction
    ).order_by(
        Transaction.id.desc()
    ).limit(100).all()


# =====================================
# High Risk Transactions
# =====================================

@router.get("/high-risk")
def high_risk_transactions(
    db: Session = Depends(get_db)
):

    return db.query(
        Transaction
    ).filter(
        Transaction.risk_score >= 80
    ).order_by(
        Transaction.risk_score.desc()
    ).all()


# =====================================
# Fraud Transactions
# =====================================

@router.get("/fraud")
def fraud_transactions(
    db: Session = Depends(get_db)
):

    return db.query(
        Transaction
    ).filter(
        Transaction.is_fraud == True
    ).order_by(
        Transaction.risk_score.desc()
    ).all()


# =====================================
# Blocked Transactions
# =====================================

@router.get("/blocked")
def blocked_transactions(
    db: Session = Depends(get_db)
):

    return db.query(
        Transaction
    ).filter(
        Transaction.risk_score >= 85
    ).order_by(
        Transaction.risk_score.desc()
    ).all()