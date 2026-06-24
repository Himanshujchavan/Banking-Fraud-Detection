import pandas as pd
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )
)

from APP.database import SessionLocal
from sqlalchemy import text

db = SessionLocal()

query = """
SELECT

    t.amount,

    t.risk_score,

    t.is_fraud,

    up.avg_transaction_amount,

    up.total_transactions,

    up.avg_daily_transactions,

    up.beneficiary_count

FROM transactions t

JOIN accounts a
ON t.sender_account = a.account_number

JOIN user_profiles up
ON a.user_id = up.user_id
"""

df = pd.read_sql(
    text(query),
    db.bind
)

print(df.head())

df.to_csv(
    "fraud_training.csv",
    index=False
)

print("Dataset Created Successfully")
print("Rows:", len(df))