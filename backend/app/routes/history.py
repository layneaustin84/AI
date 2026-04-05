"""
History and statistics routes
"""

import logging
from fastapi import APIRouter, HTTPException, Query

from ..models import HistoryResponse, StatsResponse, OperationLog
from ..services import get_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/history", response_model=HistoryResponse)
async def get_history(limit: int = Query(50, ge=1, le=500)):
    """
    Get operation history.

    Args:
        limit: Maximum number of entries to return

    Returns:
        HistoryResponse with operation history
    """
    try:
        service = get_service()
        operations = service.get_operation_history(limit=limit)

        # Convert to OperationLog models
        logs = [OperationLog(**op) for op in operations]

        return HistoryResponse(
            operations=logs,
            total=len(logs),
            limit=limit
        )

    except Exception as e:
        logger.error(f"Error getting history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get operation history")


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    Get usage statistics.

    Returns:
        StatsResponse with usage statistics
    """
    try:
        service = get_service()
        stats = service.get_statistics()
        return StatsResponse(**stats)

    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get statistics")


@router.get("/history/count")
async def get_history_count():
    """
    Get total number of operations logged.

    Returns:
        Dictionary with count
    """
    try:
        service = get_service()
        history = service.get_operation_history(limit=None)
        return {"count": len(history)}

    except Exception as e:
        logger.error(f"Error getting history count: {e}")
        raise HTTPException(status_code=500, detail="Failed to get history count")
