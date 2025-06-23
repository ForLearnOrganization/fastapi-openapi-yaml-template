"""
OpenAPI YAML仕様から自動生成されたPydanticモデル
手動で編集しないでください。source/openapi.yamlを編集してから再生成してください。
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(description="ヘルス状態")
    timestamp: datetime = Field(description="チェック実行時刻")


class DetailedHealthResponse(BaseModel):
    status: str = Field(description="全体ヘルス状態")
    timestamp: datetime = Field(description="チェック実行時刻")
    system_info: Optional[dict[str, Any]] = None
    services: Optional[dict[str, Any]] = None


class GenerateTextRequest(BaseModel):
    prompt: str = Field(description="テキスト生成用のプロンプト")
    max_length: int = Field(description="生成テキストの最大長", ge=1, le=1000)
    temperature: float = Field(description="テキスト生成の温度パラメータ", ge=0.0, le=2.0)


class GenerateTextResponse(BaseModel):
    generated_text: str = Field(description="生成されたテキスト")
    input_prompt: str = Field(description="元の入力プロンプト")
    metadata: Optional[dict[str, Any]] = None


class EchoTextRequest(BaseModel):
    text: str = Field(description="エコー対象のテキスト")


class EchoTextResponse(BaseModel):
    echo: str = Field(description="エコーされたテキスト")
    analysis: dict[str, Any]
    timestamp: datetime = Field(description="処理時刻")


class WeatherRequest(BaseModel):
    city: str = Field(description="都市名")


class WeatherResponse(BaseModel):
    city: str = Field(description="都市名")
    temperature: float = Field(description="気温（摂氏）")
    humidity: float = Field(description="湿度（%）")
    description: str = Field(description="天気の説明")
    is_mock: bool = Field(description="モックデータかどうか")


class QuoteResponse(BaseModel):
    quote: str = Field(description="名言")
    author: str = Field(description="著者")
    category: Optional[str] = Field(description="カテゴリ")


class FactResponse(BaseModel):
    fact: str = Field(description="興味深い豆知識")
    source: Optional[str] = Field(description="豆知識の出典")


class JokeResponse(BaseModel):
    joke: str = Field(description="プログラミングジョーク")
    type: str = Field(description="ジョークのタイプ")


class ErrorResponse(BaseModel):
    detail: str = Field(description="エラーの詳細")
    error_code: Optional[str] = Field(description="エラーコード")
    timestamp: Optional[datetime] = Field(description="エラー発生時刻")


