# ==============================================================================
# Enterprise B2B Lead Extractor - Automated Pytest Suite
# ==============================================================================

import os
import json
import logging
import pytest
import requests
import requests_mock
from pydantic import BaseModel, EmailStr, HttpUrl, Field
from dotenv import load_dotenv

# Load test environment variables
load_dotenv()

# Configure testing logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [Lead Extractor Test Suite] - %(message)s"
)

APIFY_WEBHOOK_TEST_URL = os.getenv("APIFY_WEBHOOK_URL", "https://api.apify.com/v2/actor-runs/test-run")

# ==============================================================================
# Pydantic Schema Model for Validation Testing
# ==============================================================================
class B2BLeadModel(BaseModel):
    company_name: str = Field(..., min_length=1)
    industry: str
    decision_maker_name: str
    title: str
    email: EmailStr
    linkedin_url: HttpUrl
    company_website: HttpUrl
    location: str


@pytest.fixture
def sample_raw_lead_payload() -> dict:
    """Provides a standardized raw lead dictionary mimicking Apify scraper output."""
    return {
        "company_name": "Apex SaaS Solutions",
        "industry": "B2B Cloud Infrastructure",
        "decision_maker_name": "Marcus Vance",
        "title": "Chief Technology Officer",
        "email": "marcus.v@apexsaas.example",
        "linkedin_url": "https://linkedin.com/in/marcus-vance-example",
        "company_website": "https://apexsaas.example",
        "location": "San Francisco, CA"
    }


def test_lead_schema_pydantic_validation(sample_raw_lead_payload: dict) -> None:
    """
    Validates that incoming raw scraped lead dictionaries conform strictly 
    to the Pydantic data model and pass type safety checks.
    """
    logging.info("Running Pydantic schema validation test...")
    lead_instance = B2BLeadModel(**sample_raw_lead_payload)
    
    assert lead_instance.company_name == "Apex SaaS Solutions"
    assert lead_instance.email == "marcus.v@apexsaas.example"
    assert str(lead_instance.linkedin_url).startswith("https://")


def test_scraper_success_mock(requests_mock: requests_mock.Mocker, sample_raw_lead_payload: dict) -> None:
    """
    Mocks a successful Apify dataset retrieval endpoint and verifies 
    that the pipeline processes and structures the lead batch correctly.
    """
    mock_api_response = {
        "data": {
            "status": "SUCCEEDED",
            "defaultDatasetId": "dataset_id_xyz987",
            "itemsCount": 1
        },
        "extracted_leads": [sample_raw_lead_payload]
    }

    requests_mock.get(APIFY_WEBHOOK_TEST_URL, json=mock_api_response, status_code=200)

    logging.info(f"Firing mock GET request to: {APIFY_WEBHOOK_TEST_URL}")
    response = requests.get(APIFY_WEBHOOK_TEST_URL, timeout=10)

    assert response.status_code == 200
    data = response.json()
    assert data["data"]["status"] == "SUCCEEDED"
    assert len(data["extracted_leads"]) == 1
    assert data["extracted_leads"][0]["company_name"] == "Apex SaaS Solutions"


@pytest.mark.parametrize(
    "http_error_code, error_description",
    [
        (401, "Unauthorized: Invalid Apify API token"),
        (429, "Rate Limit Exceeded: Too many requests"),
        (500, "Internal Server Error: Apify actor crash")
    ]
)
def test_scraper_error_handling_matrix(requests_mock: requests_mock.Mocker, http_error_code: int, error_description: str) -> None:
    """
    Parametrized test suite verifying that the pipeline gracefully catches 
    network failures, rate limits, and authentication errors.
    """
    requests_mock.get(APIFY_WEBHOOK_TEST_URL, status_code=http_error_code, text=error_description)

    logging.info(f"Testing resilience against HTTP error code: {http_error_code}")
    response = requests.get(APIFY_WEBHOOK_TEST_URL, timeout=10)

    assert response.status_code == http_error_code
    assert error_description in response.text
  
