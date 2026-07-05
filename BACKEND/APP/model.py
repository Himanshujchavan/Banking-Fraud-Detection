from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    DateTime,
    Text,
    Index
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
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        index=True
    )

    balance = Column(
        Float,
        default=10000
    )

    is_frozen = Column(
        Boolean,
        default=False
    )

    # Updated every time this account sends or receives a transfer.
    # Used by the dormant-account risk check and by the periodic
    # dormant-account scan.
    last_active = Column(
        DateTime,
        default=datetime.utcnow
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

    sender_account = Column(String, index=True)

    receiver_account = Column(String, index=True)

    amount = Column(Float)

    status = Column(String, index=True)

    timestamp = Column(DateTime, index=True)

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
        default=datetime.utcnow,
        index=True
    )

    __table_args__ = (
        # Speeds up the mule / rapid-movement risk checks, which always
        # filter by receiver_account (or sender_account) plus a time window.
        Index("ix_transactions_receiver_time", "receiver_account", "timestamp"),
        Index("ix_transactions_sender_time", "sender_account", "timestamp"),
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

    account_number = Column(String, index=True)

    alert_type = Column(String)

    risk_score = Column(Float)

    status = Column(
        String,
        default="OPEN",
        index=True
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


# ==========================
# Outbox Events
# ==========================
#
# Transactional outbox: any code path that needs to emit an event
# (today: fraud/transfer events) writes a row here in the SAME db
# transaction as the business data. A separate publisher process
# (see outbox_publisher_worker.py) polls this table and publishes to
# Kafka. This guarantees the event is emitted if and only if the
# business transaction actually committed, without a distributed
# transaction across Postgres and Kafka.

class OutboxEvent(Base):

    __tablename__ = "outbox_events"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Future Kafka topic name, e.g. "transactions.created", "fraud.alerts"
    topic = Column(String, nullable=False, index=True)

    # Future Kafka partition key, e.g. an account number, so events for
    # the same account stay ordered once this is a real topic.
    key = Column(String, nullable=False)

    # JSON-encoded event body.
    payload = Column(Text, nullable=False)

    published = Column(Boolean, default=False, index=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )

    published_at = Column(DateTime, nullable=True)
