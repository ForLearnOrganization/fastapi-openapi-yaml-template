"""Main API router for version 1."""

from fastapi import APIRouter

from .endpoints import external, health, text

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(text.router, prefix="/text", tags=["text"])
api_router.include_router(external.router, prefix="/external", tags=["external"])
