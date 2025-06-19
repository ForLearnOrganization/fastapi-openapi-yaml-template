"""
Scalable FastAPI application with auto-generated documentation.

This application provides:
- Modular structure with routers
- Auto-generated OpenAPI documentation
- Type-safe API endpoints
- External API integrations
- Client-side type generation support
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
import uvicorn

from app.core.config import settings
from app.api.v1 import api_router


def create_custom_openapi(app: FastAPI):
    """Create custom OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.version,
        description=settings.description,
        routes=app.routes,
    )
    
    # Add custom information
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    
    # Add server information
    openapi_schema["servers"] = [
        {"url": "http://localhost:8000", "description": "Development server"},
        {"url": "https://api.example.com", "description": "Production server"},
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    
    # Create FastAPI instance
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description=settings.description,
        debug=settings.debug,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=settings.cors_allow_methods,
        allow_headers=settings.cors_allow_headers,
    )
    
    # Include API router
    app.include_router(api_router, prefix=settings.api_v1_prefix)
    
    # Set custom OpenAPI schema
    app.openapi = lambda: create_custom_openapi(app)
    
    # Root endpoint
    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Root endpoint with API documentation links."""
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Scalable FastAPI Application</title>
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
                    <h1>🚀 Scalable FastAPI Application</h1>
                    <p class="version">Version """ + settings.version + """</p>
                    <p>""" + settings.description + """</p>
                </div>
                <div class="links">
                    <a href="/docs" class="link-card">
                        <h3>📖 Swagger UI</h3>
                        <p>Interactive API documentation</p>
                    </a>
                    <a href="/redoc" class="link-card">
                        <h3>📋 ReDoc</h3>
                        <p>Alternative API documentation</p>
                    </a>
                    <a href="/openapi.json" class="link-card">
                        <h3>🔧 OpenAPI Schema</h3>
                        <p>JSON schema for type generation</p>
                    </a>
                    <a href="/api/v1/health" class="link-card">
                        <h3>❤️ Health Check</h3>
                        <p>Application status</p>
                    </a>
                </div>
            </div>
        </body>
        </html>
        """)
    
    return app


# Create the application instance
app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )