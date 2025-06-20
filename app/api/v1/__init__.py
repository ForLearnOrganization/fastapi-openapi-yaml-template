"""Main API router for version 1."""

from fastapi import APIRouter

# 自動生成されたインポート文
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.text import router as text_router
from app.api.v1.endpoints.external import router as external_router

# Create main API router
api_router = APIRouter()

# 自動生成されたルーター登録
api_router.include_router(health_router, prefix="/health", tags=['health'])
api_router.include_router(text_router, prefix="/text", tags=['text'])
api_router.include_router(external_router, prefix="/external", tags=['external'])


# =============================================================================
# 🔧 エンドポイント追加方法
# =============================================================================
# 新しいエンドポイントを追加するには:
# 1. app/api/endpoint_registry.py にエンドポイント設定を追加
# 2. app/api/v1/endpoints/ に対応する実装ファイルを作成
# 3. このスクリプトを実行: python3 scripts/generate_router.py
# =============================================================================

