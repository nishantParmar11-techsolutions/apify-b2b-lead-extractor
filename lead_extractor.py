import os
import json
import logging
import requests
from typing import List, Dict, Any
from apify_client import ApifyClient

# Configure enterprise-grade logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [Enterprise B2B Engine] - %(message)s"
)

class EnterpriseLeadPipeline:
    """
    Production-grade B2B lead extraction, cleaning, deduplication, 
    and batch-routing engine designed for high-performance sales pods.
    """
    
    def __init__(self, apify_token: str, crm_webhook_url: str):
        self.client = ApifyClient(apify_token)
        self.crm_webhook = crm_webhook_url

    def trigger_actor(self, actor_id: str, run_input: Dict[str, Any]) -> str:
        """Triggers the Apify scraper safely with error handling."""
        logging.info(f"Triggering Apify Actor execution: {actor_id}")
        try:
            run = self.client.actor(actor_id).call(run_input=run_input)
            dataset_id = run.get("defaultDatasetId")
            logging.info(f"Actor run successful. Target Dataset ID: {dataset_id}")
            return dataset_id
        except Exception as e:
            logging.critical(f"Critical failure while executing Apify Actor: {e}")
            raise

    def fetch_and_sanitize(self, dataset_id: str) -> List[Dict[str, Any]]:
        """
        Pulls raw data, strips invalid records, normalizes strings, 
        and eliminates duplicate email entries.
        """
        logging.info("Fetching dataset items and initiating sanitization protocol...")
        raw_items = self.client.dataset(dataset_id).iterate_items()
        
        seen_emails = set()
        clean_leads = []
        
        for item in raw_items:
            email = str(item.get("email", "")).lower().strip()
            
            # Validation: Must have a valid email and unique identifier
            if email and "@" in email and email not in seen_emails:
                seen_emails.add(email)
                
                # Normalization & Data Cleaning
                clean_lead = {
                    "company_name": str(item.get("companyName", "Unknown Company")).title().strip(),
                    "decision_maker": str(item.get("fullName", "Founder / Lead")).title().strip(),
                    "contact_email": email,
                    "linkedin_profile": str(item.get("linkedinUrl", "")).strip(),
                    "company_location": str(item.get("location", "US / UK")).strip(),
                    "pipeline_status": "Enriched & Validated"
                }
                clean_leads.append(clean_lead)
                
        logging.info(f"Sanitization complete. Unique qualified leads ready: {len(clean_leads)}")
        return clean_leads

    def batch_route_to_crm(self, leads: List[Dict[str, Any]], batch_size: int = 50, dry_run: bool = False):
        """
        Sends leads to the sales pod webhook in controlled batches 
        to prevent payload-overflow errors on the receiving server.
        """
        if not leads:
            logging.warning("Pipeline output is empty. No data to route.")
            return

        if dry_run:
            logging.info(f"[DRY RUN MODE] Bypassing webhook post. {len(leads)} leads validated successfully.")
            return

        logging.info(f"Initiating batch dispatch to sales infrastructure (Batch size: {batch_size})...")
        
        for i in range(0, len(leads), batch_size):
            batch = leads[i:i + batch_size]
            payload = {
                "batch_index": (i // batch_size) + 1,
                "total_leads_in_batch": len(batch),
                "leads": batch,
                "source": "Apify_Enterprise_B2B_Pipeline"
            }
            
            try:
                response = requests.post(
                    self.crm_webhook,
                    json=payload,
                    headers={"Content-Type": "application/json"},
                    timeout=15
                )
                response.raise_for_status()
                logging.info(f"Successfully dispatched batch {(i // batch_size) + 1} ({len(batch)} records).")
            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to transmit batch {(i // batch_size) + 1}: {e}")

# ==========================================
# Execution Module
# ==========================================
if __name__ == "__main__":
    # Environment variable extraction for security
    APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN", "mock_token_for_github_preview")
    CRM_WEBHOOK_URL = os.getenv("CRM_WEBHOOK_URL", "https://hooks.your-sales-pod.com/webhook")
    
    # Target profile input for US/UK remote growth outreach
    SCRAPER_CONFIG = {
        "searchKeywords": ["Founder", "Chief Executive Officer", "VP Growth"],
        "targetRegions": ["United States", "United Kingdom"],
        "maxRecords": 200
    }
    
    pipeline = EnterpriseLeadPipeline(apify_token=APIFY_API_TOKEN, crm_webhook_url=CRM_WEBHOOK_URL)
    
    try:
        # Step 1: Extract via Apify
        dataset = pipeline.trigger_actor("apify/b2b-contact-scraper", SCRAPER_CONFIG)
        
        # Step 2: Clean, Normalize, and Deduplicate
        qualified_leads = pipeline.fetch_and_sanitize(dataset)
        
        # Step 3: Securely Dispatch in Batches (Set dry_run=False for production)
        pipeline.batch_route_to_crm(qualified_leads, batch_size=50, dry_run=True)
        
    except Exception as fatal_error:
        logging.critical("Fatal error encountered during pipeline execution.", exc_info=True)
          
