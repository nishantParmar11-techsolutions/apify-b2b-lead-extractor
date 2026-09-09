# Apify B2B Lead Extractor

[![Elite CI/CD Pipeline](https://github.com/nishantParmar11-techsolutions/apify-b2b-lead-extractor/actions/workflows/ci.yml/badge.svg)](https://github.com/nishantParmar11-techsolutions/apify-b2b-lead-extractor/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2.0-e92063.svg)](https://docs.pydantic.dev/)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade Python automation engine designed to ingest, validate, sanitize, and structure raw B2B prospect data from Apify actors, routing verified, enriched leads directly into outbound CRM and email systems.

---

## 🏛️ Architectural Overview

```text
[ Apify Cloud Actors ] ───> [ Raw Dataset Ingestion ]
                                       │
                                       ▼
                            [ Pydantic v2 Schema Gate ]
                            (RFC Email & Field Validation)
                                       │
                   ┌───────────────────┴───────────────────┐
                   ▼                                       ▼
          [ Validated Leads ]                   [ Malformed Quarantine ]
                   │                                       │
                   ▼                                       ▼
       [ Downstream CRM/Sink ]                 [ Error Logs & Telemetry ]
```

---

## ⚙️ Architecture & Tech Stack

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Runtime** | Python 3.10 - 3.12 | Base execution environment |
| **Schema Validation** | Pydantic v2 | Strict data normalization and RFC email validation |
| **Data Ingestion** | Apify Client SDK | Memory-safe RESTful dataset pagination and actor run polling |
| **Test Isolation** | PyTest, `unittest.mock` | Automated network-isolated unit and edge-case testing |
| **CI/CD Automation** | GitHub Actions | Automated Flake8 linting, Black formatting, and multi-Python matrix |

---

## 🚀 Key Features

* **Strict RFC Schema Enforcement:** Leverages Pydantic `EmailStr` and custom schema validators to eliminate corrupt records and missing domains.
* **Defensive Paginated Ingestion:** Uses Python generators (`yield`) and the official Apify SDK to stream millions of rows with a ~0% memory footprint, avoiding server crashes.
* **Deterministic Mocked Testing:** Employs `pytest` and native `monkeypatch` to test network timeouts, schema drifts, and malformed API payloads without burning Apify compute units.
* **Multi-Version Pipeline:** Fully automated GitHub Actions workflow verifying compatibility across Python 3.10, 3.11, and 3.12.

---

## 📁 Repository Structure

```text
├── .github/workflows/
│   └── ci.yml               # Enterprise Multi-Python Matrix CI Pipeline
├── lead_extractor.py        # Core data ingestion, validation & export engine
├── test_scraper.py          # PyTest suite with isolated mock HTTP adapters
├── Dockerfile               # Multi-stage production container build
├── requirements.txt         # Production and development dependencies
├── .env.example             # Environment credential templates
├── Makefile                 # Build, lint, and test CLI targets
└── README.md                # Project architecture and setup documentation
```

---

## 🛠️ Quick Start

### 1. Clone & Setup Environment
```bash
git clone [https://github.com/nishantParmar11-techsolutions/apify-b2b-lead-extractor.git](https://github.com/nishantParmar11-techsolutions/apify-b2b-lead-extractor.git)
cd apify-b2b-lead-extractor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Set Environment Variables
```bash
export APIFY_API_TOKEN="your_secure_token_here"
```

### 3. Run the Streaming Extractor
```python
import os
from lead_extractor import ApifyLeadExtractor

extractor = ApifyLeadExtractor(api_token=os.getenv("APIFY_API_TOKEN"))

# Safely streams through thousands of leads row-by-row
for lead in extractor.stream_valid_leads("your_dataset_id_here"):
    print(f"Found: {lead.full_name} at {lead.company} ({lead.email})")
```

### 4. Run the Test Suite
Run the Pytest suite with strict coverage enforcement:
```bash
pytest --cov=lead_extractor --cov-report=term-missing --cov-fail-under=80 test_scraper.py
```
