#!/usr/bin/env python3
"""
Script to generate OpenAPI schema files for client-side type generation.

This script starts the FastAPI server temporarily to extract the OpenAPI schema,
then saves it in both JSON and YAML formats for client-side type generation.
"""

import json
import yaml
import asyncio
import uvicorn
import threading
import time
import httpx
from pathlib import Path


def start_server_temporarily():
    """Start the server in a separate thread."""
    config = uvicorn.Config("main:app", host="127.0.0.1", port=8001, log_level="error")
    server = uvicorn.Server(config)
    
    def run_server():
        asyncio.run(server.serve())
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    return server, thread


async def fetch_openapi_schema(base_url: str = "http://127.0.0.1:8001") -> dict:
    """Fetch OpenAPI schema from the running server."""
    async with httpx.AsyncClient() as client:
        # Wait for server to be ready
        for _ in range(30):  # Try for 30 seconds
            try:
                response = await client.get(f"{base_url}/openapi.json")
                if response.status_code == 200:
                    return response.json()
            except httpx.ConnectError:
                await asyncio.sleep(1)
        
        raise Exception("Could not connect to the FastAPI server")


def save_openapi_files(schema: dict, output_dir: str = "generated"):
    """Save OpenAPI schema in multiple formats."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save as JSON
    json_path = output_path / "openapi.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved OpenAPI JSON schema to: {json_path}")
    
    # Save as YAML
    yaml_path = output_path / "openapi.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(schema, f, default_flow_style=False, allow_unicode=True)
    print(f"✅ Saved OpenAPI YAML schema to: {yaml_path}")
    
    # Generate TypeScript types (basic structure)
    typescript_path = output_path / "api-types.ts"
    generate_typescript_types(schema, typescript_path)
    print(f"✅ Generated TypeScript types to: {typescript_path}")


def generate_typescript_types(schema: dict, output_path: Path):
    """Generate basic TypeScript type definitions from OpenAPI schema."""
    types_content = """// Auto-generated TypeScript types from OpenAPI schema
// Generated at: """ + time.strftime("%Y-%m-%d %H:%M:%S") + """

// Base types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  detail?: string;
}

"""
    
    # Extract components/schemas if they exist
    components = schema.get("components", {})
    schemas = components.get("schemas", {})
    
    for schema_name, schema_def in schemas.items():
        if schema_def.get("type") == "object":
            interface_content = f"export interface {schema_name} {{\n"
            
            properties = schema_def.get("properties", {})
            required_fields = schema_def.get("required", [])
            
            for prop_name, prop_def in properties.items():
                is_required = prop_name in required_fields
                prop_type = convert_openapi_type_to_typescript(prop_def)
                optional = "" if is_required else "?"
                description = prop_def.get("description", "")
                
                if description:
                    interface_content += f"  /** {description} */\n"
                interface_content += f"  {prop_name}{optional}: {prop_type};\n"
            
            interface_content += "}\n\n"
            types_content += interface_content
    
    # Add API client helper types
    types_content += """
// API endpoint paths
export const API_ENDPOINTS = {
  HEALTH: '/api/v1/health',
  HEALTH_DETAILED: '/api/v1/health/detailed',
  TEXT_GENERATE: '/api/v1/text/generate',
  TEXT_ECHO: '/api/v1/text/echo',
  EXTERNAL_WEATHER: '/api/v1/external/weather',
  EXTERNAL_QUOTE: '/api/v1/external/quote',
  EXTERNAL_FACT: '/api/v1/external/fact',
  EXTERNAL_JOKE: '/api/v1/external/joke',
} as const;

// Request/Response helper types
export type ApiEndpoint = typeof API_ENDPOINTS[keyof typeof API_ENDPOINTS];

// HTTP methods
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

// API client configuration
export interface ApiClientConfig {
  baseUrl: string;
  timeout?: number;
  headers?: Record<string, string>;
}
"""
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(types_content)


def convert_openapi_type_to_typescript(prop_def: dict) -> str:
    """Convert OpenAPI property definition to TypeScript type."""
    prop_type = prop_def.get("type", "any")
    prop_format = prop_def.get("format")
    
    if prop_type == "string":
        if prop_format == "date-time":
            return "string"  # or Date if you prefer
        return "string"
    elif prop_type == "integer":
        return "number"
    elif prop_type == "number":
        return "number"
    elif prop_type == "boolean":
        return "boolean"
    elif prop_type == "array":
        item_type = convert_openapi_type_to_typescript(prop_def.get("items", {}))
        return f"{item_type}[]"
    elif prop_type == "object":
        return "Record<string, any>"
    else:
        # Check for $ref
        ref = prop_def.get("$ref")
        if ref:
            # Extract type name from $ref
            return ref.split("/")[-1]
        return "any"


async def main():
    """Main function to generate OpenAPI schema files."""
    print("🚀 Starting FastAPI server to extract OpenAPI schema...")
    
    # Start server temporarily
    server, thread = start_server_temporarily()
    
    try:
        # Fetch OpenAPI schema
        print("📡 Fetching OpenAPI schema...")
        schema = await fetch_openapi_schema()
        
        # Save schema files
        print("💾 Saving schema files...")
        save_openapi_files(schema)
        
        print("\n✅ Schema generation completed successfully!")
        print("\nGenerated files:")
        print("  - generated/openapi.json (for OpenAPI tools)")
        print("  - generated/openapi.yaml (human-readable)")
        print("  - generated/api-types.ts (TypeScript types)")
        print("\nNext steps for Next.js:")
        print("  1. Copy api-types.ts to your Next.js project")
        print("  2. Use the types in your API calls")
        print("  3. Import endpoints from API_ENDPOINTS constant")
        
    except Exception as e:
        print(f"❌ Error generating schema: {e}")
    
    finally:
        # Note: Server will be stopped when the script ends due to daemon thread
        print("\n🛑 Stopping temporary server...")


if __name__ == "__main__":
    asyncio.run(main())