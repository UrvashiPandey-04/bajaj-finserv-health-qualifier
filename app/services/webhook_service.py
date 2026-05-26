import time
import requests
from typing import Dict, Any, Tuple
from app.config import settings
from app.utils.logger import logger

def generate_webhook() -> Tuple[str, str]:
    """
    On startup, automatically POSTs to the Bajaj Finserv Health webhook generation API.
    Handles retries, timeout limits, and prints response details.
    
    Returns:
        A tuple of (webhook_url, access_token) if successful.
        
    Raises:
        requests.RequestException: If the webhook generation request fails after all retries.
        KeyError: If required keys are missing in the response body.
    """
    url = settings.GENERATE_WEBHOOK_URL
    payload = {
        "name": settings.NAME,
        "regNo": settings.REG_NO,
        "email": settings.EMAIL
    }
    
    logger.info("==================================================")
    logger.info("PHASE 1: GENERATING WEBHOOK")
    logger.info("==================================================")
    logger.info(f"Target URL: {url}")
    logger.info(f"Payload: {payload}")
    
    retries = settings.MAX_RETRIES
    delay = settings.RETRY_DELAY
    timeout = settings.TIMEOUT
    
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Sending POST request (Attempt {attempt}/{retries})...")
            response = requests.post(url, json=payload, timeout=timeout)
            
            # Print status and response logs
            logger.info(f"HTTP Status Code: {response.status_code}")
            logger.info(f"Raw Response: {response.text}")
            
            # If status code is not 2xx, raise an exception to trigger the catch & retry
            response.raise_for_status()
            
            response_json = response.json()
            
            # Extract credentials. Depending on how the api returns them, check keys.
            # Usually returns: {"webhook": "...", "accessToken": "..."} or similar structures.
            # We'll support both standard casings just in case (e.g. accessToken/access_token, webhook/webhookUrl).
            webhook_url = response_json.get("webhook") or response_json.get("webhookUrl") or response_json.get("webhook_url")
            access_token = response_json.get("accessToken") or response_json.get("access_token")
            
            # If keys are missing, log warnings but try to proceed or raise error if critical
            if not webhook_url or not access_token:
                logger.warning(
                    f"Warning: Response json did not contain exact expected keys. "
                    f"Keys found: {list(response_json.keys())}"
                )
                # Fallbacks or Raise KeyError
                if not access_token:
                    raise KeyError("Required field 'accessToken' is missing in API response.")
                if not webhook_url:
                    # If webhook is missing, we still have access_token to submit
                    webhook_url = "N/A"
                    logger.warning("Webhook URL is missing. Continuing with placeholder since Access Token is present.")

            logger.info("Successfully generated Webhook credentials:")
            logger.info(f"-> Webhook URL: {webhook_url}")
            logger.info(f"-> Access Token: {access_token[:15]}... [TRUNCATED]")
            return webhook_url, access_token
            
        except requests.RequestException as e:
            logger.error(f"Attempt {attempt} failed: {str(e)}")
            if attempt == retries:
                logger.critical("All retry attempts for Webhook Generation have failed.")
                raise e
            logger.info(f"Waiting {delay} seconds before retrying...")
            time.sleep(delay)
            # Exponential backoff
            delay *= 2
            
    raise RuntimeError("Failed to generate webhook due to unknown issues.")
