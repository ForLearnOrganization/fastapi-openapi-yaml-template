// Auto-generated TypeScript types from OpenAPI schema
// Generated at: 2025-06-19 03:55:26

// Base types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  detail?: string;
}

export interface FactResponse {
  /** Interesting fact */
  fact: string;
  /** Fact source */
  source?: any;
}

export interface GenerateTextRequest {
  /** Text prompt for generation */
  prompt: string;
  /** Maximum length of generated text */
  max_length?: any;
  /** Temperature for text generation */
  temperature?: any;
}

export interface GenerateTextResponse {
  /** Generated text */
  generated_text: string;
  /** Original input prompt */
  input_prompt: string;
  /** Additional metadata */
  metadata?: Record<string, any>;
}

export interface HTTPValidationError {
  detail?: ValidationError[];
}

export interface HealthResponse {
  /** Application status */
  status: string;
  /** Timestamp of the health check */
  timestamp: string;
  /** Application version */
  version: string;
}

export interface QuoteResponse {
  /** Quote text */
  quote: string;
  /** Quote author */
  author: string;
  /** Quote category */
  category?: any;
}

export interface ValidationError {
  loc: any[];
  msg: string;
  type: string;
}

export interface WeatherRequest {
  /** City name */
  city: string;
  /** ISO 3166 country code */
  country_code?: any;
}

export interface WeatherResponse {
  /** City name */
  city: string;
  /** Country name */
  country: string;
  /** Temperature in Celsius */
  temperature: number;
  /** Weather description */
  description: string;
  /** Humidity percentage */
  humidity?: any;
  /** Wind speed in m/s */
  wind_speed?: any;
}


// API endpoint paths
export const API_ENDPOINTS = {
  HEALTH: '/api/v1/health/',
  HEALTH_DETAILED: '/api/v1/health/detailed',
  TEXT_GENERATE: '/api/v1/text/generate',
  TEXT_ECHO: '/api/v1/text/echo',
  EXTERNAL_WEATHER: '/api/v1/external/weather',
  EXTERNAL_QUOTE: '/api/v1/external/quote',
  EXTERNAL_FACT: '/api/v1/external/fact',
  EXTERNAL_JOKE: '/api/v1/external/joke',
  LEGACY_GENERATE: '/generate',
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
