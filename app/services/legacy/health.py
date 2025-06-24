"""Health check service functions."""

import platform
import sys
import time
from datetime import datetime

from app.generated.generated_models import DetailedHealthResponse, HealthResponse


async def get_health() -> HealthResponse:
    """基本ヘルスチェック"""
    return HealthResponse(status="healthy", timestamp=datetime.now())


async def get_health_detailed() -> DetailedHealthResponse:
    """システムの詳細情報とヘルス状態"""
    start_time = getattr(get_health_detailed, "start_time", time.time())
    if not hasattr(get_health_detailed, "start_time"):
        get_health_detailed.start_time = start_time

    return DetailedHealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        system_info={
            "python_version": sys.version,
            "platform": platform.platform(),
            "memory_usage": "not_available",  # MB (psutil not installed)
            "uptime": time.time() - start_time,
        },
        services={
            "database": "not_configured",
            "cache": "not_configured",
            "external_apis": "mock_mode",
        },
    )
