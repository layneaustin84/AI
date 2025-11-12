"""
Utility routes
"""

import logging
from fastapi import APIRouter
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/ping")
async def ping():
    """
    Health check ping endpoint.

    Returns:
        Pong response with timestamp
    """
    return {
        "message": "pong",
        "timestamp": datetime.now().isoformat()
    }


@router.get("/info")
async def info():
    """
    Get API information.

    Returns:
        API information and version
    """
    return {
        "name": "Personal Agent Web Dashboard",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }
