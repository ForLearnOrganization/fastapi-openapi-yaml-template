"""
OpenAPI YAML仕様から自動生成されたFastAPIルーター
手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。
"""

from fastapi import APIRouter

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
from app.services.external import (
    get_programming_joke_impl,
    get_random_fact_impl,
    get_random_quote_impl,
    get_weather_impl,
)
from app.services.health import (
    get_detailed_health_check_impl,
    get_health_check_impl,
)
from app.services.text import (
    post_echo_text_impl,
    post_generate_text_impl,
    post_generate_text_legacy_impl,
)

# タグ別にルーターを分割（prefixは相対パスのみ、main.pyで/api/v1が追加される）
health_router = APIRouter(prefix="/health", tags=["health"])
text_router = APIRouter(prefix="/text", tags=["text"])
external_router = APIRouter(prefix="/external", tags=["external"])
legacy_router = APIRouter(tags=["text"])


@health_router.get("/", summary="基本ヘルスチェック")
async def health_check() -> HealthResponse:
    """APIサーバーの基本動作確認"""
    return await get_health_check_impl()


@health_router.get("/detailed", summary="詳細ヘルスチェック")
async def detailed_health_check() -> DetailedHealthResponse:
    """システムの詳細情報とヘルス状態"""
    return await get_detailed_health_check_impl()


@text_router.post("/generate", summary="テキスト生成")
async def generate_text(request: GenerateTextRequest) -> GenerateTextResponse:
    """ルールベースまたはLLMを使用したテキスト生成"""
    return await post_generate_text_impl(request)


@text_router.post("/echo", summary="テキストエコーと分析")
async def echo_text(request: EchoTextRequest) -> EchoTextResponse:
    """入力テキストの分析とメタデータ付きレスポンス"""
    return await post_echo_text_impl(request)


@external_router.post("/weather", summary="天気情報取得")
async def get_weather(request: WeatherRequest) -> WeatherResponse:
    """指定された都市の天気情報（モックデータ）"""
    return await get_weather_impl(request)


@external_router.get("/quote", summary="ランダム名言取得")
async def get_random_quote() -> QuoteResponse:
    """インスピレーション名言の取得（モックデータ）"""
    return await get_random_quote_impl()


@external_router.get("/fact", summary="ランダム豆知識取得")
async def get_random_fact() -> FactResponse:
    """興味深い豆知識の取得（モックデータ）"""
    return await get_random_fact_impl()


@external_router.get("/joke", summary="プログラミングジョーク取得")
async def get_programming_joke() -> JokeResponse:
    """開発者向けユーモア（モックデータ）"""
    return await get_programming_joke_impl()


@legacy_router.post("/generate", summary="テキスト生成（後方互換）")
async def generate_text_legacy(request: GenerateTextRequest) -> GenerateTextResponse:
    """既存コードとの後方互換性のためのエンドポイント"""
    return await post_generate_text_legacy_impl(request)


# メインルーターを作成
main_router = APIRouter()
main_router.include_router(health_router)
main_router.include_router(text_router)
main_router.include_router(external_router)

# legacy_routerはmain_routerに含めず、/api/v1を付けずにマウントするため別扱い
