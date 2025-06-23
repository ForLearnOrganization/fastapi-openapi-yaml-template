#!/usr/bin/env python3
"""
OpenAPI YAML から TypeScript 型定義を生成するスクリプト

手書きのopenapi.yamlからTypeScript型定義を生成します。
Next.jsプロジェクトでの使用に最適化されています。
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import yaml


def load_openapi_spec(yaml_path: str) -> dict[str, Any]:
    """OpenAPI YAML仕様をロードします。"""
    with open(yaml_path, encoding='utf-8') as f:
        return yaml.safe_load(f)


def format_generated_python_files() -> None:
    """必要に応じて生成されたPythonファイルをフォーマットします。"""
    try:
        # app/generated ディレクトリにPythonファイルがあるかチェック
        generated_dir = Path("app/generated")
        if not generated_dir.exists():
            return
            
        python_files = list(generated_dir.glob("*.py"))
        if not python_files:
            return
            
        print("🎨 生成されたPythonファイルをフォーマット中...")
        
        # まずpoetry run ruffを試す
        try:
            subprocess.run([
                sys.executable, "-m", "poetry", "run", "ruff", "format", 
                *[str(f) for f in python_files]
            ], check=True, capture_output=True)
            print("✨ Pythonファイルのフォーマット完了（poetry経由）")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        # 次に直接ruffを試す  
        try:
            subprocess.run([
                "ruff", "format", *[str(f) for f in python_files]
            ], check=True, capture_output=True)
            print("✨ Pythonファイルのフォーマット完了（直接実行）")
            return
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
            
        print("⚠️  ruffが見つかりません。基本的なフォーマットをスキップします...")
        
    except Exception as e:
        print(f"⚠️  フォーマットに失敗しましたが、生成は完了しています: {e}")


def convert_openapi_type_to_typescript(prop_def: dict[str, Any]) -> str:
    """OpenAPIプロパティ定義をTypeScript型に変換します。"""
    prop_type = prop_def.get('type', 'any')
    prop_format = prop_def.get('format')

    if prop_type == 'string':
        if prop_format == 'date-time':
            return 'string'  # ISO date stringとして扱う
        # enumの処理
        enum_values = prop_def.get('enum')
        if enum_values:
            return ' | '.join([f'"{value}"' for value in enum_values])
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
        # additionalPropertiesがある場合
        if prop_def.get('additionalProperties'):
            return 'Record<string, any>'
        # プロパティが定義されている場合は個別に処理
        properties = prop_def.get('properties', {})
        if properties:
            # インライン型定義
            return 'Record<string, any>'  # 簡略化
        return 'Record<string, any>'
    else:
        # $refの処理
        ref = prop_def.get('$ref')
        if ref:
            return ref.split('/')[-1]
        # anyOfの処理
        any_of = prop_def.get('anyOf')
        if any_of:
            types = []
            for option in any_of:
                if option.get('type') == 'null':
                    continue  # nullは後でOptionalとして処理
                types.append(convert_openapi_type_to_typescript(option))
            return ' | '.join(types) if types else 'any'
        return 'any'


def generate_typescript_interface(name: str, schema: dict[str, Any]) -> str:
    """単一のTypeScriptインターフェースを生成します。"""
    description = schema.get('description', '')
    properties = schema.get('properties', {})
    required = schema.get('required', [])

    interface_def = ""

    if description:
        interface_def += f"/**\n * {description}\n */\n"

    interface_def += f"export interface {name} {{\n"

    for prop_name, prop_def in properties.items():
        is_required = prop_name in required
        prop_type = convert_openapi_type_to_typescript(prop_def)
        prop_description = prop_def.get('description', '')

        # anyOfでnullが含まれている場合の処理
        any_of = prop_def.get('anyOf')
        if any_of and any(option.get('type') == 'null' for option in any_of):
            is_required = False

        optional_marker = '' if is_required else '?'

        if prop_description:
            interface_def += f"  /** {prop_description} */\n"

        interface_def += f"  {prop_name}{optional_marker}: {prop_type};\n"

    interface_def += "}\n"

    return interface_def


def extract_api_endpoints(spec: dict[str, Any]) -> dict[str, str]:
    """API エンドポイント定数を抽出します。"""
    endpoints = {}
    paths = spec.get('paths', {})

    for path, methods in paths.items():
        for method, operation in methods.items():
            if method.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                operation_id = operation.get('operationId', '')
                if operation_id:
                    #操作IDを定数名に変換
                    const_name = operation_id.upper()
                    endpoints[const_name] = path

    return endpoints


def generate_typescript_types(spec: dict[str, Any], output_path: str) -> None:
    """TypeScript型定義ファイルを生成します。"""
    content = f"""// OpenAPI YAML仕様から自動生成されたTypeScript型定義
// 生成日時: {time.strftime('%Y-%m-%d %H:%M:%S')}
// ソース: source/openapi.yaml
//
// 手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。

// ベース型
export interface ApiResponse<T> {{
  data?: T;
  error?: string;
  detail?: string;
}}

