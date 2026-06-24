from APP.model import FraudAlert


def calculate_account_risk(
    account_number,
    db
):

    alerts = db.query(
        FraudAlert
    ).filter(
        FraudAlert.account_number == account_number,
        FraudAlert.status == "OPEN"
    ).all()

    risk = 0

    for alert in alerts:

        if alert.alert_type == "MULTIPLE_SENDERS":
            risk += 30

        elif alert.alert_type == "DORMANT_ACCOUNT":
            risk += 30

        elif alert.alert_type == "RAPID_MOVEMENT":
            risk += 40

    return min(risk, 100)