#!/usr/bin/env python3
"""
クライアントサイド型生成用のOpenAPIスキーマファイル生成スクリプト

このスクリプトはFastAPIサーバーを一時的に起動してOpenAPIスキーマを抽出し、
クライアントサイド型生成用にJSON、YAML、TypeScript形式で保存します。
"""

import asyncio
import json
import threading
import time
from pathlib import Path

import httpx
import uvicorn
import yaml


def start_server_temporarily():
    """サーバーを別スレッドで起動します。"""
    config = uvicorn.Config("main:app", host="127.0.0.1", port=8001, log_level="error")
    server = uvicorn.Server(config)

    def run_server():
        asyncio.run(server.serve())

    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    return server, thread


async def fetch_openapi_schema(base_url: str = "http://127.0.0.1:8001") -> dict:
    """実行中のサーバーからOpenAPIスキーマを取得します。"""
    async with httpx.AsyncClient() as client:
        # Wait for server to be ready
        for _ in range(30):  # Try for 30 seconds
            try:
                response = await client.get(f"{base_url}/openapi.json")
                if response.status_code == 200:
                    return response.json()
            except httpx.ConnectError:
                await asyncio.sleep(1)

        raise Exception("FastAPIサーバーに接続できませんでした")


def save_openapi_files(schema: dict, output_dir: str = "generated"):
    """OpenAPIスキーマを複数の形式で保存します。"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Save as JSON
    json_path = output_path / "openapi.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
    print(f"✅ OpenAPIのJSONスキーマを保存しました: {json_path}")

    # Save as YAML
    yaml_path = output_path / "openapi.yaml"
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(schema, f, default_flow_style=False, allow_unicode=True)
    print(f"✅ OpenAPIのYAMLスキーマを保存しました: {yaml_path}")

    # Generate TypeScript types (basic structure)
    typescript_path = output_path / "api-types.ts"
    generate_typescript_types(schema, typescript_path)
    print(f"✅ TypeScript型定義を生成しました: {typescript_path}")


def generate_typescript_types(schema: dict, output_path: Path):
    """OpenAPIスキーマから基本的なTypeScript型定義を生成します。"""
    types_content = (
        """// OpenAPIスキーマから自動生成されたTypeScript型定義
// 生成日時: """
        + time.strftime("%Y-%m-%d %H:%M:%S")
        + """

// ベース型
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  detail?: string;
}

"""
    )

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

// API エラー型
export interface ApiError {
  detail: string;
  status_code?: number;
}

// fetch ベースのAPIクライアントヘルパー
export class ApiClient {
  private config: ApiClientConfig;

  constructor(config: ApiClientConfig) {
    this.config = config;
  }

  async request<T>(
    endpoint: ApiEndpoint,
    method: HttpMethod = 'GET',
    data?: any
  ): Promise<T> {
    const url = `${this.config.baseUrl}${endpoint}`;

    const options: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        ...this.config.headers,
      },
    };

    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(url, options);

    if (!response.ok) {
      let errorDetail = `HTTP error! status: ${response.status}`;
      try {
        const errorData = await response.json();
        errorDetail = errorData.detail || errorDetail;
      } catch (e) {
        // JSONパースエラーの場合はデフォルトメッセージを使用
      }
      throw new Error(errorDetail);
    }

    return response.json();
  }

  // GET リクエスト用のヘルパーメソッド
  async get<T>(endpoint: ApiEndpoint): Promise<T> {
    return this.request<T>(endpoint, 'GET');
  }

  // POST リクエスト用のヘルパーメソッド
  async post<T>(endpoint: ApiEndpoint, data: any): Promise<T> {
    return this.request<T>(endpoint, 'POST', data);
  }

  // PUT リクエスト用のヘルパーメソッド
  async put<T>(endpoint: ApiEndpoint, data: any): Promise<T> {
    return this.request<T>(endpoint, 'PUT', data);
  }

  // DELETE リクエスト用のヘルパーメソッド
  async delete<T>(endpoint: ApiEndpoint): Promise<T> {
    return this.request<T>(endpoint, 'DELETE');
  }
}

// デフォルトAPIクライアントの作成関数
export function createApiClient(baseUrl: string, options?: Partial<ApiClientConfig>): ApiClient {
  return new ApiClient({
    baseUrl,
    timeout: 10000,
    ...options,
  });
}
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(types_content)


def convert_openapi_type_to_typescript(prop_def: dict) -> str:
    """OpenAPIプロパティ定義をTypeScript型に変換します。"""
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
    """OpenAPIスキーマファイル生成のメイン関数。"""
    print("🚀 OpenAPIスキーマ抽出のためにFastAPIサーバーを起動中...")

    # Start server temporarily
    server, thread = start_server_temporarily()

    try:
        # Fetch OpenAPI schema
        print("📡 OpenAPIスキーマを取得中...")
        schema = await fetch_openapi_schema()

        # Save schema files
        print("💾 スキーマファイルを保存中...")
        save_openapi_files(schema)

        print("\n✅ スキーマ生成が正常に完了しました！")
        print("\n生成されたファイル:")
        print("  - generated/openapi.json (OpenAPIツール用)")
        print("  - generated/openapi.yaml (人間が読みやすい形式)")
        print("  - generated/api-types.ts (TypeScript型定義)")
        print("\nNext.jsでの次のステップ:")
        print("  1. api-types.ts をNext.jsプロジェクトにコピー")
        print("  2. APIコールで型を使用")
        print("  3. API_ENDPOINTS定数からエンドポイントをインポート")
        print("  4. fetchベースのAPIクライアントを使用（axiosではなく）")

    except Exception as e:
        print(f"❌ スキーマ生成エラー: {e}")

    finally:
        # Note: Server will be stopped when the script ends due to daemon thread
        print("\n🛑 一時サーバーを停止中...")


if __name__ == "__main__":
    asyncio.run(main())
