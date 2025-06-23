"""
OpenAPI YAML仕様から自動生成されたFastAPIルーター
手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException

# ruff: noqa: F401
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
from app.services.external_service import ExternalAPIService
from app.services.text_service import TextService

# サービスインスタンス
text_service = TextService()
external_service = ExternalAPIService()

# タグ別にルーターを分割（prefixは相対パスのみ、main.pyで/api/v1が追加される）
health_router = APIRouter(prefix="/health", tags=["health"])
text_router = APIRouter(prefix="/text", tags=["text"])
external_router = APIRouter(prefix="/external", tags=["external"])
legacy_router = APIRouter(tags=["text"])


@health_router.get("/", summary="基本ヘルスチェック")
async def health_check() -> HealthResponse:
    """APIサーバーの基本動作確認"""

    return HealthResponse(status="healthy", timestamp=datetime.now())


@health_router.get("/detailed", summary="詳細ヘルスチェック")
async def detailed_health_check() -> DetailedHealthResponse:
    """システムの詳細情報とヘルス状態"""
    import platform
    import sys
    import time

    start_time = getattr(detailed_health_check, "start_time", time.time())
    if not hasattr(detailed_health_check, "start_time"):
        detailed_health_check.start_time = start_time

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


@text_router.post("/generate", summary="テキスト生成")
async def generate_text(request: GenerateTextRequest) -> GenerateTextResponse:
    """ルールベースまたはLLMを使用したテキスト生成"""
    try:
        result = await text_service.generate_text(
            prompt=request.prompt,
            max_length=request.max_length or 100,
            temperature=request.temperature or 0.7,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"テキスト生成に失敗しました: {str(e)}"
        )


@text_router.post("/echo", summary="テキストエコーと分析")
async def echo_text(request: EchoTextRequest) -> EchoTextResponse:
    """入力テキストの分析とメタデータ付きレスポンス"""
    import re

    # Simple text analysis
    text = request.text
    character_count = len(text)
    word_count = len(text.split())

    # Simple language detection (very basic)
    if re.search(r"[ひらがなカタカナ漢字]", text):
        language = "ja"
    elif re.search(r"[a-zA-Z]", text):
        language = "en"
    else:
        language = "unknown"

    # Simple sentiment analysis (keyword based)
    positive_words = ["good", "great", "excellent", "良い", "素晴らしい", "最高"]
    negative_words = ["bad", "terrible", "awful", "悪い", "最悪", "ひどい"]

    sentiment = "neutral"
    for word in positive_words:
        if word in text.lower():
            sentiment = "positive"
            break
    for word in negative_words:
        if word in text.lower():
            sentiment = "negative"
            break

    return EchoTextResponse(
        echo=text,
        analysis={
            "character_count": character_count,
            "word_count": word_count,
            "language": language,
            "sentiment": sentiment,
        },
        timestamp=datetime.now(),
    )


@external_router.post("/weather", summary="天気情報取得")
async def get_weather(request: WeatherRequest) -> WeatherResponse:
    """指定された都市の天気情報（モックデータ）"""
    try:
        result = await external_service.get_weather(city=request.city)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"天気情報の取得に失敗しました: {str(e)}"
        )


@external_router.get("/quote", summary="ランダム名言取得")
async def get_random_quote() -> QuoteResponse:
    """インスピレーション名言の取得（モックデータ）"""
    try:
        result = await external_service.get_random_quote()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"名言の取得に失敗しました: {str(e)}"
        )


@external_router.get("/fact", summary="ランダム豆知識取得")
async def get_random_fact() -> FactResponse:
    """興味深い豆知識の取得（モックデータ）"""
    try:
        result = await external_service.get_random_fact()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"豆知識の取得に失敗しました: {str(e)}"
        )


@external_router.get("/joke", summary="プログラミングジョーク取得")
async def get_programming_joke() -> JokeResponse:
    """開発者向けユーモア（モックデータ）"""
    try:
        joke_data = await external_service.get_random_joke()
        return JokeResponse(
            joke=joke_data["joke"], type=joke_data.get("category", "programming")
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"ジョークの取得に失敗しました: {str(e)}"
        )


@legacy_router.post("/generate", summary="テキスト生成（後方互換）")
async def generate_text_legacy(request: GenerateTextRequest) -> GenerateTextResponse:
    """既存コードとの後方互換性のためのエンドポイント"""
    try:
        result = await text_service.generate_text(
            prompt=request.prompt,
            max_length=request.max_length or 100,
            temperature=request.temperature or 0.7,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"テキスト生成に失敗しました: {str(e)}"
        )


# メインルーターを作成
main_router = APIRouter()
main_router.include_router(health_router)
main_router.include_router(text_router)
main_router.include_router(external_router)

# Legacy router should be separate (not include in main_router)
# so it can be mounted without /api/v1 prefix
