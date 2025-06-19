#!/bin/bash
# Next.jsプロジェクト用のクライアントサイド型生成スクリプト

echo "🚀 FastAPI用のクライアントサイド型を生成中..."

# プロジェクトディレクトリに移動
cd "$(dirname "$0")/.."

# 出力ディレクトリを作成
mkdir -p generated

# サーバーが既に実行されているかチェック
if curl -s http://localhost:8000/openapi.json > /dev/null 2>&1; then
    echo "📡 localhost:8000で実行中のFastAPIサーバーを使用..."
    BASE_URL="http://localhost:8000"
else
    echo "🔧 一時的なFastAPIサーバーを起動中..."
    # バックグラウンドでサーバーを起動
    python3 -m uvicorn main:app --port 8001 --host 127.0.0.1 &
    SERVER_PID=$!
    
    # サーバーの起動を待機
    echo "⏳ サーバーの起動を待機中..."
    for i in {1..30}; do
        if curl -s http://localhost:8001/openapi.json > /dev/null 2>&1; then
            echo "✅ サーバーが準備完了！"
            break
        fi
        sleep 1
        if [ $i -eq 30 ]; then
            echo "❌ 30秒以内にサーバーの起動に失敗しました"
            kill $SERVER_PID 2>/dev/null
            exit 1
        fi
    done
    BASE_URL="http://localhost:8001"
fi

# OpenAPIスキーマをダウンロード
echo "📥 OpenAPIスキーマをダウンロード中..."
curl -s "$BASE_URL/openapi.json" > generated/openapi.json

if [ $? -eq 0 ]; then
    echo "✅ OpenAPI JSONスキーマを generated/openapi.json に保存しました"
else
    echo "❌ OpenAPIスキーマのダウンロードに失敗しました"
    [ ! -z "$SERVER_PID" ] && kill $SERVER_PID 2>/dev/null
    exit 1
fi

# JSONをYAMLに変換
echo "🔄 YAML形式に変換中..."
python3 -c "
import json
import yaml

with open('generated/openapi.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('generated/openapi.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data, f, default_flow_style=False, allow_unicode=True)

print('✅ OpenAPI YAMLスキーマを generated/openapi.yaml に保存しました')
"

# TypeScript型を生成
echo "🔧 TypeScript型を生成中..."
python3 -c "
import json
import time
from pathlib import Path

def convert_openapi_type_to_typescript(prop_def: dict) -> str:
    \"\"\"OpenAPIプロパティ定義をTypeScript型に変換します。\"\"\"
    prop_type = prop_def.get('type', 'any')
    prop_format = prop_def.get('format')
    
    if prop_type == 'string':
        if prop_format == 'date-time':
            return 'string'
        return 'string'
    elif prop_type == 'integer':
        return 'number'
    elif prop_type == 'number':
        return 'number'
    elif prop_type == 'boolean':
        return 'boolean'
    elif prop_type == 'array':
        item_type = convert_openapi_type_to_typescript(prop_def.get('items', {}))
        return f'{item_type}[]'
    elif prop_type == 'object':
        return 'Record<string, any>'
    else:
        # Check for \$ref
        ref = prop_def.get('\$ref')
        if ref:
            # Extract type name from \$ref
            return ref.split('/')[-1]
        return 'any'

# OpenAPIスキーマを読み込み
with open('generated/openapi.json', 'r', encoding='utf-8') as f:
    schema = json.load(f)

# TypeScript型定義の生成
types_content = '''// OpenAPIスキーマから自動生成されたTypeScript型定義
// 生成日時: ''' + time.strftime('%Y-%m-%d %H:%M:%S') + '''

// ベース型
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  detail?: string;
}

'''

# components/schemasが存在する場合に抽出
components = schema.get('components', {})
schemas = components.get('schemas', {})

for schema_name, schema_def in schemas.items():
    if schema_def.get('type') == 'object':
        interface_content = f'export interface {schema_name} {{\\n'
        
        properties = schema_def.get('properties', {})
        required_fields = schema_def.get('required', [])
        
        for prop_name, prop_def in properties.items():
            is_required = prop_name in required_fields
            prop_type = convert_openapi_type_to_typescript(prop_def)
            optional = '' if is_required else '?'
            description = prop_def.get('description', '')
            
            if description:
                interface_content += f'  /** {description} */\\n'
            interface_content += f'  {prop_name}{optional}: {prop_type};\\n'
        
        interface_content += '}\\n\\n'
        types_content += interface_content

# APIクライアントヘルパー型を追加
types_content += '''
// APIエンドポイントパス
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

// リクエスト/レスポンスヘルパー型
export type ApiEndpoint = typeof API_ENDPOINTS[keyof typeof API_ENDPOINTS];

// HTTPメソッド
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

// APIクライアント設定
export interface ApiClientConfig {
  baseUrl: string;
  timeout?: number;
  headers?: Record<string, string>;
}

// APIエラー型
export interface ApiError {
  detail: string;
  status_code?: number;
}

// fetchベースのAPIクライアントヘルパー
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
    const url = \`\${this.config.baseUrl}\${endpoint}\`;
    
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
      let errorDetail = \`HTTP error! status: \${response.status}\`;
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

  // GETリクエスト用のヘルパーメソッド
  async get<T>(endpoint: ApiEndpoint): Promise<T> {
    return this.request<T>(endpoint, 'GET');
  }

  // POSTリクエスト用のヘルパーメソッド
  async post<T>(endpoint: ApiEndpoint, data: any): Promise<T> {
    return this.request<T>(endpoint, 'POST', data);
  }

  // PUTリクエスト用のヘルパーメソッド
  async put<T>(endpoint: ApiEndpoint, data: any): Promise<T> {
    return this.request<T>(endpoint, 'PUT', data);
  }

  // DELETEリクエスト用のヘルパーメソッド
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
'''

# TypeScript型定義ファイルを保存
with open('generated/api-types.ts', 'w', encoding='utf-8') as f:
    f.write(types_content)

print('✅ TypeScript型定義を generated/api-types.ts に生成しました')
"

# サーバーをクリーンアップ - 起動した場合は停止
if [ ! -z "$SERVER_PID" ]; then
    echo "🛑 一時サーバーを停止中..."
    kill $SERVER_PID 2>/dev/null
fi

echo ""
echo "🎉 クライアント型生成が完了しました！"
echo ""
echo "生成されたファイル:"
echo "  📄 generated/openapi.json   - JSON形式のOpenAPIスキーマ"
echo "  📄 generated/openapi.yaml   - YAML形式のOpenAPIスキーマ"
echo "  📄 generated/api-types.ts   - TypeScript型定義"
echo ""
echo "📋 Next.js統合手順:"
echo "  1. generated/api-types.ts をNext.jsプロジェクトにコピー (例: types/api.ts)"
echo "  2. fetchベースのAPIクライアントを使用（axiosではなく）:"
echo ""
echo "     import { WeatherRequest, WeatherResponse, API_ENDPOINTS, createApiClient } from './types/api';"
echo ""
echo "     const apiClient = createApiClient(process.env.NEXT_PUBLIC_API_URL!);"
echo ""
echo "     const getWeather = async (request: WeatherRequest): Promise<WeatherResponse> => {"
echo "       return apiClient.post<WeatherResponse>(API_ENDPOINTS.EXTERNAL_WEATHER, request);"
echo "     };"
echo ""
echo "  3. NEXT_PUBLIC_API_URL環境変数をFastAPIサーバーURLに設定"
echo ""