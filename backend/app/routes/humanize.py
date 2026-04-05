"""
Humanize routes
"""

import logging
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from datetime import datetime

from ..models import (
    HumanizeRequest, HumanizeResponse,
    SummarizeRequest, SummarizeResponse,
    TakeawaysRequest, TakeawaysResponse,
    ErrorResponse
)
from ..services import get_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/humanize", response_model=HumanizeResponse)
async def humanize(request: HumanizeRequest):
    """
    Humanize text using a specified tone profile.

    Args:
        request: HumanizeRequest with text, tone, and optional instruction

    Returns:
        HumanizeResponse with original and humanized text
    """
    try:
        service = get_service()
        result = service.humanize_text(
            text=request.text,
            tone=request.tone,
            doc_type=request.doc_type,
            instruction=request.instruction
        )
        return HumanizeResponse(**result)

    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Humanize error: {e}")
        raise HTTPException(status_code=500, detail="Failed to humanize text")


@router.post("/summarize", response_model=SummarizeResponse)
async def summarize(request: SummarizeRequest):
    """
    Summarize text to key points.

    Args:
        request: SummarizeRequest with text

    Returns:
        SummarizeResponse with original and summary
    """
    try:
        service = get_service()
        result = service.summarize_text(request.text)
        return SummarizeResponse(**result)

    except Exception as e:
        logger.error(f"Summarize error: {e}")
        raise HTTPException(status_code=500, detail="Failed to summarize text")


@router.post("/takeaways", response_model=TakeawaysResponse)
async def takeaways(request: TakeawaysRequest):
    """
    Extract key takeaways from text.

    Args:
        request: TakeawaysRequest with text

    Returns:
        TakeawaysResponse with original and takeaways
    """
    try:
        service = get_service()
        result = service.extract_takeaways(request.text)
        return TakeawaysResponse(**result)

    except Exception as e:
        logger.error(f"Takeaways extraction error: {e}")
        raise HTTPException(status_code=500, detail="Failed to extract takeaways")


@router.post("/batch")
async def batch_humanize(
    files: list[UploadFile] = File(...),
    tone: str = Form("friendly"),
    doc_type: str = Form(None)
):
    """
    Batch humanize multiple files.

    Args:
        files: List of uploaded files
        tone: Tone profile to use
        doc_type: Document type (optional)

    Returns:
        Batch processing results
    """
    try:
        # Read file contents
        file_data = []
        for file in files:
            content = await file.read()
            try:
                text = content.decode('utf-8')
            except UnicodeDecodeError:
                text = content.decode('latin-1')

            file_data.append({
                "filename": file.filename,
                "content": text
            })

        service = get_service()
        result = service.batch_humanize(file_data, tone, doc_type)
        return result

    except Exception as e:
        logger.error(f"Batch humanize error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process batch")
