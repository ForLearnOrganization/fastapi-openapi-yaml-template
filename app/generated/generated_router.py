"""
OpenAPI YAML仕様から自動生成されたFastAPIルーター
手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。
"""

from fastapi import APIRouter

# ruff: noqa: F401
from app.generated.generated_models import (
    HealthResponse,
    DetailedHealthResponse,
    GenerateTextRequest,
    GenerateTextResponse,
    EchoTextRequest,
    EchoTextResponse,
    WeatherRequest,
    WeatherResponse,
    QuoteResponse,
    FactResponse,
    JokeResponse,
    ErrorResponse,
)
from app.services.external_service import (
    get_external_fact,
    get_external_joke,
    get_external_quote,
    post_external_weather,
)
from app.services.health import get_health, get_health_detailed
from app.services.text_service import post_generate, post_text_echo, post_text_generate

# タグ別にルーターを分割（prefixは相対パスのみ、main.pyで/api/v1が追加される）
health_router = APIRouter(prefix="/health", tags=["health"])
text_router = APIRouter(prefix="/text", tags=["text"])
external_router = APIRouter(prefix="/external", tags=["external"])
legacy_router = APIRouter(tags=["text"])


@health_router.get("/", summary="基本ヘルスチェック")
async def health_check() -> HealthResponse:
    """APIサーバーの基本動作確認"""
    return await get_health()

@health_router.get("/detailed", summary="詳細ヘルスチェック")
async def detailed_health_check() -> DetailedHealthResponse:
    """システムの詳細情報とヘルス状態"""
    return await get_health_detailed()

@text_router.post("/generate", summary="テキスト生成")
async def generate_text(request: GenerateTextRequest) -> GenerateTextResponse:
    """ルールベースまたはLLMを使用したテキスト生成"""
    return await post_text_generate(request)

@text_router.post("/echo", summary="テキストエコーと分析")
async def echo_text(request: EchoTextRequest) -> EchoTextResponse:
    """入力テキストの分析とメタデータ付きレスポンス"""
    return await post_text_echo(request)

@external_router.post("/weather", summary="天気情報取得")
async def get_weather(request: WeatherRequest) -> WeatherResponse:
    """指定された都市の天気情報（モックデータ）"""
    return await post_external_weather(request)

@external_router.get("/quote", summary="ランダム名言取得")
async def get_random_quote() -> QuoteResponse:
    """インスピレーション名言の取得（モックデータ）"""
    return await get_external_quote()

@external_router.get("/fact", summary="ランダム豆知識取得")
async def get_random_fact() -> FactResponse:
    """興味深い豆知識の取得（モックデータ）"""
    return await get_external_fact()

@external_router.get("/joke", summary="プログラミングジョーク取得")
async def get_programming_joke() -> JokeResponse:
    """開発者向けユーモア（モックデータ）"""
    return await get_external_joke()

@legacy_router.post("/generate", summary="テキスト生成（後方互換）")
async def generate_text_legacy(request: GenerateTextRequest) -> GenerateTextResponse:
    """既存コードとの後方互換性のためのエンドポイント"""
    return await post_generate(request)


# メインルーターを作成
main_router = APIRouter()
main_router.include_router(health_router)
main_router.include_router(text_router)
main_router.include_router(external_router)

# Legacy router should be separate (not include in main_router)
# so it can be mounted without /api/v1 prefix
