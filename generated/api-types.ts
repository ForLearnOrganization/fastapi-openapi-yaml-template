// OpenAPI YAML仕様から自動生成されたTypeScript型定義
// 生成日時: 2025-06-20 05:54:29
// ソース: source/openapi.yaml
// 
// 手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。

// ベース型
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  detail?: string;
}

export interface HealthResponse {
  /** ヘルス状態 */
  status: string;
  /** チェック実行時刻 */
  timestamp: string;
}

export interface DetailedHealthResponse {
  /** 全体ヘルス状態 */
  status: string;
  /** チェック実行時刻 */
  timestamp: string;
  system_info?: Record<string, any>;
  services?: Record<string, any>;
}

export interface GenerateTextRequest {
  /** テキスト生成用のプロンプト */
  prompt: string;
  /** 生成テキストの最大長 */
  max_length?: number;
  /** テキスト生成の温度パラメータ */
  temperature?: number;
}

export interface GenerateTextResponse {
  /** 生成されたテキスト */
  generated_text: string;
  /** 元の入力プロンプト */
  input_prompt: string;
  metadata?: Record<string, any>;
}

export interface EchoTextRequest {
  /** エコー対象のテキスト */
  text: string;
}

export interface EchoTextResponse {
  /** エコーされたテキスト */
  echo: string;
  analysis: Record<string, any>;
  /** 処理時刻 */
  timestamp: string;
}

export interface WeatherRequest {
  /** 都市名 */
  city: string;
}

export interface WeatherResponse {
  /** 都市名 */
  city: string;
  /** 気温（摂氏） */
  temperature: number;
  /** 湿度（%） */
  humidity: number;
  /** 天気の説明 */
  description: string;
  /** モックデータかどうか */
  is_mock?: boolean;
}

export interface QuoteResponse {
  /** 名言 */
  quote: string;
  /** 著者 */
  author: string;
  /** カテゴリ */
  category?: string;
}

export interface FactResponse {
  /** 興味深い豆知識 */
  fact: string;
  /** 豆知識の出典 */
  source?: string;
}

export interface JokeResponse {
  /** プログラミングジョーク */
  joke: string;
  /** ジョークのタイプ */
  type: "programming" | "dev" | "tech";
}

export interface ErrorResponse {
  /** エラーの詳細 */
  detail: string;
  /** エラーコード */
  error_code?: string;
  /** エラー発生時刻 */
  timestamp?: string;
}

// API エンドポイント定数
export const API_ENDPOINTS = {
  HEALTH_CHECK: '/api/v1/health/',
  DETAILED_HEALTH_CHECK: '/api/v1/health/detailed',
  GENERATE_TEXT: '/api/v1/text/generate',
  ECHO_TEXT: '/api/v1/text/echo',
  GET_WEATHER: '/api/v1/external/weather',
  GET_RANDOM_QUOTE: '/api/v1/external/quote',
  GET_RANDOM_FACT: '/api/v1/external/fact',
  GET_PROGRAMMING_JOKE: '/api/v1/external/joke',
  GENERATE_TEXT_LEGACY: '/generate',
} as const;

// 型ヘルパー
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
