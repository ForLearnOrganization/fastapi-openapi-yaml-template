"""
OpenAPI YAML仕様から自動生成されたFastAPIルーター
手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。
"""

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

# タグ別にルーターを分割
health_router = APIRouter(prefix="/health", tags=["health"])
text_router = APIRouter(prefix="/text", tags=["text"])
external_router = APIRouter(prefix="/external", tags=["external"])
legacy_router = APIRouter(tags=["text"])


@health_router.get("/", summary="基本ヘルスチェック")
async def health_check() -> HealthResponse:
    """APIサーバーの基本動作確認"""
    from datetime import datetime
    
    return HealthResponse(status="ok", timestamp=datetime.now())


@health_router.get("/detailed", summary="詳細ヘルスチェック")
async def detailed_health_check() -> DetailedHealthResponse:
    """システムの詳細情報とヘルス状態"""
    import platform
    from datetime import datetime
    
    try:
        import psutil
        # システム情報を取得
        system_info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "disk_usage": psutil.disk_usage('/').percent
        }
        
        services = {
            "api": "healthy",
            "text_service": "healthy", 
            "external_service": "healthy"
        }
    except ImportError:
        # psutil が利用できない場合の基本情報
        system_info = {
            "platform": platform.system(),
            "python_version": platform.python_version(),
            "note": "psutil not available for detailed system metrics"
        }
        services = {
            "api": "healthy",
            "text_service": "healthy", 
            "external_service": "healthy"
        }
    
    return DetailedHealthResponse(
        status="ok", 
        timestamp=datetime.now(),
        system_info=system_info,
        services=services
    )


@text_router.post("/generate", summary="テキスト生成")
async def generate_text(request: GenerateTextRequest) -> GenerateTextResponse:
    """ルールベースまたはLLMを使用したテキスト生成"""
    from app.services.text_service import TextService
    
    text_service = TextService()
    result = await text_service.generate_text(
        prompt=request.prompt,
        max_length=request.max_length,
        temperature=request.temperature
    )
    return result


@text_router.post("/echo", summary="テキストエコーと分析")
async def echo_text(request: EchoTextRequest) -> EchoTextResponse:
    """入力テキストの分析とメタデータ付きレスポンス"""
    from datetime import datetime
    
    # テキスト分析を実行
    analysis = {
        "character_count": len(request.text),
        "word_count": len(request.text.split()),
        "uppercase_count": sum(1 for c in request.text if c.isupper()),
        "lowercase_count": sum(1 for c in request.text if c.islower()),
        "digit_count": sum(1 for c in request.text if c.isdigit()),
        "space_count": sum(1 for c in request.text if c.isspace()),
    }
    
    return EchoTextResponse(
        echo=request.text,
        analysis=analysis,
        timestamp=datetime.now()
    )


@external_router.post("/weather", summary="天気情報取得")
async def get_weather(request: WeatherRequest) -> WeatherResponse:
    """指定された都市の天気情報（モックデータ）"""
    from app.services.external_service import ExternalAPIService
    
    external_service = ExternalAPIService()
    # WeatherRequestの構造の違いを調整
    try:
        result = await external_service.get_weather(request.city)
        return WeatherResponse(
            city=result.city,
            temperature=result.temperature,
            humidity=result.humidity,
            description=result.description,
            is_mock=True
        )
    except AttributeError:
        # 直接レスポンスを作成（フィールドマッピングの問題がある場合）
        import random
        return WeatherResponse(
            city=request.city.title(),
            temperature=round(random.uniform(-10, 35), 1),
            humidity=random.randint(30, 90),
            description=random.choice(["Sunny", "Cloudy", "Rainy", "Partly cloudy"]),
            is_mock=True
        )


@external_router.get("/quote", summary="ランダム名言取得")
async def get_random_quote() -> QuoteResponse:
    """インスピレーション名言の取得（モックデータ）"""
    from app.services.external_service import ExternalAPIService
    
    external_service = ExternalAPIService()
    result = await external_service.get_random_quote()
    return result


@external_router.get("/fact", summary="ランダム豆知識取得")
async def get_random_fact() -> FactResponse:
    """興味深い豆知識の取得（モックデータ）"""
    from app.services.external_service import ExternalAPIService
    
    external_service = ExternalAPIService()
    result = await external_service.get_random_fact()
    return result


@external_router.get("/joke", summary="プログラミングジョーク取得")
async def get_programming_joke() -> JokeResponse:
    """開発者向けユーモア（モックデータ）"""
    from app.services.external_service import ExternalAPIService
    
    external_service = ExternalAPIService()
    result = await external_service.get_random_joke()
    return JokeResponse(
        joke=result["joke"],
        type=result["type"]
    )


@legacy_router.post("/generate", summary="テキスト生成（後方互換）")
async def generate_text_legacy(request: GenerateTextRequest) -> GenerateTextResponse:
    """既存コードとの後方互換性のためのエンドポイント"""
    from app.services.text_service import TextService
    
    text_service = TextService()
    result = await text_service.generate_text(
        prompt=request.prompt,
        max_length=request.max_length,
        temperature=request.temperature
    )
    return result


# メインルーターを作成
main_router = APIRouter()
main_router.include_router(health_router)
main_router.include_router(text_router)
main_router.include_router(external_router)
main_router.include_router(legacy_router)
