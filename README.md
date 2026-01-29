# 🚚 AI-Powered Logistics & Inventory Optimization Platform (Backend)

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-323330?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn)
![AWS](https://img.shields.io/badge/AWS%20Lightsail-FF9900?style=for-the-badge&logo=amazonaws)

---

## 📌 Overview

This backend powers an **industry-grade logistics and inventory management system** with integrated **Machine Learning for demand forecasting and inventory optimization**.

The system is designed to:
- Track real-time inventory across warehouses
- Capture historical stock movements
- Forecast future product demand using ML
- Recommend optimal reorder quantities
- Support role-based access for different users

This project follows **backend-first architecture**, **production ML practices**, and **explainable decision logic**.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** – High-performance REST API framework
- **SQLAlchemy** – ORM for database interaction
- **PostgreSQL** – Relational database
- **Alembic** – Database migrations
- **JWT (python-jose)** – Authentication & authorization
- **Passlib (bcrypt)** – Secure password hashing
- **dotenv** – Environment variable management

### Machine Learning & Data Science
- **Pandas** – Data manipulation
- **NumPy** – Numerical computing
- **scikit-learn** – ML modeling
- **RandomForestRegressor** – Demand forecasting model
- **Joblib** – Model serialization

---

## 👥 User Roles

| Role | Capabilities |
|----|----|
| **Super Admin** | Full system access |
| **Warehouse Manager** | Inventory, orders, ML insights |
| **Delivery Boy** | Delivery status updates |

---

## 🧱 Backend Architecture

```
backend/
├── core/
├── models/
├── schemas/
├── api/
├── ml/
├── scripts/
├── alembic/
├── main.py
└── requirements.txt
```

---

## 🔐 Authentication & Authorization

- JWT-based stateless authentication
- Role-based route protection
- Secure password hashing using bcrypt
- Environment-based secret management

---

## 📦 Inventory System Design (ML-Ready)

### Key Tables
- **inventory** → Current stock state
- **inventory_logs** → Historical stock movements

### Why `inventory_logs` exists
- Captures every stock change as a time-stamped event
- Enables demand trend analysis
- Serves as the **only data source for ML training**
- Provides auditability and traceability

---

## 🧠 Machine Learning Pipeline

### Demand Forecasting
- Supervised regression problem
- Trained on 6 months of synthetic inventory consumption data
- Features: warehouse, product, day, month, weekday, weekend
- Model: RandomForestRegressor
- Metric: Mean Absolute Error (MAE ≈ 4.2)

### Reorder Recommendation Engine
- Combines ML forecasts with inventory logic
- Calculates reorder point, safety stock, and reorder quantity
- Fully explainable decision system

---

## 🔁 Synthetic Data Generation

- Simulates realistic logistics operations
- Includes seasonal demand and weekend spikes
- Generates ML-grade training data

---

## 🌐 Deployment

- Backend: AWS Lightsail (Amazon Linux 2023)
- Database: PostgreSQL
- ML inference served via FastAPI
- Secrets managed using `.env`

---

## ✅ Key Highlights

- Backend-first architecture
- Realistic ML pipeline
- Explainable AI decisions
- Industry-aligned logistics use cases

---

## 🚀 Next Phase

Frontend integration with React + Vite + Tailwind + shadcn/ui

## Run backend on your device
```
git clone https://github.com/chiragRane-Projects/inv_backend.git

cd inv_backend/

python -m venv env #Linux/MacOs
source env/bin/activate

pip install -r requirements.txt

uvicorn main:app --reload

```