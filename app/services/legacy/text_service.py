"""Text generation service."""

import random
import re
from datetime import datetime

from fastapi import HTTPException

from app.generated.generated_models import (
    EchoTextRequest,
    EchoTextResponse,
    GenerateTextRequest,
    GenerateTextResponse,
)


class TextService:
    """Service for text generation operations."""

    def __init__(self):
        # Sample text templates for generation
        self.templates = [
            "Based on your prompt '{prompt}', here are some thoughts: ",
            "Continuing from '{prompt}', we could explore: ",
            "Your idea about '{prompt}' reminds me of: ",
            "Building on '{prompt}', consider this: ",
            "In response to '{prompt}', I would suggest: ",
        ]

        self.continuations = [
            "the importance of creativity in problem-solving.",
            "how technology shapes our daily experiences.",
            "the value of continuous learning and adaptation.",
            "the interconnectedness of all things in nature.",
            "the power of collaboration and teamwork.",
            "the beauty found in simplicity and minimalism.",
            "the significance of sustainable practices.",
            "the impact of positive thinking on outcomes.",
            "the role of innovation in progress.",
            "the wisdom gained through diverse perspectives.",
        ]

    async def generate_text(
        self, prompt: str, max_length: int = 50, temperature: float = 1.0
    ) -> GenerateTextResponse:
        """
        Generate text based on input prompt.

        This is a simple rule-based text generator since we don't have
        access to external models in this environment.
        """
        # Select a random template and continuation
        template = random.choice(self.templates)
        continuation = random.choice(self.continuations)

        # Generate the text
        generated_part = template.format(prompt=prompt) + continuation

        # Respect max_length by truncating if necessary
        if len(generated_part) > max_length:
            generated_part = generated_part[: max_length - 3] + "..."

        # Add some metadata
        metadata = {
            "generation_method": "rule_based",
            "temperature_used": temperature,
            "max_length_requested": max_length,
            "actual_length": len(generated_part),
            "prompt_length": len(prompt),
        }

        return GenerateTextResponse(
            generated_text=generated_part, input_prompt=prompt, metadata=metadata
        )


# Global service instance
text_service = TextService()


async def post_text_generate(request: GenerateTextRequest) -> GenerateTextResponse:
    """テキスト生成エンドポイント用のサービス関数"""
    try:
        result = await text_service.generate_text(
            prompt=request.prompt,
            max_length=request.max_length or 100,
            temperature=request.temperature or 0.7,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"テキスト生成に失敗しました: {str(e)}"
        )


async def post_generate(request: GenerateTextRequest) -> GenerateTextResponse:
    """後方互換性エンドポイント用のサービス関数"""
    try:
        result = await text_service.generate_text(
            prompt=request.prompt,
            max_length=request.max_length or 100,
            temperature=request.temperature or 0.7,
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"テキスト生成に失敗しました: {str(e)}"
        )


async def post_text_echo(request: EchoTextRequest) -> EchoTextResponse:
    """テキストエコーと分析エンドポイント用のサービス関数"""
    # Simple text analysis
    text = request.text
    character_count = len(text)
    word_count = len(text.split())

    # Simple language detection (very basic)
    if re.search(r"[ひらがなカタカナ漢字]", text):
        language = "ja"
    elif re.search(r"[a-zA-Z]", text):
        language = "en"
    else:
        language = "unknown"

    # Simple sentiment analysis (keyword based)
    positive_words = ["good", "great", "excellent", "良い", "素晴らしい", "最高"]
    negative_words = ["bad", "terrible", "awful", "悪い", "最悪", "ひどい"]

    sentiment = "neutral"
    for word in positive_words:
        if word in text.lower():
            sentiment = "positive"
            break
    for word in negative_words:
        if word in text.lower():
            sentiment = "negative"
            break

    return EchoTextResponse(
        echo=text,
        analysis={
            "character_count": character_count,
            "word_count": word_count,
            "language": language,
            "sentiment": sentiment,
        },
        timestamp=datetime.now(),
    )
