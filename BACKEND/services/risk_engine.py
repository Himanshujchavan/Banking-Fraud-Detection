from datetime import datetime, timedelta

from sqlalchemy import func

from APP.model import Account, Transaction
from APP.ml.predictor import predict_fraud

# ---- Tunables ----

SENDER_FEATURE_WINDOW_DAYS = 90

RAPID_WINDOW_SECONDS = 300
RAPID_AMOUNT_TOLERANCE = 5000

MULE_SENDER_THRESHOLD = 20
MULE_WINDOW_HOURS = 24

DORMANT_INACTIVITY_DAYS = 180
DORMANT_AMOUNT_THRESHOLD = 40000

RULE_RISK_SCORES = {
    "RAPID_MOVEMENT": 80,
    "MULTIPLE_SENDERS": 80,
    "DORMANT_ACCOUNT": 85,
}


def _sender_features(sender_account_number, db):
    """
    Builds the same feature shape APP/routers/fraud.py already exposes via
    /fraud/predict, but computed from this account's own history instead of
    being supplied by the caller. Scoped to one account + a bounded window,
    so this is an indexed lookup, not a table scan.
    """

    window_start = datetime.utcnow() - timedelta(days=SENDER_FEATURE_WINDOW_DAYS)

    total_transactions, avg_amount, beneficiary_count = (
        db.query(
            func.count(Transaction.id),
            func.avg(Transaction.amount),
            func.count(func.distinct(Transaction.receiver_account)),
        )
        .filter(
            Transaction.sender_account == sender_account_number,
            Transaction.created_at >= window_start,
        )
        .first()
    )

    total_transactions = total_transactions or 0
    avg_amount = float(avg_amount) if avg_amount else 0.0
    beneficiary_count = beneficiary_count or 0

    avg_daily_transactions = total_transactions / SENDER_FEATURE_WINDOW_DAYS

    return {
        "avg_transaction_amount": avg_amount,
        "total_transactions": total_transactions,
        "avg_daily_transactions": avg_daily_transactions,
        "beneficiary_count": beneficiary_count,
    }


def _check_rapid_movement(sender_account_number, amount, db):
    """
    Did this account receive a similar amount within the last few minutes,
    and is it now immediately forwarding it? Scoped to one account + a
    5-minute window instead of rapid_movement_detector's full-table self join.
    """

    window_start = datetime.utcnow() - timedelta(seconds=RAPID_WINDOW_SECONDS)

    match = (
        db.query(Transaction.id)
        .filter(
            Transaction.receiver_account == sender_account_number,
            Transaction.timestamp >= window_start,
            func.abs(Transaction.amount - amount) < RAPID_AMOUNT_TOLERANCE,
        )
        .first()
    )

    return match is not None


def _check_mule_pattern(receiver_account_number, db):
    """
    Is this receiver suddenly collecting funds from many distinct senders
    in a short window? Scoped to one account + 24h instead of a
    GROUP BY over the whole transactions table.
    """

    window_start = datetime.utcnow() - timedelta(hours=MULE_WINDOW_HOURS)

    sender_count = (
        db.query(func.count(func.distinct(Transaction.sender_account)))
        .filter(
            Transaction.receiver_account == receiver_account_number,
            Transaction.timestamp >= window_start,
        )
        .scalar()
    )

    return (sender_count or 0) >= MULE_SENDER_THRESHOLD


def _check_dormant_reactivation(receiver_account_number, amount, db):
    """
    Is a long-dormant account suddenly receiving a large amount?
    """

    account = (
        db.query(Account)
        .filter(Account.account_number == receiver_account_number)
        .first()
    )

    if not account or not account.last_active:
        return False

    inactive_for = datetime.utcnow() - account.last_active

    return (
        inactive_for > timedelta(days=DORMANT_INACTIVITY_DAYS)
        and amount > DORMANT_AMOUNT_THRESHOLD
    )


def evaluate_transaction_risk(sender_account_number, receiver_account_number, amount, db):
    """
    Scores a single transaction in real time, combining the trained fraud
    model with the same rule families as the mule / rapid-movement /
    dormant detectors, but scoped to the two accounts involved instead of
    scanning the whole table.

    This is deliberately a plain function of (accounts, amount, db) with no
    dependency on FastAPI or the request/response cycle. Today it's called
    inline from transfer_service.transfer_money(); once Kafka is in place,
    a consumer reading `transactions.created` events can call this exact
    function with a fresh db session and nothing here needs to change.

    Returns:
        {
            "risk_score": float 0-100,
            "ml_probability": float 0-1,
            "decision": one of APPROVE / OTP_VERIFICATION / FACE_VERIFICATION / BLOCK_TRANSACTION,
            "triggered_rules": list[str],
        }
    """

    features = _sender_features(sender_account_number, db)
    features["amount"] = amount

    ml_result = predict_fraud(features)
    risk_score = ml_result["risk_score"]

    triggered_rules = []

    if _check_rapid_movement(sender_account_number, amount, db):
        triggered_rules.append("RAPID_MOVEMENT")
        risk_score = max(risk_score, RULE_RISK_SCORES["RAPID_MOVEMENT"])

    if _check_mule_pattern(receiver_account_number, db):
        triggered_rules.append("MULTIPLE_SENDERS")
        risk_score = max(risk_score, RULE_RISK_SCORES["MULTIPLE_SENDERS"])

    if _check_dormant_reactivation(receiver_account_number, amount, db):
        triggered_rules.append("DORMANT_ACCOUNT")
        risk_score = max(risk_score, RULE_RISK_SCORES["DORMANT_ACCOUNT"])

    return {
        "risk_score": round(risk_score, 2),
        "ml_probability": ml_result["fraud_probability"],
        "decision": ml_result["decision"],
        "triggered_rules": triggered_rules,
    }