"""

    # スキーマからインターフェースを生成
    schemas = spec.get('components', {}).get('schemas', {})

    for schema_name, schema_def in schemas.items():
        if schema_def.get('type') == 'object':
            interface_code = generate_typescript_interface(schema_name, schema_def)
            content += interface_code + "\n"

    # API エンドポイント定数
    endpoints = extract_api_endpoints(spec)
    content += "// API エンドポイント定数\n"
    content += "export const API_ENDPOINTS = {\n"

    for const_name, path in endpoints.items():
        content += f"  {const_name}: '{path}',\n"

    content += "} as const;\n\n"

    # 型ヘルパー
    content += """// 型ヘルパー
export type ApiEndpoint = typeof API_ENDPOINTS[keyof typeof API_ENDPOINTS];

// HTTP メソッド
export type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

// API クライアント設定
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

// fetchベースのAPIクライアントクラス
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
        // JSON パースエラーの場合はデフォルトメッセージを使用
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

// Next.js用のカスタムフック型定義（React Query/SWR等で使用）
export interface UseApiOptions {
  enabled?: boolean;
  refetchOnWindowFocus?: boolean;
  staleTime?: number;
}

// API呼び出し用のヘルパー型
export type ApiRequest<T> = T extends undefined ? [] : [T];
export type ApiMethod<Req, Res> = (...args: ApiRequest<Req>) => Promise<Res>;

// 型安全なAPI呼び出し関数の例
export const apiMethods = {
  // ヘルスチェック
  healthCheck: (): Promise<HealthResponse> => {
    const client = createApiClient(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');
    return client.get(API_ENDPOINTS.HEALTH_CHECK);
  },

  detailedHealthCheck: (): Promise<DetailedHealthResponse> => {
    const client = createApiClient(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');
    return client.get(API_ENDPOINTS.DETAILED_HEALTH_CHECK);
  },

  // テキスト生成
  generateText: (request: GenerateTextRequest): Promise<GenerateTextResponse> => {
    const client = createApiClient(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');
    return client.post(API_ENDPOINTS.GENERATE_TEXT, request);
  },

  echoText: (request: EchoTextRequest): Promise<EchoTextResponse> => {
    const client = createApiClient(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');
    return client.post(API_ENDPOINTS.ECHO_TEXT, request);
  },

  // 外部API
  getWeather: (request: WeatherRequest): Promise<WeatherResponse> => {
    const client = createApiClient(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');
    return client.post(API_ENDPOINTS.GET_WEATHER, request);
  },

  getRandomQuote: (): Promise<QuoteResponse> => {
    const client = createApiClient(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');
    return client.get(API_ENDPOINTS.GET_RANDOM_QUOTE);
  },

  getRandomFact: (): Promise<FactResponse> => {
    const client = createApiClient(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');
    return client.get(API_ENDPOINTS.GET_RANDOM_FACT);
  },

  getProgrammingJoke: (): Promise<JokeResponse> => {
    const client = createApiClient(process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000');
    return client.get(API_ENDPOINTS.GET_PROGRAMMING_JOKE);
  },
} as const;
"""

    # ファイルに出力
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ TypeScript型定義を生成しました: {output_file}")


def generate_openapi_files(spec: dict[str, Any], output_dir: str) -> None:
    """OpenAPI JSONとYAMLファイルを生成します。"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # JSON形式で保存
    json_path = output_path / "openapi.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(spec, f, indent=2, ensure_ascii=False)
    print(f"✅ OpenAPI JSONスキーマを生成しました: {json_path}")

    # YAML形式で保存（クリーンアップ版）
    yaml_path = output_path / "openapi.yaml"
    with open(yaml_path, 'w', encoding='utf-8') as f:
        yaml.dump(spec, f, default_flow_style=False, allow_unicode=True, indent=2)
    print(f"✅ OpenAPI YAMLスキーマを生成しました: {yaml_path}")


def main():
    """メイン処理"""
    print("🚀 OpenAPI YAML から TypeScript 型生成を開始...")

    # パス設定
    project_root = Path(__file__).parent.parent
    yaml_path = project_root / "source" / "openapi.yaml"
    types_output = project_root / "generated" / "api-types.ts"
    project_root / "docs" / "generated"

    if not yaml_path.exists():
        print(f"❌ OpenAPI YAML ファイルが見つかりません: {yaml_path}")
        sys.exit(1)

    try:
        # OpenAPI仕様をロード
        spec = load_openapi_spec(str(yaml_path))
        print(f"📖 OpenAPI仕様をロードしました: {yaml_path}")

        # TypeScript型定義生成
        generate_typescript_types(spec, str(types_output))

        # 生成されたPythonファイルがあればフォーマット
        format_generated_python_files()

        print("✅ 型生成が完了しました！")
        print()
        print("📁 生成されたファイル:")
        print(f"  🔧 TypeScript型定義: {types_output}")
        print()
        print("💡 Next.js での使用例:")
        print("  import { GenerateTextRequest, apiMethods } from './generated/api-types';")
        print("  const response = await apiMethods.generateText({ prompt: 'Hello' });")

    except Exception as e:
        print(f"❌ 型生成エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
