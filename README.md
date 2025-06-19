# 🚀 Scalable FastAPI Application

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.8-009688.svg?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg?style=flat&logo=python&logoColor=white)](https://python.org)
[![Poetry](https://img.shields.io/badge/dependency-poetry-blue.svg?style=flat&logo=poetry&logoColor=white)](https://python-poetry.org)

A production-ready, scalable FastAPI application with auto-generated documentation, type-safe API endpoints, and client-side type generation for Next.js projects.

## ✨ Features

- 🏗️ **Modular Architecture**: Clean separation with routers, services, and models
- 📖 **Auto-Generated Documentation**: Swagger UI and ReDoc with custom OpenAPI schema
- 🔄 **Type Generation**: Automatic TypeScript type generation for client-side development
- 🌐 **External API Integration**: Mock endpoints for weather, quotes, facts, and jokes
- 🧪 **Text Generation**: Rule-based text generation service (expandable to real LLMs)
- ❤️ **Health Checks**: Comprehensive health monitoring endpoints
- 🔧 **YAML Configuration**: Configuration-driven development
- 🌍 **CORS Ready**: Pre-configured for Next.js development

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Poetry (for dependency management)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ForLearnOrganization/localllm-fastapi.git
   cd localllm-fastapi
   ```

2. **Install dependencies with Poetry**
   ```bash
   poetry install
   ```

3. **Start the development server**
   ```bash
   poetry run uvicorn main:app --reload
   ```

4. **Access the application**
   - **API Documentation**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc
   - **Root Page**: http://localhost:8000/
   - **Health Check**: http://localhost:8000/api/v1/health/

## 📁 Project Structure

```
localllm-fastapi/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── health.py        # Health check endpoints
│   │   │   ├── text.py          # Text generation endpoints
│   │   │   └── external.py      # External API endpoints
│   │   └── __init__.py          # API router configuration
│   ├── core/
│   │   └── config.py            # Application settings
│   ├── models/
│   │   └── __init__.py          # Pydantic models and schemas
│   ├── services/
│   │   ├── text_service.py      # Text generation service
│   │   └── external_service.py  # External API service
│   └── utils/
│       └── openapi.py           # OpenAPI utilities
├── scripts/
│   ├── generate_client_types.py # Python script for type generation
│   └── generate_types.sh        # Shell script for type generation
├── generated/                   # Auto-generated files (created on first run)
│   ├── openapi.json
│   ├── openapi.yaml
│   └── api-types.ts
├── config.yaml                 # Configuration file
├── main.py                     # Application entry point
└── pyproject.toml              # Poetry configuration
```

## 🔧 API Endpoints

### Health Endpoints
- `GET /api/v1/health/` - Basic health check
- `GET /api/v1/health/detailed` - Detailed health information

### Text Generation
- `POST /api/v1/text/generate` - Generate text from prompt
- `POST /api/v1/text/echo` - Echo text with metadata

### External APIs (Mock Data)
- `POST /api/v1/external/weather` - Get weather information
- `GET /api/v1/external/quote` - Get random quote
- `GET /api/v1/external/fact` - Get random fact
- `GET /api/v1/external/joke` - Get programming joke

## 🎯 Usage Examples

### Text Generation
```bash
curl -X POST "http://localhost:8000/api/v1/text/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Hello world", "max_length": 100}'
```

### Weather API
```bash
curl -X POST "http://localhost:8000/api/v1/external/weather" \
     -H "Content-Type: application/json" \
     -d '{"city": "Tokyo", "country_code": "JP"}'
```

### Random Quote
```bash
curl -X GET "http://localhost:8000/api/v1/external/quote"
```

## 📦 Client-Side Type Generation

Generate TypeScript types for your Next.js project:

### Using the Shell Script (Recommended)
```bash
# Generate all types and schemas
./scripts/generate_types.sh
```

### Using the Python Script
```bash
poetry run python scripts/generate_client_types.py
```

### Next.js Integration

1. **Copy the generated types**
   ```bash
   cp generated/api-types.ts your-nextjs-project/types/api.ts
   ```

2. **Install HTTP client** (e.g., axios)
   ```bash
   npm install axios
   ```

3. **Use in your Next.js components**
   ```typescript
   import { WeatherRequest, WeatherResponse, API_ENDPOINTS } from './types/api';
   import axios from 'axios';

   const getWeather = async (request: WeatherRequest): Promise<WeatherResponse> => {
     const response = await axios.post<WeatherResponse>(
       `${process.env.NEXT_PUBLIC_API_URL}${API_ENDPOINTS.EXTERNAL_WEATHER}`,
       request
     );
     return response.data;
   };
   ```

4. **Set environment variable**
   ```bash
   # .env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

## ⚙️ Configuration

The application uses YAML-based configuration. Edit `config.yaml` to customize:

```yaml
app:
  name: "Your App Name"
  version: "1.0.0"
  debug: true

api:
  v1_prefix: "/api/v1"

cors:
  origins:
    - "http://localhost:3000"
    - "http://localhost:8000"

external_apis:
  weather:
    mock_mode: true
    api_key: "your-api-key"
```

## 🧪 Development

### Running Tests
```bash
poetry run pytest
```

### Code Formatting
```bash
poetry run black .
poetry run isort .
```

### Type Checking
```bash
poetry run mypy .
```

### Adding New Endpoints

1. **Create endpoint file** in `app/api/v1/endpoints/`
2. **Define Pydantic models** in `app/models/__init__.py`
3. **Implement business logic** in `app/services/`
4. **Register router** in `app/api/v1/__init__.py`

Example new endpoint:
```python
# app/api/v1/endpoints/new_feature.py
from fastapi import APIRouter
from app.models import NewFeatureRequest, NewFeatureResponse

router = APIRouter()

@router.post("/new-endpoint", response_model=NewFeatureResponse)
async def new_endpoint(request: NewFeatureRequest):
    # Implementation here
    pass
```

## 🌐 Deployment

### Production Setup
```bash
# Install production dependencies
poetry install --no-dev

# Run with Gunicorn
poetry run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Docker (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev
COPY . .
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the linters and tests
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Poetry Documentation](https://python-poetry.org/docs/)

---

Built with ❤️ using FastAPI and modern Python development practices.