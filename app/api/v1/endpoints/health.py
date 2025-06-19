"""ヘルスチェックエンドポイント"""

from datetime import datetime

from fastapi import APIRouter

from app.core import settings
from app.models import HealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    ヘルスチェックエンドポイント

    アプリケーションの現在の状態を返します。
    """
    return HealthResponse(
        status="healthy", timestamp=datetime.now(), version=settings.version
    )


@router.get("/detailed", response_model=dict)
async def detailed_health_check():
    """
    詳細ヘルスチェックエンドポイント

    アプリケーションの状態に関する詳細情報を返します。
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": settings.version,
        "app_name": settings.app_name,
        "description": settings.description,
        "debug_mode": settings.debug,
        "uptime": "起動時より利用可能",
    }
