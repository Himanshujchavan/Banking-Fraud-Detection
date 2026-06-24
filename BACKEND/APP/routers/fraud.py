from fastapi import APIRouter
from APP.schemas import FraudPredictionRequest
from APP.ml.predictor import predict_fraud

router = APIRouter(
    prefix="/fraud",
    tags=["Fraud Detection"]
)

@router.post("/predict")
def predict(data: FraudPredictionRequest):

    result = predict_fraud({
        "amount": data.amount,
        "avg_transaction_amount": data.avg_transaction_amount,
        "total_transactions": data.total_transactions,
        "avg_daily_transactions": data.avg_daily_transactions,
        "beneficiary_count": data.beneficiary_count
    })

    return result