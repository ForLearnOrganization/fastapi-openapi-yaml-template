"""
Scalable FastAPI application with auto-generated documentation.

This application provides:
- Modular structure with routers
- Auto-generated OpenAPI documentation
- Type-safe API endpoints
- External API integrations
- Client-side type generation support
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse

from app.api.v1 import api_router
from app.core.config import settings
from app.models import GenerateTextRequest, GenerateTextResponse
from app.services.text_service import TextService


def create_custom_openapi(app: FastAPI):
    """カスタムOpenAPIスキーマを作成します。"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.version,
        description=settings.description,
        routes=app.routes,
    )

    # カスタム情報を追加
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    # サーバー情報を追加
    openapi_schema["servers"] = [
        {"url": "http://localhost:8000", "description": "開発サーバー"},
        {"url": "https://api.example.com", "description": "本番サーバー"},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


def create_application() -> FastAPI:
    """FastAPIアプリケーションを作成し設定します。"""

    # FastAPIインスタンスを作成
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description=settings.description,
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # CORSミドルウェアを追加
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )

    # APIルーターを含める
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    # カスタムOpenAPIスキーマを設定
    app.openapi = lambda: create_custom_openapi(app)

    # テキスト生成サービスのインスタンス
    text_service = TextService()

    # ルートエンドポイント
    @app.get("/", response_class=HTMLResponse)
    async def root():
        """APIドキュメントリンク付きのルートエンドポイント。"""
        return HTMLResponse(
            content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>localLLM-FastAPI</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .header { text-align: center; margin-bottom: 40px; }
                .links { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }
                .link-card { 
                    background: #f0f0f0; 
                    padding: 20px; 
                    border-radius: 8px; 
                    text-decoration: none; 
                    color: #333;
                    min-width: 200px;
                    text-align: center;
                }
                .link-card:hover { background: #e0e0e0; }
                .version { color: #666; font-size: 0.9em; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🚀 localLLM-FastAPI</h1>
                    <p class="version">バージョン """
            + settings.version
            + """</p>
                    <p>"""
            + settings.description
            + """</p>
                </div>
                <div class="links">
                    <a href="/docs" class="link-card">
                        <h3>📖 Swagger UI</h3>
                        <p>インタラクティブAPIドキュメント</p>
                    </a>
                    <a href="/redoc" class="link-card">
                        <h3>📋 ReDoc</h3>
                        <p>代替APIドキュメント</p>
                    </a>
                    <a href="/openapi.json" class="link-card">
                        <h3>🔧 OpenAPIスキーマ</h3>
                        <p>型生成用JSONスキーマ</p>
                    </a>
                    <a href="/api/v1/health" class="link-card">
                        <h3>❤️ ヘルスチェック</h3>
                        <p>アプリケーションステータス</p>
                    </a>
                </div>
            </div>
        </body>
        </html>
        """
        )

    # 元の/generateエンドポイント（後方互換性のため）
    @app.post("/generate", response_model=GenerateTextResponse)
    async def generate_text_legacy(request: GenerateTextRequest):
        """
        元の/generateエンドポイント（後方互換性のため）

        この機能は /api/v1/text/generate に移行されましたが、
        既存のクライアントとの互換性を保つために提供されています。
        """
        try:
            result = await text_service.generate_text(
                prompt=request.prompt,
                max_length=request.max_length or 50,
                temperature=request.temperature or 1.0,
            )
            return result
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"テキスト生成に失敗しました: {str(e)}"
            )

    return app


# アプリケーションインスタンスを作成
app = create_application()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)
