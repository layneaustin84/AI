"""
FastAPI application for Personal Agent Web Dashboard
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime

from .config import settings
from .routes import humanize, profiles, history, utilities
from .models import ErrorResponse

# Configure logging
logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="AI-powered text transformation web dashboard with Gemini API integration"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(humanize.router, prefix="/api", tags=["humanize"])
app.include_router(profiles.router, prefix="/api", tags=["profiles"])
app.include_router(history.router, prefix="/api", tags=["history"])
app.include_router(utilities.router, prefix="/api", tags=["utilities"])


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("🚀 Personal Agent Web Dashboard starting up")
    logger.info(f"API running at {settings.api_host}:{settings.api_port}")
    logger.info(f"CORS origins: {settings.cors_origins_list}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("🛑 Personal Agent Web Dashboard shutting down")


@app.get("/", tags=["root"])
async def root():
    """Root endpoint with API information."""
    return {
        "title": settings.api_title,
        "version": settings.api_version,
        "status": "running",
        "endpoints": {
            "profiles": "/api/profiles",
            "humanize": "/api/humanize",
            "batch": "/api/batch",
            "summarize": "/api/summarize",
            "takeaways": "/api/takeaways",
            "history": "/api/history",
            "stats": "/api/stats"
        }
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc),
            timestamp=datetime.now()
        ).model_dump()
    )
