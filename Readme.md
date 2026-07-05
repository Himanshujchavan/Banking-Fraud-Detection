# 🚨 AI-Powered Banking Fraud Detection & Mule Account Monitoring System

## Problem Statement

Banks face increasing financial fraud through:

* Fraudulent transactions
* Mule accounts used to move illegal funds
* Rapid money movement between accounts
* Dormant accounts suddenly becoming active
* Manual fraud investigation delays

This project provides an AI-powered fraud monitoring platform that detects suspicious transactions, identifies mule accounts, generates real-time alerts, and supports fraud investigation workflows.

---

## What I Built

A full-stack fraud detection platform with:

* AI-based Fraud Detection (XGBoost)
* Mule Account Detection Engine
* Real-Time Fraud Alerts
* Network Analysis Dashboard
* Investigation & Case Management System
* Account Freeze / Unfreeze Controls
* WebSocket-Based Live Monitoring
* Dockerized Backend Deployment

---

## Key Features

### 🤖 Fraud Detection Engine

* XGBoost-based fraud prediction
* Fraud probability scoring
* Risk score generation (0–100)
* Real-time transaction evaluation

### 🚨 Mule Detection

* Multiple Sender Detection
* Rapid Money Movement Detection
* Dormant Account Detection

### 📊 Admin Dashboard

* Transaction Monitoring
* Fraud Analytics
* Alert Management
* High-Risk Account Tracking

### 🕵️ Investigation Workflow

* Review Alerts
* Resolve Alerts
* False Positive Management
* Investigation Cases

### 🌐 Network Analysis

Visualizes:

* Money flow between accounts
* Suspicious transaction chains
* High-risk account networks

---

## System Architecture

Transaction
→ Fraud Detection Model
→ Risk Score Generation
→ Alert Engine
→ WebSocket Notification
→ Admin Dashboard
→ Investigation Workflow
→ Account Freeze / Unfreeze

---

## Tech Stack

### Frontend

* React.js
* React Flow
* Recharts
* Axios

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL
* WebSockets

### Machine Learning

* XGBoost
* Scikit-Learn
* Pandas
* NumPy
* SMOTE

### DevOps

* Docker
* GitHub

---

## Achievements

✅ AI-Powered Fraud Detection

✅ Mule Account Detection Engine

✅ Real-Time Alert System

✅ Network Analysis Dashboard

✅ Investigation Case Management

✅ Account Freeze Protection

✅ React + FastAPI Full-Stack Application

✅ PostgreSQL Integration

✅ Docker Containerization

---

## Project Structure

```text
BANKING-FRAUD-DETECTION

├── BACKEND
│   ├── APP
│   ├── Dockerfile
│   ├── requirements.txt
│   └── fraud_model.pkl
│
├── FRONTEND
│   ├── src
│   └── package.json
│
└── README.md
```

---

## Run Locally

### Backend

```bash
cd BACKEND

pip install -r requirements.txt

uvicorn APP.main:app --reload
```

Swagger Docs:

```text
http://localhost:8000/docs
```

### Frontend

```bash
cd FRONTEND

npm install

npm run dev
```

---

## Docker Setup

Build Image:

```bash
docker build -t fraud-backend .
```

Run Container:

```bash
docker run -p 8000:8000 fraud-backend
```

---

## Future Improvements

* Device Fingerprinting
* Geo-Location Risk Analysis
* Behavioral Biometrics
* OTP Verification
* Face Verification
* Kafka Event Streaming

---

## Author

**Himanshu Chavan**

Computer Science Engineering, YCCE Nagpur



