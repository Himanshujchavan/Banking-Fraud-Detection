import random
from datetime import datetime, timedelta

from APP.database import SessionLocal
from APP.model import User
from sqlalchemy import text

db = SessionLocal()

locations = [
    ("Mumbai", "India", 19.0760, 72.8777),
    ("Pune", "India", 18.5204, 73.8567),
    ("Nagpur", "India", 21.1458, 79.0882),
    ("Delhi", "India", 28.6139, 77.2090),
    ("Bangalore", "India", 12.9716, 77.5946),
    ("Hyderabad", "India", 17.3850, 78.4867),
    ("Chennai", "India", 13.0827, 80.2707),
    ("Kolkata", "India", 22.5726, 88.3639)
]

users = db.query(User).all()

total_rows = 0

for user in users:

    # 5-10 login records per user
    num_logins = random.randint(5, 10)

    # User's preferred city
    preferred = random.choice(locations)

    for _ in range(num_logins):

        # 80% from preferred city
        if random.random() < 0.8:
            city, country, lat, lon = preferred
        else:
            city, country, lat, lon = random.choice(locations)

        login_time = datetime.now() - timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        db.execute(
            text("""
            INSERT INTO login_locations
            (
                user_id,
                city,
                country,
                latitude,
                longitude,
                login_time
            )
            VALUES
            (
                :user_id,
                :city,
                :country,
                :lat,
                :lon,
                :login_time
            )
            """),
            {
                "user_id": user.id,
                "city": city,
                "country": country,
                "lat": lat,
                "lon": lon,
                "login_time": login_time
            }
        )

        total_rows += 1

db.commit()

print(f"{total_rows} login locations inserted")