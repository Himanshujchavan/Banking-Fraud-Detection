import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from APP.database import SessionLocal
from APP.model import Account
from APP.schemas import CreateAccount

router = APIRouter(tags=["Accounts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/account/create")
def create_account(
    data: CreateAccount,
    db: Session = Depends(get_db)
):

    existing_account = db.query(Account).filter(
        Account.user_id == data.user_id
    ).first()

    if existing_account:
        raise HTTPException(
            status_code=400,
            detail="Account already exists"
        )

    account = Account(
        account_number=str(uuid.uuid4())[:10],
        user_id=data.user_id,
        balance=10000
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return {
        "message": "Account created successfully",
        "account_number": account.account_number,
        "balance": account.balance
    }


@router.get("/account/balance/{account_number}")
def get_balance(
    account_number: str,
    db: Session = Depends(get_db)
):

    account = db.query(Account).filter(
        Account.account_number == account_number
    ).first()

    if not account:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return {
        "account_number": account.account_number,
        "balance": account.balance
    }