#!/bin/bash
# Shell script to generate client-side types for Next.js projects

echo "🚀 Generating client-side types for FastAPI..."

# Ensure we're in the project directory
cd "$(dirname "$0")/.."

# Create output directory if it doesn't exist
mkdir -p generated

# Check if the server is already running
if curl -s http://localhost:8000/openapi.json > /dev/null 2>&1; then
    echo "📡 Using running FastAPI server at localhost:8000..."
    BASE_URL="http://localhost:8000"
else
    echo "🔧 Starting temporary FastAPI server..."
    # Start the server in the background
    poetry run uvicorn app:app --port 8001 --host 127.0.0.1 &
    SERVER_PID=$!
    
    # Wait for server to start
    echo "⏳ Waiting for server to start..."
    for i in {1..30}; do
        if curl -s http://localhost:8001/openapi.json > /dev/null 2>&1; then
            echo "✅ Server is ready!"
            break
        fi
        sleep 1
        if [ $i -eq 30 ]; then
            echo "❌ Server failed to start within 30 seconds"
            kill $SERVER_PID 2>/dev/null
            exit 1
        fi
    done
    BASE_URL="http://localhost:8001"
fi

# Download OpenAPI schema
echo "📥 Downloading OpenAPI schema..."
curl -s "$BASE_URL/openapi.json" > generated/openapi.json

if [ $? -eq 0 ]; then
    echo "✅ OpenAPI JSON schema saved to generated/openapi.json"
else
    echo "❌ Failed to download OpenAPI schema"
    [ ! -z "$SERVER_PID" ] && kill $SERVER_PID 2>/dev/null
    exit 1
fi

# Convert JSON to YAML
echo "🔄 Converting to YAML format..."
python3 -c "
import json
import yaml

with open('generated/openapi.json', 'r') as f:
    data = json.load(f)

with open('generated/openapi.yaml', 'w') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

print('✅ OpenAPI YAML schema saved to generated/openapi.yaml')
"

# Generate TypeScript types using Python script
echo "🔧 Generating TypeScript types..."
python3 scripts/generate_client_types.py

# Clean up - kill the server if we started it
if [ ! -z "$SERVER_PID" ]; then
    echo "🛑 Stopping temporary server..."
    kill $SERVER_PID 2>/dev/null
fi

echo ""
echo "🎉 Client type generation completed!"
echo ""
echo "Generated files:"
echo "  📄 generated/openapi.json   - OpenAPI schema in JSON format"
echo "  📄 generated/openapi.yaml   - OpenAPI schema in YAML format"
echo "  📄 generated/api-types.ts   - TypeScript type definitions"
echo ""
echo "📋 Next.js Integration Instructions:"
echo "  1. Copy generated/api-types.ts to your Next.js project (e.g., types/api.ts)"
echo "  2. Install axios or your preferred HTTP client"
echo "  3. Use the generated types in your API calls:"
echo ""
echo "     import { WeatherRequest, WeatherResponse, API_ENDPOINTS } from './types/api';"
echo "     import axios from 'axios';"
echo ""
echo "     const getWeather = async (request: WeatherRequest): Promise<WeatherResponse> => {"
echo "       const response = await axios.post<WeatherResponse>("
echo "         \`\${process.env.NEXT_PUBLIC_API_URL}\${API_ENDPOINTS.EXTERNAL_WEATHER}\`,"
echo "         request"
echo "       );"
echo "       return response.data;"
echo "     };"
echo ""
echo "  4. Set NEXT_PUBLIC_API_URL environment variable to your FastAPI server URL"
echo ""