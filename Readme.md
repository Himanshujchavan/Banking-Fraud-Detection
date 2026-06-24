# 🚨 AI-Powered Banking Fraud Detection & Mule Account Monitoring System

## Overview

An enterprise-grade fraud detection platform designed to identify suspicious banking transactions, detect mule accounts, monitor money movement networks, and assist fraud analysts with investigation workflows.

The system combines Machine Learning, Rule-Based Detection, Real-Time Alerts, Network Analysis, and Case Management to help financial institutions proactively prevent fraud.

---

## Key Features

### 🤖 AI Fraud Detection Engine

* XGBoost-based fraud prediction model
* Risk score generation (0–100)
* Fraud probability prediction
* Transaction classification
* Real-time fraud evaluation

### 🏦 Banking Operations

* User Registration & Authentication
* Account Creation
* Balance Management
* Money Transfer Service
* Transaction History

### 🚨 Fraud Alert System

Automatically generates alerts for:

* Rapid Money Movement
* Multiple Sender Activity
* Dormant Account Reactivation
* High-Risk ML Transactions

### 🔔 Real-Time Notifications

* WebSocket-powered alert broadcasting
* Live dashboard updates
* Instant analyst notifications

### 🕵️ Investigation Workflow

* Alert Review
* Alert Resolution
* False Positive Handling
* Analyst Assignment
* Investigation Notes

### 📁 Case Management

* Create Investigation Cases
* Assign Fraud Analysts
* Track Case Status
* Store Investigation Notes

### ❄️ Account Freeze System

* Freeze Suspicious Accounts
* Unfreeze Cleared Accounts
* Prevent Transfers from Frozen Accounts

### 🌐 Network Analysis

Visual money-flow network displaying:

* Sender → Receiver relationships
* High-risk account clusters
* Suspicious transaction paths
* Mule account patterns

### 📊 Admin Dashboard

Real-time statistics:

* Total Users
* Total Accounts
* Total Transactions
* Fraud Transactions
* Open Alerts
* High-Risk Accounts
* Investigation Cases

---

# System Architecture

Transaction Request
↓
Transfer Service
↓
Fraud Detection Model (XGBoost)
↓
Risk Score Generation
↓
Decision Engine
↓
Transaction Storage
↓
Alert Generation
↓
WebSocket Broadcast
↓
Admin Dashboard
↓
Investigation Workflow
↓
Freeze / Unfreeze Actions

---

# Machine Learning Model

## Algorithm

* XGBoost Classifier

## Features Used

* Transaction Amount
* Average Transaction Amount
* Total Transactions
* Average Daily Transactions
* Beneficiary Count

## Performance

* Accuracy: 99.10%
* ROC-AUC Score: 0.9802
* Precision: 1.00
* Recall: 0.96
* F1 Score: 0.98

---

# Mule Account Detection Modules

## 1. Multiple Sender Detection

Flags accounts receiving money from an unusually high number of distinct senders.

## 2. Rapid Movement Detection

Detects money entering and leaving an account within a short time window.

## 3. Dormant Account Detection

Identifies dormant accounts that suddenly receive large transactions.

---

# Technology Stack

## Frontend

* React.js
* React Flow
* Recharts
* Axios

## Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* WebSockets

## Machine Learning

* XGBoost
* Scikit-Learn
* Pandas
* NumPy
* Imbalanced-Learn (SMOTE)

## Deployment

* Vercel (Frontend)
* Railway / Render (Backend)
* PostgreSQL / Neon DB

---

# Database Schema

## Users

* id
* username
* email
* password

## Accounts

* id
* account_number
* user_id
* balance
* is_frozen

## Transactions

* id
* sender_account
* receiver_account
* amount
* status
* timestamp
* risk_score
* is_fraud

## Fraud Alerts

* id
* account_number
* alert_type
* risk_score
* status
* assigned_to
* remarks
* created_at

## Investigation Cases

* id
* alert_id
* account_number
* analyst_name
* notes
* status
* created_at

---

# API Modules

## Authentication

POST /register

POST /login

## Banking

POST /transactions/transfer

GET /transactions/account/{account_number}

GET /transactions/all

## Fraud Detection

POST /predict

## Admin Dashboard

GET /admin/dashboard/stats

GET /admin/fraud-alerts

GET /admin/users

GET /admin/accounts

## Alert Workflow

PATCH /admin/alerts/{id}/review

PATCH /admin/alerts/{id}/resolve

PATCH /admin/alerts/{id}/false-positive

## Account Control

POST /admin/freeze/{account_number}

POST /admin/unfreeze/{account_number}

## Mule Detection

POST /mule/scan

POST /mule/rapid-movement

POST /mule/dormant

GET /mule/top-risk

GET /mule/network-analysis

---

# Installation

## Clone Repository

git clone <repository-url>

cd FRAUD_DETECTION

## Install Dependencies

pip install -r requirements.txt

## Configure Environment

Create a .env file:

DATABASE_URL=postgresql://username:password@localhost/fraud_db

SECRET_KEY=your_secret_key

## Run Backend

uvicorn APP.main:app --reload

Backend URL:

http://localhost:8000

Swagger Documentation:

http://localhost:8000/docs

## Run Frontend

npm install

npm run dev

Frontend URL:

http://localhost:5173

---

# Future Enhancements

* Device Fingerprinting
* Geo-Location Risk Analysis
* Behavioral Biometrics
* OTP Verification Workflow
* Face Verification Integration
* Kafka Event Streaming
* Real-Time Risk Scoring Pipeline
* SIEM Integration

---

# Author

Himanshu Chavan

Computer Science Engineering

YCCE Nagpur

