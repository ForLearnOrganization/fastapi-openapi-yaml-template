# """Common Pydantic models and schemas."""

# from datetime import datetime
# from typing import Any, Optional

# from pydantic import BaseModel, Field


# class HealthResponse(BaseModel):
#     """Health check response model."""

#     status: str = Field(..., description="Application status")
#     timestamp: datetime = Field(..., description="Timestamp of the health check")
#     version: str = Field(..., description="Application version")


# class ErrorResponse(BaseModel):
#     """Error response model."""

#     error: str = Field(..., description="Error message")
#     detail: Optional[str] = Field(None, description="Detailed error information")
#     timestamp: datetime = Field(..., description="Timestamp of the error")


# class GenerateTextRequest(BaseModel):
#     """Text generation request model."""

#     prompt: str = Field(
#         ..., description="Text prompt for generation", min_length=1, max_length=1000
#     )
#     max_length: Optional[int] = Field(
#         50, description="Maximum length of generated text", ge=1, le=500
#     )
#     temperature: Optional[float] = Field(
#         1.0, description="Temperature for text generation", ge=0.1, le=2.0
#     )


# class GenerateTextResponse(BaseModel):
#     """Text generation response model."""

#     generated_text: str = Field(..., description="Generated text")
#     input_prompt: str = Field(..., description="Original input prompt")
#     metadata: dict[str, Any] = Field(
#         default_factory=dict, description="Additional metadata"
#     )


# class WeatherRequest(BaseModel):
#     """Weather request model."""

#     city: str = Field(..., description="City name", min_length=1, max_length=100)
#     country_code: Optional[str] = Field(
#         None, description="ISO 3166 country code", min_length=2, max_length=2
#     )


# class WeatherResponse(BaseModel):
#     """Weather response model."""

#     city: str = Field(..., description="City name")
#     country: str = Field(..., description="Country name")
#     temperature: float = Field(..., description="Temperature in Celsius")
#     description: str = Field(..., description="Weather description")
#     humidity: Optional[int] = Field(None, description="Humidity percentage")
#     wind_speed: Optional[float] = Field(None, description="Wind speed in m/s")


# class QuoteResponse(BaseModel):
#     """Random quote response model."""

#     quote: str = Field(..., description="Quote text")
#     author: str = Field(..., description="Quote author")
#     category: Optional[str] = Field(None, description="Quote category")


# class FactResponse(BaseModel):
#     """Random fact response model."""

#     fact: str = Field(..., description="Interesting fact")
#     source: Optional[str] = Field(None, description="Fact source")
