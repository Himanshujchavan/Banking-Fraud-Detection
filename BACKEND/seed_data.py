import random
from APP.database import SessionLocal
from APP.model import User, Account

db = SessionLocal()

# Start after user_380 and generate the next 5,000 records
START_INDEX = 381
TOTAL_NEW_USERS = 5000
END_INDEX = START_INDEX + TOTAL_NEW_USERS

for i in range(START_INDEX, END_INDEX):
    try:
        # 1. Create and add user
        user = User(
            username=f"user_{i}",
            email=f"user_{i}@fraudbank.com",
            password="hashed_password"
        )
        db.add(user)
        db.flush()  # Populates user.id for the account relationship

        # 2. Create and add account
        account = Account(
            account_number=f"ACC{i+100000}",
            user_id=user.id,
            balance=random.randint(5000, 100000)
        )
        db.add(account)

        # 3. Batch commit every 50 records for speed
        if i % 50 == 0:
            db.commit()
            print(f"Progress: Reached user_{i}")

    except Exception as e:
        db.rollback()
        print(f"Skipped user_{i}: {e}")

# Final commit for remaining records
try:
    db.commit()
except Exception as e:
    db.rollback()
    print(f"Final commit failed: {e}")

db.close()
print(f"Successfully added 5,000 users from user_{START_INDEX} to user_{END_INDEX - 1}")
