import random
import uuid

from APP.database import SessionLocal
from APP.model import User
from sqlalchemy import text

db = SessionLocal()

browsers = [
    "Chrome",
    "Firefox",
    "Edge",
    "Safari"
]

operating_systems = [
    "Windows",
    "Android",
    "iOS",
    "Linux",
    "MacOS"
]

users = db.query(User).all()

device_count = 0

for user in users:

    num_devices = random.randint(1, 3)

    for _ in range(num_devices):

        device_id = str(uuid.uuid4())

        browser = random.choice(browsers)

        os_name = random.choice(operating_systems)

        ip_address = ".".join(
            str(random.randint(1, 255))
            for _ in range(4)
        )

        db.execute(
            text("""
            INSERT INTO devices
            (
                user_id,
                device_id,
                browser,
                os,
                ip_address
            )
            VALUES
            (
                :user_id,
                :device_id,
                :browser,
                :os,
                :ip
            )
            """),
            {
                "user_id": user.id,
                "device_id": device_id,
                "browser": browser,
                "os": os_name,
                "ip": ip_address
            }
        )

        device_count += 1

db.commit()

print(f"{device_count} devices inserted")