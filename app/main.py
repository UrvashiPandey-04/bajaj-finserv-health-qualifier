import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.utils.logger import logger
from app.services.webhook_service import generate_webhook
from app.services.sql_service import get_sql_query
from app.services.submit_service import submit_sql_query

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Asynchronous lifespan manager for the FastAPI application.
    Executes automatically on startup, performing all the qualifier steps
    without manual intervention or endpoint requests.
    """
    logger.info("==================================================")
    logger.info("FASTAPI APP LIFESPAN STARTING - RUNNING AUTOMATIC WORKFLOW")
    logger.info("==================================================")
    
    # Run the qualifier workflow in a separate worker thread or async executor
    # to avoid blocking the main event loop if startup takes a bit of time.
    # Here, we run it within the startup context.
    loop = asyncio.get_running_loop()
    
    try:
        # STEP 1: Generate webhook credentials (name, regNo, email)
        webhook_url, access_token = await loop.run_in_executor(
            None, generate_webhook
        )
        
        # STEP 2 & 3: Select SQL query based on registration number parity
        selected_query = get_sql_query(
            reg_no=settings.REG_NO, 
            dialect=settings.DB_DIALECT
        )
        
        # STEP 4: Submit the final query
        success = await loop.run_in_executor(
            None, submit_sql_query, selected_query, access_token
        )
        
        if success:
            logger.info("==================================================")
            logger.info("QUALIFIER FLOW EXECUTED SUCCESSFULLY")
            logger.info("==================================================")
        else:
            logger.error("==================================================")
            logger.error("QUALIFIER FLOW EXECUTED WITH SUBMISSION FAILURE")
            logger.error("==================================================")
            
    except Exception as e:
        logger.critical("==================================================")
        logger.critical(f"QUALIFIER FLOW ABORTED DUE TO AN UNCAUGHT EXCEPTION:")
        logger.critical(f"Reason: {str(e)}")
        logger.critical("==================================================")
        
    yield
    
    logger.info("==================================================")
    logger.info("FASTAPI APP LIFESPAN SHUTTING DOWN")
    logger.info("==================================================")

# Initialize production-ready FastAPI app with custom lifecycle
app = FastAPI(
    title="Bajaj Finserv Health Qualifier",
    description="Automated FastAPI backend that executes SQL qualifier tasks on startup.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    """
    Health check endpoint for Render/Railway/Koyeb deployment monitoring.
    """
    return {
        "status": "healthy",
        "app": "bajaj-finserv-health-qualifier",
        "config": {
            "name": settings.NAME,
            "reg_no": settings.REG_NO,
            "email": settings.EMAIL,
            "db_dialect": settings.DB_DIALECT
        }
    }
