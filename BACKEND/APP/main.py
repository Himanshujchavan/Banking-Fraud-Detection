import asyncio
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from APP.database import Base, engine
from APP.background_scans import periodic_scan_loop
from APP.websocket.alert_socket import redis_listener

from APP.routers import auth
from APP.routers import account
from APP.routers import transaction
from APP.routers import admin
from APP.routers import fraud
from APP.routers import fraud_alerts
from APP.routers import mule
from APP.websocket.alert_socket import router as ws_router


# CORS: read from env instead of hardcoding "*". allow_credentials=True
# combined with allow_origins=["*"] is invalid/unsafe (browsers reject
# wildcard origins on credentialed requests), so this requires an
# explicit, comma-separated allowlist in production.
ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

# Only auto-create tables in dev. In staging/prod, manage schema with a
# real migration tool (e.g. Alembic) — see migrate.py for a stopgap.
AUTO_CREATE_TABLES = os.getenv("AUTO_CREATE_TABLES", "false").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    if AUTO_CREATE_TABLES:
        Base.metadata.create_all(bind=engine)

    scan_task = asyncio.create_task(periodic_scan_loop())
    redis_task = asyncio.create_task(redis_listener())

    yield

    for task in (scan_task, redis_task):
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


app = FastAPI(
    title="Fraud Detection Banking API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ws_router)
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(account.router)
app.include_router(transaction.router)
app.include_router(fraud.router)
app.include_router(fraud_alerts.router)
app.include_router(mule.router)


@app.get("/")
def home():
    return {"message": "API Running"}
