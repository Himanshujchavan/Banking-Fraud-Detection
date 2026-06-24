from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Text
)

from datetime import datetime

from APP.database import Base


# ==========================
# Users
# ==========================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=False
    )


# ==========================
# Accounts
# ==========================

class Account(Base):

    __tablename__ = "accounts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    account_number = Column(
        String,
        unique=True,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    balance = Column(
        Float,
        default=10000
    )

    is_frozen = Column(
        Boolean,
        default=False
    )


# ==========================
# Transactions
# ==========================

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(
        Integer,
        primary_key=True
    )

    sender_account = Column(String)

    receiver_account = Column(String)

    amount = Column(Float)

    status = Column(String)

    timestamp = Column(DateTime)

    is_fraud = Column(
        Boolean,
        default=False
    )

    risk_score = Column(
        Float,
        default=0
    )

    transaction_type = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ==========================
# Fraud Alerts
# ==========================

class FraudAlert(Base):

    __tablename__ = "fraud_alerts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    account_number = Column(String)

    alert_type = Column(String)

    risk_score = Column(Float)

    status = Column(
        String,
        default="OPEN"
    )

    assigned_to = Column(String)

    remarks = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ==========================
# Investigation Cases
# ==========================

class InvestigationCase(Base):

    __tablename__ = "investigation_cases"

    id = Column(
        Integer,
        primary_key=True
    )

    alert_id = Column(
        Integer,
        ForeignKey("fraud_alerts.id")
    )

    account_number = Column(String)

    analyst_name = Column(String)

    notes = Column(Text)

    status = Column(
        String,
        default="OPEN"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )