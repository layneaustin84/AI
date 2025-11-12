"""
Pydantic models for request/response handling
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class HumanizeRequest(BaseModel):
    """Request model for humanizing text."""
    text: str = Field(..., description="Text to humanize", min_length=1, max_length=50000)
    tone: str = Field(default="friendly", description="Tone profile to use")
    doc_type: Optional[str] = Field(None, description="Document type for auto-profile")
    instruction: Optional[str] = Field(None, description="Custom instruction to append")


class HumanizeResponse(BaseModel):
    """Response model for humanized text."""
    original: str
    humanized: str
    tone: str
    input_length: int
    output_length: int
    timestamp: datetime


class SummarizeRequest(BaseModel):
    """Request model for summarizing text."""
    text: str = Field(..., description="Text to summarize", min_length=1, max_length=50000)
    length: str = Field(default="short", description="Summary length: short, medium, long")


class SummarizeResponse(BaseModel):
    """Response model for summary."""
    original: str
    summary: str
    input_length: int
    output_length: int
    timestamp: datetime


class TakeawaysRequest(BaseModel):
    """Request model for extracting takeaways."""
    text: str = Field(..., description="Text to extract takeaways from", min_length=1, max_length=50000)


class TakeawaysResponse(BaseModel):
    """Response model for takeaways."""
    original: str
    takeaways: str
    input_length: int
    output_length: int
    timestamp: datetime


class ToneProfile(BaseModel):
    """Model representing a tone profile."""
    name: str
    description: str
    tone_keywords: List[str]
    use_cases: List[str]


class ProfilesResponse(BaseModel):
    """Response model for available profiles."""
    profiles: Dict[str, ToneProfile]
    total: int


class DocumentType(BaseModel):
    """Model representing a document type."""
    type: str
    default_profile: str


class TypesResponse(BaseModel):
    """Response model for document types."""
    types: List[DocumentType]
    total: int


class OperationLog(BaseModel):
    """Model representing a logged operation."""
    timestamp: str
    operation: str
    input_length: int
    output_length: int
    tone_profile: str
    doc_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class HistoryResponse(BaseModel):
    """Response model for operation history."""
    operations: List[OperationLog]
    total: int
    limit: int


class StatsResponse(BaseModel):
    """Response model for usage statistics."""
    total_operations: int
    avg_input_length: int
    avg_output_length: int
    compression_ratio: float
    last_operation: Optional[str]


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime


class BatchUploadResponse(BaseModel):
    """Response model for batch upload processing."""
    files_processed: int
    successful: int
    failed: int
    results: List[Dict[str, Any]]
    timestamp: datetime


class ChangelogEntry(BaseModel):
    """Model for operation changelog."""
    original_text: str
    humanized_text: str
    tone_profile: str
    custom_instruction: Optional[str]
    timestamp: datetime
