// OpenAPIスキーマから自動生成されたTypeScript型定義
// 生成日時: 2025-06-19 07:30:00

// ベース型
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  detail?: string;
}

export interface FactResponse {
  /** 興味深い豆知識 */
  fact: string;
  /** 豆知識の出典 */
  source?: any;
}

export interface GenerateTextRequest {
  /** テキスト生成用のプロンプト */
  prompt: string;
  /** 生成テキストの最大長 */
  max_length?: any;
  /** テキスト生成の温度パラメータ */
  temperature?: any;
}

export interface GenerateTextResponse {
  /** 生成されたテキスト */
  generated_text: string;
  /** 元の入力プロンプト */
  input_prompt: string;
  /** 追加のメタデータ */
  metadata?: Record<string, any>;
}

export interface HTTPValidationError {
  detail?: ValidationError[];
}

export interface HealthResponse {
  /** アプリケーションステータス */
  status: string;
  /** ヘルスチェックのタイムスタンプ */
  timestamp: string;
  /** アプリケーションバージョン */
  version: string;
}

export interface QuoteResponse {
  /** 名言テキスト */
  quote: string;
  /** 著者名 */
  author?: any;
  /** カテゴリ */
  category?: any;
}

export interface TextEchoRequest {
  /** エコーするテキスト */
  text: string;
  /** メタデータを含むかどうか */
  include_metadata?: any;
}

export interface TextEchoResponse {
  /** エコーされたテキスト */
  echo_text: string;
  /** 文字数 */
  character_count: number;
  /** 単語数 */
  word_count: number;
  /** タイムスタンプ */
  timestamp: string;
  /** 追加のメタデータ */
  metadata?: Record<string, any>;
}

export interface ValidationError {
  /** エラーの場所 */
  loc: any[];
  /** エラーメッセージ */
  msg: string;
  /** エラータイプ */
  type: string;
}

export interface WeatherRequest {
  /** 都市名 */
  city: string;
  /** 国コード（例: JP, US） */
  country_code?: any;
}

export interface WeatherResponse {
  /** 都市名 */
  city: string;
  /** 国コード */
  country: string;
  /** 気温（摂氏） */
  temperature: number;
  /** 天気の説明 */
  description: string;
  /** 湿度（%） */
  humidity: number;
  /** タイムスタンプ */
  timestamp: string;
}

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