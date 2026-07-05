"""
This project has no Alembic set up, so there's no clean way to evolve an
existing database's schema. This script is a stopgap: it applies the
schema changes that came with this update using idempotent, IF NOT EXISTS
statements, so it's safe to re-run.

For anything beyond this one-time catch-up, set up Alembic
(`alembic init migrations`) so future schema changes are tracked properly
instead of hand-written here.

Usage:
    python migrate.py
"""

from sqlalchemy import text

from APP.database import engine, Base
import APP.model  # noqa: F401  (ensures all models are registered on Base)


STATEMENTS = [
    # Account.last_active (used by the dormant-account risk check)
    """
    ALTER TABLE accounts
    ADD COLUMN IF NOT EXISTS last_active TIMESTAMP DEFAULT NOW()
    """,

    # Indexes used by the real-time risk engine and the periodic scans
    "CREATE INDEX IF NOT EXISTS ix_accounts_account_number ON accounts (account_number)",
    "CREATE INDEX IF NOT EXISTS ix_accounts_user_id ON accounts (user_id)",
    "CREATE INDEX IF NOT EXISTS ix_transactions_sender_account ON transactions (sender_account)",
    "CREATE INDEX IF NOT EXISTS ix_transactions_receiver_account ON transactions (receiver_account)",
    "CREATE INDEX IF NOT EXISTS ix_transactions_status ON transactions (status)",
    "CREATE INDEX IF NOT EXISTS ix_transactions_timestamp ON transactions (timestamp)",
    "CREATE INDEX IF NOT EXISTS ix_transactions_created_at ON transactions (created_at)",
    "CREATE INDEX IF NOT EXISTS ix_transactions_receiver_time ON transactions (receiver_account, timestamp)",
    "CREATE INDEX IF NOT EXISTS ix_transactions_sender_time ON transactions (sender_account, timestamp)",
    "CREATE INDEX IF NOT EXISTS ix_fraud_alerts_account_number ON fraud_alerts (account_number)",
    "CREATE INDEX IF NOT EXISTS ix_fraud_alerts_status ON fraud_alerts (status)",
]


def run():
    with engine.begin() as conn:
        for statement in STATEMENTS:
            conn.execute(text(statement))
    print("Applied column/index migrations.")

    # outbox_events / audit_log are brand new tables — safe to create via
    # metadata directly rather than hand-writing their DDL.
    Base.metadata.tables["outbox_events"].create(bind=engine, checkfirst=True)
    Base.metadata.tables["audit_log"].create(bind=engine, checkfirst=True)
    print("Ensured outbox_events and audit_log tables exist.")


if __name__ == "__main__":
    run()
