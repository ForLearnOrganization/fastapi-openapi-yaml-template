"""External API endpoints."""

from fastapi import APIRouter, HTTPException
from app.models import WeatherRequest, WeatherResponse, QuoteResponse, FactResponse
from app.services.external_service import ExternalAPIService
import logging

router = APIRouter()
external_service = ExternalAPIService()
logger = logging.getLogger(__name__)


@router.post("/weather", response_model=WeatherResponse)
async def get_weather(request: WeatherRequest):
    """
    Get weather information for a city.
    
    This endpoint provides mock weather data since external API access 
    may be limited in the current environment.
    """
    try:
        result = await external_service.get_weather(request.city, request.country_code)
        return result
    except Exception as e:
        logger.error(f"Weather API call failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Weather data unavailable: {str(e)}")


@router.get("/quote", response_model=QuoteResponse)
async def get_random_quote():
    """
    Get a random inspirational quote.
    
    Returns a random quote from a curated collection.
    """
    try:
        result = await external_service.get_random_quote()
        return result
    except Exception as e:
        logger.error(f"Quote API call failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Quote unavailable: {str(e)}")


@router.get("/fact", response_model=FactResponse)
async def get_random_fact():
    """
    Get a random interesting fact.
    
    Returns a random educational fact.
    """
    try:
        result = await external_service.get_random_fact()
        return result
    except Exception as e:
        logger.error(f"Fact API call failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Fact unavailable: {str(e)}")


@router.get("/joke", response_model=dict)
async def get_random_joke():
    """
    Get a random programming joke.
    
    Returns a random programming-related joke.
    """
    try:
        result = await external_service.get_random_joke()
        return result
    except Exception as e:
        logger.error(f"Joke API call failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Joke unavailable: {str(e)}")