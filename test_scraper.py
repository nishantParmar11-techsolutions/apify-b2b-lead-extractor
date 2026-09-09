import logging
import pytest
from unittest.mock import MagicMock
from lead_extractor import ApifyLeadExtractor, LeadRecord

@pytest.fixture
def mock_apify_client(monkeypatch):
    """
    Uses Pytest's native monkeypatch for perfect isolation.
    Guarantees the real SDK is never accidentally called over the network.
    """
    mock_client_class = MagicMock()
    mock_instance = MagicMock()
    mock_client_class.return_value = mock_instance
    monkeypatch.setattr("lead_extractor.ApifyClient", mock_client_class)
    return mock_instance

@pytest.fixture
def extractor(mock_apify_client):
    return ApifyLeadExtractor(api_token="prod_secure_token_999")

def test_stream_valid_leads_with_dirty_payload(extractor, mock_apify_client, caplog):
    """
    Tests data sanitization and operational logging against real-world API bloat.
    """
    caplog.set_level(logging.INFO)
    
    # Simulates a messy Apify response with unwanted tracking fields
    dirty_mock_data = [
        {
            "full_name": "Nishant Parmar", 
            "company": "Abynthe & Co.", 
            "email": "nishant@example.com",
            "unwanted_apify_tracking_id": "xyz-987", # Must be dropped
            "linkedin_url": "https://linkedin.com/in/nishant"
        },
        {
            "full_name": "Ghost Lead", 
            "company": "No Email Corp" 
            # Missing email, must be silently skipped
        }
    ]
    
    mock_dataset = MagicMock()
    mock_dataset.iterate_items.return_value = dirty_mock_data
    mock_apify_client.dataset.return_value = mock_dataset

    # Consume the generator
    leads = list(extractor.stream_valid_leads("test_dataset_xyz"))
    
    # 1. Assert Telemetry: Did the system log its startup sequence?
    assert "Connecting to Apify dataset: test_dataset_xyz" in caplog.text
    
    # 2. Assert Sanitization: Did it drop the bad row and strip the junk fields?
    assert len(leads) == 1
    assert leads[0].email == "nishant@example.com"
    assert leads[0].linkedin_url == "https://linkedin.com/in/nishant"
    assert not hasattr(leads[0], "unwanted_apify_tracking_id")

def test_stream_api_failure_logs_and_raises(extractor, mock_apify_client, caplog):
    """
    Ensures that when Apify goes down, the exact error is logged for SysOps.
    """
    mock_apify_client.dataset.side_effect = Exception("HTTP 502 Bad Gateway")
    
    with pytest.raises(RuntimeError, match="Extraction failed: HTTP 502 Bad Gateway"):
        list(extractor.stream_valid_leads("broken_dataset_id"))
        
    # Assert Telemetry: Did the system log the exact failure reason?
    assert "Failed to stream dataset: HTTP 502 Bad Gateway" in caplog.text
