# Changelog

All notable changes, architectural upgrades, and data pipeline patches to the Enterprise B2B Lead Extractor will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.1.0-PROD] - 2026-09-02
### Added
- **Enterprise Proxy Rotation Engine:** Integrated Apify residential proxy configuration rules within `.env.example` to ensure zero IP-blocking during high-volume extractions.
- **Pydantic v2 Schema Validation:** Enforced strict type-checking and automated data sanitization on all incoming raw lead payloads to guarantee clean downstream CRM exports.
- **Structured Telemetry Artifacts:** Added `sample-leads-output.json` sample output logs for complete auditing and verification.

### Optimized
- Upgraded exception handling routines to gracefully catch timeout errors and trigger automatic request retries with exponential backoff.
- Refined regex filtering rules to automatically normalize company names and strip trailing whitespace from extracted email addresses.

---

## [2.0.0] - 2026-08-22
### Added
- **Deduplication Logic:** Implemented automated duplicate checking based on domain names and LinkedIn URLs to eliminate redundant records.
- **Secure Secret Management:** Introduced environment configuration loading via `python-dotenv` for safe API token handling.

---

## [1.0.0] - 2026-08-15
### Added
- Initial release of core Python-based Apify lead scraping script.
- Basic execution instructions and markdown documentation (`README.md`).
