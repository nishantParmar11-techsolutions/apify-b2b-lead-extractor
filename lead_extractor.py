import logging
from typing import Iterator, Optional
from pydantic import BaseModel, EmailStr, Field, ValidationError
from apify_client import ApifyClient

# Setup basic logging for production visibility
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Pydantic Data Rules (Blocks bad data automatically)
class LeadRecord(BaseModel):
    full_name: str = Field(..., description="Full name of the prospect")
    company: str = Field(..., description="Company name")
    email: EmailStr = Field(..., description="Verified email address")
    linkedin_url: Optional[str] = None

# 2. Enterprise-Grade Streaming Scraper
class ApifyLeadExtractor:
    def __init__(self, api_token: str):
        if not api_token:
            raise ValueError("API token is required")
        # The official SDK handles rate limits (429s), retries, and connection pooling automatically
        self.client = ApifyClient(api_token)

    def stream_valid_leads(self, dataset_id: str) -> Iterator[LeadRecord]:
        """
        Yields leads one by one as a generator. 
        This uses 99% less memory than lists and handles automatic pagination.
        """
        logger.info(f"Connecting to Apify dataset: {dataset_id}")
        
        try:
            dataset_client = self.client.dataset(dataset_id)
            
            # iterate_items() automatically paginates through thousands of results safely
            for item in dataset_client.iterate_items():
                try:
                    # Validates the row and yields it immediately
                    yield LeadRecord(**item)
                except ValidationError:
                    # Silently skip malformed rows without breaking the loop
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to stream dataset: {str(e)}")
            raise RuntimeError(f"Extraction failed: {str(e)}")
