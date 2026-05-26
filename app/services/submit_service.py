import requests
from app.config import settings
from app.utils.logger import logger

def submit_sql_query(query: str, access_token: str) -> bool:
    """
    Submits the generated SQL query string to the Bajaj Finserv test API.
    
    Args:
        query: The exact SQL query string.
        access_token: The accessToken received from the webhook generation phase.
        
    Returns:
        True if the submission was successful (status 2xx/valid response), False otherwise.
    """
    url = settings.SUBMIT_WEBHOOK_URL
    
    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }
    
    payload = {
        "finalQuery": query
    }
    
    logger.info("==================================================")
    logger.info("PHASE 3: SUBMITTING FINAL SQL QUERY")
    logger.info("==================================================")
    logger.info(f"Target URL: {url}")
    logger.info(f"Headers: Authorization: {access_token[:15]}... [TRUNCATED], Content-Type: application/json")
    logger.info(f"Payload Body: {payload}")
    
    try:
        logger.info("Sending query submission POST request...")
        response = requests.post(
            url, 
            json=payload, 
            headers=headers, 
            timeout=settings.TIMEOUT
        )
        
        logger.info(f"HTTP Status Code: {response.status_code}")
        logger.info(f"Submission Response Text: {response.text}")
        
        # Check success conditions
        if response.status_code >= 200 and response.status_code < 300:
            logger.info("Submission SUCCESS: Query successfully validated by server.")
            return True
        else:
            logger.error(f"Submission FAILURE: Server responded with status code {response.status_code}")
            return False
            
    except requests.RequestException as e:
        logger.critical(f"Submission CRITICAL EXCEPTION: Failed to make the request. Reason: {str(e)}")
        return False
