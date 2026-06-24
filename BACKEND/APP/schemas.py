from pydantic import BaseModel, EmailStr


# =====================================
# User Registration
# =====================================

class UserRegister(BaseModel):

    username: str

    email: EmailStr

    password: str


# =====================================
# User Login
# =====================================

class UserLogin(BaseModel):

    email: EmailStr

    password: str


# =====================================
# Create Account
# =====================================

class CreateAccount(BaseModel):

    user_id: int


# =====================================
# Money Transfer
# =====================================

class TransferRequest(BaseModel):

    sender_account: str

    receiver_account: str

    amount: float


# =====================================
# Balance Response
# =====================================

class BalanceResponse(BaseModel):

    balance: float


# =====================================
# Fraud Prediction Request
# =====================================

class FraudPredictionRequest(BaseModel):

    amount: float

    avg_transaction_amount: float

    total_transactions: int

    avg_daily_transactions: float

    beneficiary_count: int


# =====================================
# Fraud Prediction Response
# =====================================

class FraudPredictionResponse(BaseModel):

    fraud_probability: float

    risk_score: float

    decision: str


# =====================================
# Alert Review
# =====================================

class AlertReviewRequest(BaseModel):

    analyst_name: str

    remarks: str


# =====================================
# Create Investigation Case
# =====================================

class CreateCaseRequest(BaseModel):

    alert_id: int

    account_number: str

    analyst_name: str

    notes: str


# =====================================
# Investigation Case Response
# =====================================

class CaseResponse(BaseModel):

    id: int

    alert_id: int

    account_number: str

    analyst_name: str

    notes: str

    status: str


# =====================================
# Freeze Account
# =====================================

class FreezeAccountResponse(BaseModel):

    message: str


# =====================================
# Alert Response
# =====================================

class AlertResponse(BaseModel):

    id: int

    account_number: str

    alert_type: str

    risk_score: float

    status: str