# Apify B2B Lead Extractor

[![Elite CI/CD Pipeline](https://github.com/nishantParmar11-techsolutions/apify-b2b-lead-extractor/actions/workflows/ci.yml/badge.svg)](https://github.com/nishantParmar11-techsolutions/apify-b2b-lead-extractor/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2.0-e92063.svg)](https://docs.pydantic.dev/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade Python automation engine designed to ingest, validate, sanitize, and structure raw B2B prospect data from Apify actors, routing verified, enriched leads directly into outbound CRM and email systems.

---

## 🏛️ Architectural Overview

```
[ Apify Cloud Actors ] ───> [ Raw Dataset Ingestion ]
                                     │
                                     ▼
                      [ Pydantic v2 Schema Gate ]
                     (RFC Email & Field Validation)
                                     │
            ┌────────────────────────┴────────────────────────┐
            ▼                                                 ▼
   [ Validated Leads ]                              [ Malformed Quarantine ]
            │                                                 │
            ▼                                                 ▼
  [ Downstream CRM/Sink ]                            [ Error Logs & Telemetry ]
```

---

## ⚙️ Architecture & Tech Stack

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Runtime** | Python 3.10 – 3.12 | Base execution environment |
| **Schema Validation** | Pydantic v2, `email-validator` | Strict data normalization and RFC email validation |
| **Data Ingestion** | Apify Client, Requests | RESTful dataset pagination and actor run polling |
| **Test Isolation** | PyTest, `requests-mock` | Automated network-isolated unit and edge-case testing |
| **CI/CD Automation** | GitHub Actions Matrix | Automated Flake8 linting, Black formatting, and multi-Python matrix |

---

## 🚀 Key Features

* **Strict RFC Schema Enforcement:** Leverages Pydantic `EmailStr` and custom schema validators (`lead_extractor.py`) to eliminate corrupt records and missing domains.
* **Defensive Paginated Ingestion:** Implements automated retry logic, exponential backoff, and pagination handling across variable Apify dataset volumes.
* **Deterministic Mocked Testing:** Employs `pytest` and `requests-mock` to test network timeouts, schema drifts, and malformed API payloads without burning Apify compute units.
* **Multi-Version Pipeline:** Fully automated GitHub Actions workflow verifying compatibility across Python 3.10, 3.11, and 3.12.

---

## 📁 Repository Structure

```text
├── .github/workflows/
│   └── ci.yml             # Enterprise Multi-Python Matrix CI Pipeline
├── lead_extractor.py      # Core data ingestion, validation & export engine
├── test_scraper.py        # PyTest suite with isolated mock HTTP adapters
├── Dockerfile             # Multi-stage production container build
├── requirements.txt       # Production and development dependencies
├── .env.example           # Environment credential templates
├── Makefile               # Build, lint, and test CLI targets
└── README.md              # Project architecture and setup documentation
```

---

## 🛠️ Quick Start

### 1. Clone & Setup Environment
```bash
git clone [https://github.com/nishantParmar11-techsolutions/apify-b2b-lead-extractor.git](https://github.com/nishantParmar11-techsolutions/apify-b2b-lead-extractor.git)
cd apify-b2b-lead-extractor
python -m venv .venv
source .venv/bin/activate  #
