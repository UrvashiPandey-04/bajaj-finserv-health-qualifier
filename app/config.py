import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file if it exists
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

class Settings:
    """
    App settings loaded from environment variables or standard defaults.
    """
    # Personal Info for Webhook Generation
    NAME: str = os.getenv("NAME", "John Doe")
    REG_NO: str = os.getenv("REG_NO", "REG12347")
    EMAIL: str = os.getenv("EMAIL", "john@example.com")
    
    # API Endpoints
    GENERATE_WEBHOOK_URL: str = os.getenv(
        "GENERATE_WEBHOOK_URL", 
        "https://bfhldevapigw.healthrx.co.in/hiring/generateWebhook/PYTHON"
    )
    SUBMIT_WEBHOOK_URL: str = os.getenv(
        "SUBMIT_WEBHOOK_URL", 
        "https://bfhldevapigw.healthrx.co.in/hiring/testWebhook/PYTHON"
    )

    # Dialect config (postgresql or mysql) for query logging format
    DB_DIALECT: str = os.getenv("DB_DIALECT", "postgresql").lower()

    # Retry Config
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    RETRY_DELAY: int = int(os.getenv("RETRY_DELAY", "2"))  # in seconds
    TIMEOUT: int = int(os.getenv("TIMEOUT", "10"))  # in seconds

# Instantiate a single global settings object
settings = Settings()
