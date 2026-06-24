import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier


# ==========================
# Load Dataset
# ==========================

df = pd.read_csv("fraud_training.csv")

df["is_fraud"] = df["is_fraud"].astype(int)

print("\nFraud Distribution:")
print(df["is_fraud"].value_counts())


# ==========================
# Features & Target
# ==========================

X = df.drop(
    ["is_fraud", "risk_score"],
    axis=1
)

y = df["is_fraud"]


# ==========================
# Train Test Split
# ==========================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==========================
# Handle Class Imbalance
# ==========================

smote = SMOTE(random_state=42)

X_train, y_train = smote.fit_resample(
    X_train,
    y_train
)

print("\nAfter SMOTE:")
print(pd.Series(y_train).value_counts())


# ==========================
# XGBoost Weight
# ==========================

fraud_count = sum(y == 1)
normal_count = sum(y == 0)

scale_weight = normal_count / fraud_count

print(f"\nScale Weight: {scale_weight}")


# ==========================
# Model
# ==========================

model = XGBClassifier(
    n_estimators=200,
    max_depth=6,
    learning_rate=0.1,
    random_state=42,
    eval_metric="logloss"
)


# ==========================
# Train
# ==========================

model.fit(
    X_train,
    y_train
)


# ==========================
# Predictions
# ==========================

preds = model.predict(X_test)

probs = model.predict_proba(X_test)[:, 1]


# ==========================
# Metrics
# ==========================

accuracy = accuracy_score(
    y_test,
    preds
)

auc = roc_auc_score(
    y_test,
    probs
)

print(f"\nAccuracy: {accuracy*100:.2f}%")

print(f"ROC-AUC Score: {auc:.4f}\n")

print(classification_report(
    y_test,
    preds,
    zero_division=0
))

print("Confusion Matrix:\n")

print(confusion_matrix(
    y_test,
    preds
))


# ==========================
# Save Model
# ==========================

joblib.dump(
    model,
    "fraud_model.pkl"
)

print("\nModel Saved Successfully")