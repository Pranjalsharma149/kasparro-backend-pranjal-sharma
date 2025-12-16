# 🚀 Kasparro – Backend & ETL Systems

This repository contains a **production-grade, dockerized Backend & ETL system** built as part of the Kasparro Backend & ETL Systems Assignment. The system demonstrates end-to-end ownership of data ingestion, transformation, persistence, and API exposure, following clean architecture and industry best practices.

---

## 🎯 Project Goals

* Build a **robust ETL pipeline** ingesting data from multiple heterogeneous sources
* Normalize and store data in a **PostgreSQL-backed unified schema**
* Expose a **lightweight, production-ready API**
* Ensure **incremental ingestion, fault tolerance, and observability**
* Deliver a **fully dockerized system** runnable with a single command

---

## 🧱 Architecture Overview

```
kasparro-backend-pranjal-sharma/
│
├── api/                # FastAPI routes & controllers
├── ingestion/          # ETL ingestion logic (per source)
├── services/           # Business logic & transformations
├── schemas/            # Pydantic models & validation
├── core/               # DB, config, dependencies, checkpoints
├── tests/              # Automated test suite
│
├── main.py             # Application entrypoint
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
└── README.md
```

The system follows **separation of concerns**:

* Ingestion layer handles external data fetching
* Service layer handles transformation & normalization
* Core layer handles DB, config, checkpoints, and shared utilities
* API layer exposes validated data and ETL metadata

---

## 🔌 Data Sources

### P0 – Required Sources

1. **API Source** (Authenticated)

   * Uses provided API key via environment variables
   * Example: CoinGecko / CoinPaprika

2. **CSV Source**

   * Handles schema quirks and type inconsistencies
   * Loaded incrementally into raw tables

### P1 – Additional Source

3. **Third Source**

   * Additional API / CSV / RSS feed
   * Unified into the same normalized schema

All raw ingested data is stored in:

* `raw_api_data`
* `raw_csv_data`
* `raw_third_source_data`

---

## 🔄 ETL Pipeline

### Features

* Incremental ingestion (no reprocessing)
* Checkpoint-based resume-on-failure
* Idempotent writes
* Pydantic-based validation & type cleaning

### ETL Flow

1. Fetch data from source
2. Validate & clean using Pydantic schemas
3. Store raw data (`raw_*` tables)
4. Normalize into unified tables
5. Update checkpoint table
6. Record run metadata

---

## 🧪 Testing Strategy

The project includes an automated test suite covering:

* ETL transformation logic
* Incremental ingestion & checkpoints
* Failure & recovery scenarios
* Schema mismatches
* API endpoints
* Rate limiting logic (if enabled)

Run tests using:

```bash
make test
```

---

## 🌐 API Endpoints

### GET /data

Returns normalized data with pagination & filtering.

**Features:**

* Pagination (`limit`, `offset`)
* Filtering
* Metadata returned:

  * `request_id`
  * `api_latency_ms`

---

### GET /health

Reports system health:

* Database connectivity
* Last ETL run status

---

### GET /stats

Provides ETL execution statistics:

* Records processed
* Duration
* Last success timestamp
* Last failure timestamp
* Run metadata

---

## 🐳 Dockerized Execution

The entire system runs using Docker.

### Prerequisites

* Docker
* Docker Compose
* Make

### Commands

```bash
make up     # Start ETL + API
make down   # Stop services
make test   # Run tests
```

The Docker image:

* Automatically starts the ETL service
* Exposes API endpoints immediately

---

## 🔐 Configuration & Secrets

All secrets are handled securely via environment variables:

```env
API_KEY=your_api_key_here
DATABASE_URL=postgresql://...
```

⚠️ No secrets are hard-coded.

---

## ☁️ Cloud Deployment

The system is deployed on a cloud provider (AWS / GCP / Azure) with:

* Public API endpoints
* Scheduled ETL runs (cron / scheduler)
* Cloud-native logs & metrics

During evaluation, the following will be demonstrated:

* Cron-triggered ETL runs
* Live logs & metrics via cloud dashboard
* ETL recovery after failure

---

## 🔍 Observability (Optional Enhancements)

* Structured JSON logs
* ETL run metadata
* Optional `/metrics` endpoint (Prometheus-compatible)

---

## 🧠 Design Decisions

* **FastAPI** for performance & validation
* **PostgreSQL** for reliability and schema control
* **Pydantic** for strong data contracts
* **Docker-first** approach for reproducibility
* **Checkpointing** for fault tolerance

---

## ✅ Assignment Coverage

* ✔ P0 – Foundation Layer
* ✔ P1 – Growth Layer
* ⭐ Partial P2 – Differentiators (where applicable)

This project was built with a strong emphasis on **production readiness**, **clarity**, and **scalability**, closely mirroring real-world backend ownership at Kasparro.

---

## 🙌 Final Note

This assignment was approached not just as a test, but as a **learning-focused, production-style system build**. Every design choice prioritizes reliability, maintainability, and real-world engineering standards.

**Built with curiosity. Built with clarity. Built to differentiate.** 🚀
