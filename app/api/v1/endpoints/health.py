"""Health check endpoints."""

from fastapi import APIRouter
from datetime import datetime
from app.models import HealthResponse
from app.core import settings

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    
    Returns the current status of the application.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.version
    )


@router.get("/detailed", response_model=dict)
async def detailed_health_check():
    """
    Detailed health check endpoint.
    
    Returns detailed information about the application status.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": settings.version,
        "app_name": settings.app_name,
        "description": settings.description,
        "debug_mode": settings.debug,
        "uptime": "Available since startup"
    }