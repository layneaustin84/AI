"""
Profiles routes
"""

import logging
from fastapi import APIRouter, HTTPException

from ..models import ProfilesResponse, TypesResponse, DocumentType, ToneProfile
from ..services import get_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/profiles", response_model=ProfilesResponse)
async def list_profiles():
    """
    Get all available tone profiles.

    Returns:
        ProfilesResponse with all tone profiles
    """
    try:
        service = get_service()
        profiles_dict = service.get_tone_profiles()

        # Convert to ToneProfile models
        profiles = {
            name: ToneProfile(**profile)
            for name, profile in profiles_dict.items()
        }

        return ProfilesResponse(
            profiles=profiles,
            total=len(profiles)
        )

    except Exception as e:
        logger.error(f"Error listing profiles: {e}")
        raise HTTPException(status_code=500, detail="Failed to list profiles")


@router.get("/types", response_model=TypesResponse)
async def list_types():
    """
    Get all available document types and their default profiles.

    Returns:
        TypesResponse with document types
    """
    try:
        service = get_service()
        types_dict = service.get_document_types()

        # Convert to DocumentType models
        types = [
            DocumentType(type=doc_type, default_profile=profile)
            for doc_type, profile in types_dict.items()
        ]

        return TypesResponse(
            types=types,
            total=len(types)
        )

    except Exception as e:
        logger.error(f"Error listing types: {e}")
        raise HTTPException(status_code=500, detail="Failed to list document types")


@router.get("/profile/{profile_name}")
async def get_profile(profile_name: str):
    """
    Get details for a specific tone profile.

    Args:
        profile_name: Name of the tone profile

    Returns:
        ToneProfile details
    """
    try:
        service = get_service()
        profiles = service.get_tone_profiles()

        if profile_name not in profiles:
            raise HTTPException(status_code=404, detail=f"Profile '{profile_name}' not found")

        return ToneProfile(**profiles[profile_name])

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting profile: {e}")
        raise HTTPException(status_code=500, detail="Failed to get profile")
