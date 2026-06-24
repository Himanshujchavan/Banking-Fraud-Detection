from fastapi import FastAPI

from APP.routers import auth
from APP.routers import account
from APP.routers import transaction
from APP.routers import admin
from APP.routers import fraud
from APP.routers import fraud_alerts
from APP.routers import mule
from APP.routers import admin
from fastapi.middleware.cors import CORSMiddleware
from APP.websocket.alert_socket import router as ws_router
app = FastAPI(
    title="Fraud Detection Banking API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
app.include_router(
    fraud_alerts.router
)
app.include_router(
    mule.router
)
app.include_router(admin.router)
@app.get("/")
def home():
    return {"message": "API Running"}