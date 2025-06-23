"""
OpenAPI YAML仕様から自動生成されたFastAPIルーター
手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。
"""

# ruff: noqa: F401
from fastapi import APIRouter, HTTPException

from app.generated.generated_models import (
    DetailedHealthResponse,
    EchoTextRequest,
    EchoTextResponse,
    ErrorResponse,
    FactResponse,
    GenerateTextRequest,
    GenerateTextResponse,
    HealthResponse,
    JokeResponse,
    QuoteResponse,
    WeatherRequest,
    WeatherResponse,
)

# タグ別にルーターを分割
health_router = APIRouter(prefix="/api/v1/health", tags=["health"])
text_router = APIRouter(prefix="/api/v1/text", tags=["text"])
external_router = APIRouter(prefix="/api/v1/external", tags=["external"])
legacy_router = APIRouter(tags=["text"])


@health_router.get("/api/v1/health/", summary="基本ヘルスチェック")
async def health_check() -> HealthResponse:
    """APIサーバーの基本動作確認"""
    # TODO: 実装が必要
    raise HTTPException(status_code=501, detail="Not implemented")


@health_router.get("/api/v1/health/detailed", summary="詳細ヘルスチェック")
async def detailed_health_check() -> DetailedHealthResponse:
    """システムの詳細情報とヘルス状態"""
    # TODO: 実装が必要
    raise HTTPException(status_code=501, detail="Not implemented")


@text_router.post("/api/v1/text/generate", summary="テキスト生成")
async def generate_text(request: GenerateTextRequest) -> GenerateTextResponse:
    """ルールベースまたはLLMを使用したテキスト生成"""
    # TODO: 実装が必要
    raise HTTPException(status_code=501, detail="Not implemented")


@text_router.post("/api/v1/text/echo", summary="テキストエコーと分析")
async def echo_text(request: EchoTextRequest) -> EchoTextResponse:
    """入力テキストの分析とメタデータ付きレスポンス"""
    # TODO: 実装が必要
    raise HTTPException(status_code=501, detail="Not implemented")


@external_router.post("/api/v1/external/weather", summary="天気情報取得")
async def get_weather(request: WeatherRequest) -> WeatherResponse:
    """指定された都市の天気情報（モックデータ）"""
    # TODO: 実装が必要
    raise HTTPException(status_code=501, detail="Not implemented")


@external_router.get("/api/v1/external/quote", summary="ランダム名言取得")
async def get_random_quote() -> QuoteResponse:
    """インスピレーション名言の取得（モックデータ）"""
    # TODO: 実装が必要
    raise HTTPException(status_code=501, detail="Not implemented")


@external_router.get("/api/v1/external/fact", summary="ランダム豆知識取得")
async def get_random_fact() -> FactResponse:
    """興味深い豆知識の取得（モックデータ）"""
    # TODO: 実装が必要
    raise HTTPException(status_code=501, detail="Not implemented")


@external_router.get("/api/v1/external/joke", summary="プログラミングジョーク取得")
async def get_programming_joke() -> JokeResponse:
    """開発者向けユーモア（モックデータ）"""
    # TODO: 実装が必要
    raise HTTPException(status_code=501, detail="Not implemented")


@legacy_router.post("/generate", summary="テキスト生成（後方互換）")
async def generate_text_legacy(request: GenerateTextRequest) -> GenerateTextResponse:
    """既存コードとの後方互換性のためのエンドポイント"""
    # TODO: 実装が必要
    raise HTTPException(status_code=501, detail="Not implemented")


# メインルーターを作成
main_router = APIRouter()
main_router.include_router(health_router)
main_router.include_router(text_router)
main_router.include_router(external_router)
main_router.include_router(legacy_router)
