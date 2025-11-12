"""
Entry point for running the Personal Agent Web Dashboard backend
"""

import uvicorn
import logging
from app.config import settings

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info(f"Starting Personal Agent Web Dashboard")
    logger.info(f"API: http://{settings.api_host}:{settings.api_port}")
    logger.info(f"Docs: http://{settings.api_host}:{settings.api_port}/docs")

    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level.lower()
    )
