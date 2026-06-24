from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, text

from APP.database import SessionLocal

from APP.model import (
    User,
    Account,
    Transaction,
    FraudAlert,
    InvestigationCase
)

from APP.schemas import (
    CreateCaseRequest,
    AlertReviewRequest
)

from services.mule_detector import (
    detect_multiple_senders
)

from services.rapid_movement_detector import (
    detect_rapid_movement
)

from services.dormant_detector import (
    detect_dormant_accounts
)
router = APIRouter(
    prefix="/admin",
    tags=["Admin Dashboard"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =====================================
# Dashboard Stats
# =====================================

@router.get("/dashboard/stats")
def dashboard_stats(
    db: Session = Depends(get_db)
):

    total_users = db.query(User).count()

    total_accounts = db.query(Account).count()

    total_transactions = db.query(Transaction).count()

    fraud_transactions = db.query(
        Transaction
    ).filter(
        Transaction.is_fraud.is_(True)
    ).count()

    total_alerts = db.query(
        FraudAlert
    ).count()

    open_alerts = db.query(
        FraudAlert
    ).filter(
        FraudAlert.status == "OPEN"
    ).count()

    blocked_transactions = db.query(
        Transaction
    ).filter(
        Transaction.risk_score >= 85
    ).count()
    high_risk_accounts = db.query(
    FraudAlert.account_number
).distinct().count()
    return {
        "total_users": total_users,
        "total_accounts": total_accounts,
        "total_transactions": total_transactions,
        "fraud_transactions": fraud_transactions,
        "total_alerts": total_alerts,
        "open_alerts": open_alerts,
        "blocked_transactions": blocked_transactions,
        "high_risk_accounts": high_risk_accounts
}


# =====================================
# Users
# =====================================

@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(User).all()


# =====================================
# Accounts
# =====================================

@router.get("/accounts")
def get_accounts(
    db: Session = Depends(get_db)
):
    return db.query(Account).all()


# =====================================
# Latest Transactions
# =====================================

@router.get("/transactions")
def get_transactions(
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

@router.get("/transactions/high-risk")
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
# Fraud Alerts
# =====================================

@router.get("/fraud-alerts")
def fraud_alerts(
    db: Session = Depends(get_db)
):

    return db.query(
        FraudAlert
    ).order_by(
        FraudAlert.created_at.desc()
    ).all()


# =====================================
# Open Alerts
# =====================================

@router.get("/fraud-alerts/open")
def open_alerts(
    db: Session = Depends(get_db)
):

    return db.query(
        FraudAlert
    ).filter(
        FraudAlert.status == "OPEN"
    ).all()


# =====================================
# Account Investigation
# =====================================

@router.get("/account/{account_number}")
def account_details(
    account_number: str,
    db: Session = Depends(get_db)
):

    account = db.query(
        Account
    ).filter(
        Account.account_number == account_number
    ).first()

    if not account:
        return {
            "message": "Account not found"
        }

    transactions = db.query(
        Transaction
    ).filter(
        (Transaction.sender_account == account_number)
        |
        (Transaction.receiver_account == account_number)
    ).order_by(
        Transaction.timestamp.desc()
    ).all()

    alerts = db.query(
        FraudAlert
    ).filter(
        FraudAlert.account_number == account_number
    ).all()

    return {
        "account": {
    "id": account.id,
    "user_id": account.user_id,
    "account_number": account.account_number,
    "balance": account.balance,
    "is_frozen": account.is_frozen
},
        "transactions": transactions,
        "alerts": alerts
    }

# =====================================
# Risk Distribution
# =====================================

@router.get("/risk-distribution")
def risk_distribution(
    db: Session = Depends(get_db)
):

    low = db.query(Transaction).filter(
        Transaction.risk_score < 30
    ).count()

    medium = db.query(Transaction).filter(
        Transaction.risk_score.between(30, 60)
    ).count()

    high = db.query(Transaction).filter(
        Transaction.risk_score.between(60, 85)
    ).count()

    critical = db.query(Transaction).filter(
        Transaction.risk_score > 85
    ).count()

    return {
        "low": low,
        "medium": medium,
        "high": high,
        "critical": critical
    }


# =====================================
# Top Suspicious Accounts
# =====================================

@router.get("/top-suspicious")
def top_suspicious_accounts(
    db: Session = Depends(get_db)
):

    result = db.query(
        FraudAlert.account_number,
        func.count(FraudAlert.id).label("alert_count")
    ).group_by(
        FraudAlert.account_number
    ).order_by(
        func.count(FraudAlert.id).desc()
    ).limit(20).all()

    return result


# =====================================
# Network Analysis
# =====================================

@router.get("/network-analysis")
def network_analysis(
    db: Session = Depends(get_db)
):

    transactions = db.query(
        Transaction
    ).limit(50).all()

    nodes = {}
    edges = []

    for txn in transactions:

        sender = txn.sender_account
        receiver = txn.receiver_account

        sender_risk = txn.risk_score or 0
        receiver_risk = txn.risk_score or 0

        if sender not in nodes:

            level = "low"

            if sender_risk >= 80:
                level = "high"

            elif sender_risk >= 50:
                level = "medium"

            nodes[sender] = {
                "id": sender,
                "risk": sender_risk,
                "level": level
            }

        if receiver not in nodes:

            level = "low"

            if receiver_risk >= 80:
                level = "high"

            elif receiver_risk >= 50:
                level = "medium"

            nodes[receiver] = {
                "id": receiver,
                "risk": receiver_risk,
                "level": level
            }

        edges.append({
            "from": sender,
            "to": receiver,
            "amount": txn.amount
        })

    return {
        "nodes": list(nodes.values()),
        "edges": edges
    }


@router.get("/network-analysis/fraud")
def fraud_network(
    db: Session = Depends(get_db)
):

    query = text("""
        SELECT
            sender_account,
            receiver_account,
            amount

        FROM transactions

        WHERE risk_score >= 80

        LIMIT 1000
    """)

    transactions = db.execute(
        query
    ).fetchall()

    nodes = set()
    edges = []

    for txn in transactions:

        nodes.add(txn.sender_account)
        nodes.add(txn.receiver_account)

        edges.append({
            "source": txn.sender_account,
            "target": txn.receiver_account,
            "amount": float(txn.amount)
        })

    return {
        "nodes": [
            {"id": n}
            for n in nodes
        ],
        "edges": edges
    }



@router.patch("/alerts/{alert_id}/false-positive")
def false_positive(
    alert_id:int,
    db:Session=Depends(get_db)
):

    alert = db.query(FraudAlert).filter(
        FraudAlert.id == alert_id
    ).first()

    alert.status = "FALSE_POSITIVE"

    db.commit()

    return {
        "message":"Marked False Positive"
    }

@router.post("/cases/create")
def create_case(
    payload: CreateCaseRequest,
    db: Session = Depends(get_db)
):

    case = InvestigationCase(
        alert_id=payload.alert_id,
        account_number=payload.account_number,
        analyst_name=payload.analyst_name,
        notes=payload.notes,
        status="OPEN"
    )

    db.add(case)

    db.commit()

    return {
        "message":"Case created"
    }

@router.get("/cases")
def get_cases(
    db: Session = Depends(get_db)
):

    return db.query(
        InvestigationCase
    ).all()

@router.post("/freeze/{account_number}")
def freeze_account(
    account_number:str,
    db:Session=Depends(get_db)
):

    account = db.query(Account).filter(
        Account.account_number ==
        account_number
    ).first()

    if not account:

        return {
            "message":"Account not found"
        }

    account.is_frozen = True

    db.commit()

    return {
        "message":"Account frozen"
    }

@router.post("/unfreeze/{account_number}")
def unfreeze_account(
    account_number: str,
    db: Session = Depends(get_db)
):

    account = db.query(
        Account
    ).filter(
        Account.account_number ==
        account_number
    ).first()

    if not account:

        return {
            "message": "Account not found"
        }

    account.is_frozen = False

    db.commit()

    return {
        "message": "Account unfrozen"
    }

@router.post("/scan")
async def scan_for_mules(
    db: Session = Depends(get_db)
):

    alerts = await detect_multiple_senders(
        db
    )

    return {
        "message": "Scan completed",
        "alerts_created": alerts
    }

@router.post("/rapid-movement")
async def rapid_movement_scan(
    db: Session = Depends(get_db)
):

    count = await detect_rapid_movement(
        db
    )

    return {
        "alerts_created": count
    }

@router.patch("/alerts/{alert_id}/review")
def review_alert(
    alert_id: int,
    payload: AlertReviewRequest,
    db: Session = Depends(get_db)
):

    alert = db.query(
        FraudAlert
    ).filter(
        FraudAlert.id == alert_id
    ).first()

    if not alert:

        return {
            "message":
            "Alert not found"
        }

    alert.status = "UNDER_REVIEW"

    alert.assigned_to = (
        payload.analyst_name
    )

    alert.remarks = (
        payload.remarks
    )

    db.commit()

    return {
        "message":
        "Alert Under Review"
    }



@router.patch("/alerts/{alert_id}/resolve")
def resolve_alert(
    alert_id: int,
    db: Session = Depends(get_db)
):

    alert = db.query(
        FraudAlert
    ).filter(
        FraudAlert.id == alert_id
    ).first()

    if not alert:

        return {
            "message":
            "Alert not found"
        }

    alert.status = "RESOLVED"

    db.commit()

    return {
        "message":
        "Alert Resolved"
    }

@router.post("/dormant")
async def dormant_scan(
    db: Session = Depends(get_db)
):

    count = await detect_dormant_accounts(
        db
    )

    return {
        "alerts_created": count
    }

@router.get("/cases/{case_id}")
def get_case(
    case_id: int,
    db: Session = Depends(get_db)
):

    case = db.query(
        InvestigationCase
    ).filter(
        InvestigationCase.id == case_id
    ).first()

    if not case:

        return {
            "message": "Case not found"
        }

    return case