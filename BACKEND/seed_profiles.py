from sqlalchemy import text
from APP.database import SessionLocal

db = SessionLocal()

# Clear existing profiles
db.execute(text("TRUNCATE TABLE user_profiles"))

# Insert all profiles in one query
db.execute(text("""
INSERT INTO user_profiles
(
    user_id,
    avg_transaction_amount,
    total_transactions,
    avg_daily_transactions,
    beneficiary_count,
    preferred_city,
    active_hour_start,
    active_hour_end
)

SELECT
    a.user_id,

    COALESCE(AVG(t.amount), 0) AS avg_transaction_amount,

    COUNT(t.id) AS total_transactions,

    ROUND(COUNT(t.id) / 30.0, 2) AS avg_daily_transactions,

    COUNT(DISTINCT t.receiver_account) AS beneficiary_count,

    COALESCE(
        (
            SELECT ll.city
            FROM login_locations ll
            WHERE ll.user_id = a.user_id
            GROUP BY ll.city
            ORDER BY COUNT(*) DESC
            LIMIT 1
        ),
        'Unknown'
    ) AS preferred_city,

    8 AS active_hour_start,

    22 AS active_hour_end

FROM accounts a
LEFT JOIN transactions t
ON a.account_number = t.sender_account

GROUP BY a.user_id

"""))

db.commit()

print("User Profiles Created Successfully")

count = db.execute(
    text("SELECT COUNT(*) FROM user_profiles")
).scalar()

print(f"Profiles Created: {count}")

db.close()