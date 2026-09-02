# Apify B2B Lead Extractor

[![Elite CI/CD Pipeline](https://github.com/nishantParmar11-techsolutions/apify-b2b-lead-extractor/actions/workflows/ci.yml/badge.svg)](https://github.com/nishantParmar11-techsolutions/apify-b2b-lead-extractor/actions/workflows/ci.yml)
![Python Versions](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)
![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Testing](https://img.shields.io/badge/tests-pytest-brightgreen)

An enterprise-grade Python automation pipeline designed to ingest, validate, and structure raw B2B prospect data from Apify actors, routing clean, enriched leads directly into outbound CRM and email systems.

---

### Core Architecture

* **Strict Schema Enforcement:** Uses Pydantic (`B2BLeadModel`) with RFC-compliant `email-validator` logic to eliminate dirty records, corrupted emails, and missing company domains before downstream delivery.
* **Defensive Ingestion:** Implements structured exception handling and payload normalization across paginated Apify dataset runs.
* **Mocked Test Suite:** Employs `pytest` and `requests-mock` to simulate real-world API status codes, rate limits, and schema edge cases without burning Apify platform compute credits.
* **Multi-Version Matrix CI/CD:** GitHub Actions runner executing automated linting (`flake8`), style checks (`black`), and full test runs across Python 3.10, 3.11, and 3.12.

---

### Architecture & Tech Stack

| Layer | Technology | Function |
| :--- | :--- | :--- |
| **Runtime** | Python 3.10 - 3.12 | Base environment |
| **Validation** | Pydantic v2, `email-validator` | Strict record typing and parsing |
| **Data Extraction** | `requests`, Apify REST API | Web scraping and actor dataset fetching |
| **Testing** | `pytest`, `requests-mock` | Automated unit testing and network isolation |
| **CI / DevOps** | GitHub Actions, Flake8, Black | Multi-matrix automated validation |

---

### Project Layout

```text
├── .github/workflows/
│   └── ci.yml             # Matrix CI/CD pipeline (Python 3.10 - 3.12)
├── lead_extractor.py      # Core data ingestion and extraction logic
├── test_scraper.py        # PyTest suite with mocked HTTP interactions
├── requirements.txt       # Production & dev dependencies
└── README.md

