# 🚨 AI-Powered Banking Fraud Detection & Mule Account Monitoring System

## Problem Statement

Banks face increasing financial fraud through:

* Fraudulent transactions
* Mule accounts used to move illegal funds
* Rapid money movement between accounts
* Dormant accounts suddenly becoming active
* Manual fraud investigation delays
* Fraud systems that can't scale past a single server

This project provides an AI-powered fraud monitoring platform that detects suspicious transactions in real time, identifies mule accounts, generates live alerts across every running instance, and supports fraud investigation workflows — built on an event-driven architecture so detection, alerting, and case management scale independently of each other.

---

## What I Built

A full-stack fraud detection platform with:

* AI-based Fraud Detection (XGBoost)
* Real-Time, Per-Transaction Risk Scoring
* Mule Account Detection Engine
* Event-Driven Architecture with Kafka
* Real-Time, Multi-Instance Fraud Alerts (Redis Pub/Sub + WebSockets)
* Automated Case Creation for High-Risk Alerts
* Network Analysis Dashboard
* Investigation & Case Management System
* Account Freeze / Unfreeze Controls
* Dockerized, Multi-Service Deployment

---

## Key Features

### 🤖 Fraud Detection Engine

* XGBoost-based fraud prediction
* Fraud probability scoring
* Risk score generation (0–100)
* Real-time transaction evaluation, before money ever moves — a transaction scoring high enough is blocked outright, never touching account balances

### 🚨 Mule Detection

* Multiple Sender Detection
* Rapid Money Movement Detection
* Dormant Account Detection
* Runs two ways: scoped, indexed checks inline on every transaction, plus a periodic time-bounded scan as a backstop for patterns that build up gradually

### ⚡ Event-Driven Architecture (Kafka)

* Transactional outbox pattern — a transfer and its event are written in the same DB commit, so an event can never fire for a transfer that didn't happen (or vice versa)
* `transactions.created` and `fraud.alerts` topics
* Independent consumers for audit logging and automated case creation, each scalable on its own without touching the transfer API

### 📡 Real-Time Alerts (Redis + WebSockets)

* Alerts fan out via Redis pub/sub, so every API replica's connected clients get notified — not just the replica that generated the alert
* Live `/ws/alerts` feed for dashboards

### 📊 Admin Dashboard

* Transaction Monitoring
* Fraud Analytics
* Alert Management
* High-Risk Account Tracking

### 🕵️ Investigation Workflow

* Review Alerts
* Resolve Alerts
* False Positive Management
* Investigation Cases — created manually or auto-opened by the case automation consumer for high-risk alerts

### 🌐 Network Analysis

Visualizes:

* Money flow between accounts
* Suspicious transaction chains
* High-risk account networks

---

## System Architecture

```
Transaction Request
  → Account Locking (prevents race conditions on balance)
  → Real-Time Risk Engine (ML model + mule/rapid/dormant rule checks)
  → Block (risk ≥ 85)  or  Complete + Flag (risk ≥ 60)
  → Postgres commit (transaction + outbox event, same transaction)
       │
       ├─▶ Outbox Worker → Kafka topic: transactions.created
       │        └─▶ Audit Consumer → audit_log (append-only ledger)
       │
       └─▶ Alert Service ─┬─▶ Kafka topic: fraud.alerts
                           │       └─▶ Case Automation Consumer → auto-opened Investigation Case
                           │
                           └─▶ Redis Pub/Sub → every API replica → connected WebSocket clients
                                                                        │
                                                                        ▼
                                                              Admin Dashboard (live)
```

Kafka and Redis are each doing a different job on purpose: Kafka is the
durable, replayable event log that audit and case-automation consume;
Redis is low-latency fan-out for whoever has a dashboard open right now.

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
* Redis (real-time alert fan-out across replicas)
* Kafka / aiokafka (event streaming, transactional outbox)

### Machine Learning

* XGBoost
* Scikit-Learn
* Pandas
* NumPy
* SMOTE

### DevOps

* Docker
* Docker Compose (Postgres + Redis + Kafka + API + background workers)
* GitHub

---

## Achievements

✅ AI-Powered Fraud Detection

✅ Real-Time, Per-Transaction Risk Scoring

✅ Mule Account Detection Engine

✅ Kafka Event Streaming with Transactional Outbox

✅ Redis Pub/Sub Multi-Instance Alert Fan-Out

✅ Automated Case Creation for High-Risk Alerts

✅ Network Analysis Dashboard

✅ Investigation Case Management

✅ Account Freeze Protection

✅ React + FastAPI Full-Stack Application

✅ PostgreSQL Integration

✅ Docker Containerization (multi-service)

---

## Project Structure

```text
BANKING-FRAUD-DETECTION

├── BACKEND
│   ├── APP
│   │   ├── routers            # auth, account, transaction, admin, mule, fraud
│   │   ├── websocket          # alert_socket.py (Redis-backed fan-out)
│   │   ├── ml                 # predictor.py, model training scripts
│   │   ├── model.py           # SQLAlchemy models (incl. OutboxEvent, AuditLog)
│   │   └── main.py
│   ├── services
│   │   ├── risk_engine.py     # real-time fraud/mule scoring
│   │   ├── transfer_service.py
│   │   ├── alert_service.py
│   │   └── event_publisher.py
│   ├── consumers
│   │   ├── audit_consumer.py
│   │   └── case_automation_consumer.py
│   ├── outbox_publisher_worker.py
│   ├── docker-compose.yml
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

> Needs Postgres configured in `.env` at minimum. Redis and Kafka are
> optional for basic API use — without them, transfers and fraud scoring
> still work, you just won't get live WebSocket alerts or event
> streaming to the audit/case-automation consumers. See **Docker Setup**
> below for the full stack.

### Frontend

```bash
cd FRONTEND

npm install

npm run dev
```

---

## Docker Setup

### Full stack (Postgres + Redis + Kafka + API + workers)

```bash
cd BACKEND

docker compose up -d --build

# first run only — creates new tables/columns
docker compose exec api python migrate.py
```

Scale any consumer independently:

```bash
docker compose up -d --scale audit-consumer=3
```

### Backend image only

```bash
docker build -t fraud-backend .

docker run -p 8000:8000 fraud-backend
```

---

## Future Improvements

* Device Fingerprinting
* Geo-Location Risk Analysis
* Behavioral Biometrics
* OTP Verification
* Face Verification

---

## Author

*Himanshu Jagannath Chavan
