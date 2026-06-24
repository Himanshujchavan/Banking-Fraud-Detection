import random

from APP.database import SessionLocal
from APP.model import Account, Transaction

db = SessionLocal()

accounts = db.query(Account).all()

TOTAL_TRANSACTIONS = 200000

for i in range(TOTAL_TRANSACTIONS):

    sender = random.choice(accounts)
    receiver = random.choice(accounts)

    while sender.id == receiver.id:
        receiver = random.choice(accounts)

    amount = random.randint(
        100,
        50000
    )

    transaction = Transaction(
        sender_account=sender.account_number,
        receiver_account=receiver.account_number,
        amount=amount,
        status="SUCCESS"
    )

    db.add(transaction)

    if i % 1000 == 0:
        db.commit()
        print(f"{i} transactions inserted")

db.commit()
db.close()

print("200000 Transactions Created Successfully")