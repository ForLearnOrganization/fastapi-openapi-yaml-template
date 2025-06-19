"""Text generation endpoints."""

from fastapi import APIRouter, HTTPException
from app.models import GenerateTextRequest, GenerateTextResponse
from app.services.text_service import TextService
import logging

router = APIRouter()
text_service = TextService()
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=GenerateTextResponse)
async def generate_text(request: GenerateTextRequest):
    """
    Generate text based on input prompt.
    
    This endpoint generates text using a simple rule-based approach
    since external model access is not available.
    """
    try:
        result = await text_service.generate_text(
            prompt=request.prompt,
            max_length=request.max_length or 50,
            temperature=request.temperature or 1.0
        )
        return result
    except Exception as e:
        logger.error(f"Text generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Text generation failed: {str(e)}")


@router.post("/echo", response_model=dict)
async def echo_text(request: GenerateTextRequest):
    """
    Echo back the input text with metadata.
    
    Simple endpoint that returns the input with some processing information.
    """
    return {
        "original_text": request.prompt,
        "character_count": len(request.prompt),
        "word_count": len(request.prompt.split()),
        "processed_at": "now",
        "settings": {
            "max_length": request.max_length,
            "temperature": request.temperature
        }
    }