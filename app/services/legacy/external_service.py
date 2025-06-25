"""External API service for calling third-party APIs."""

import asyncio
import random
from typing import Optional

from fastapi import HTTPException

from app.generated.generated_models import (
    FactResponse,
    JokeResponse,
    QuoteResponse,
    WeatherRequest,
    WeatherResponse,
)


class ExternalAPIService:
    """Service for handling external API calls."""

    def __init__(self):
        # Mock data for when external APIs are not available
        self.mock_quotes = [
            {
                "quote": "The only way to do great work is to love what you do.",
                "author": "Steve Jobs",
                "category": "motivation",
            },
            {
                "quote": "Innovation distinguishes between a leader and a follower.",
                "author": "Steve Jobs",
                "category": "innovation",
            },
            {
                "quote": "Code is like humor. When you have to explain it, it's bad.",
                "author": "Cory House",
                "category": "programming",
            },
            {
                "quote": "First, solve the problem. Then, write the code.",
                "author": "John Johnson",
                "category": "programming",
            },
            {
                "quote": "Experience is the name everyone gives to their mistakes.",
                "author": "Oscar Wilde",
                "category": "wisdom",
            },
            {
                "quote": "In order to be irreplaceable, one must always be different.",
                "author": "Coco Chanel",
                "category": "uniqueness",
            },
            {
                "quote": (
                    "The best time to plant a tree was 20 years ago. "
                    "The second best time is now."
                ),
                "author": "Chinese Proverb",
                "category": "action",
            },
        ]

        self.mock_facts = [
            {
                "fact": (
                    "Honey never spoils. Archaeologists have found pots of honey "
                    "in ancient Egyptian tombs that are over 3,000 years old and "
                    "still edible."
                ),
                "source": "archaeology",
            },
            {
                "fact": "Octopuses have three hearts and blue blood.",
                "source": "marine biology",
            },
            {
                "fact": "A single cloud can weigh more than a million pounds.",
                "source": "meteorology",
            },
            {
                "fact": (
                    "There are more possible games of chess than atoms "
                    "in the observable universe."
                ),
                "source": "mathematics",
            },
            {
                "fact": "Bananas are berries, but strawberries aren't.",
                "source": "botany",
            },
            {
                "fact": "A group of flamingos is called a 'flamboyance'.",
                "source": "zoology",
            },
            {
                "fact": (
                    "The Great Wall of China isn't visible from space "
                    "with the naked eye."
                ),
                "source": "geography",
            },
        ]

        self.mock_jokes = [
            {
                "joke": (
                    "Why do programmers prefer dark mode? Because light attracts bugs!"
                ),
                "category": "programming",
            },
            {
                "joke": (
                    "How many programmers does it take to change a light bulb? "
                    "None, that's a hardware problem."
                ),
                "category": "programming",
            },
            {
                "joke": "Why did the programmer quit his job? He didn't get arrays.",
                "category": "programming",
            },
            {
                "joke": "What's a programmer's favorite hangout place? Foo Bar.",
                "category": "programming",
            },
            {
                "joke": (
                    "Why do Python programmers prefer snakes? "
                    "Because they're easy to wrap around your finger!"
                ),
                "category": "programming",
            },
        ]

    async def get_weather(
        self, city: str, country_code: Optional[str] = None
    ) -> WeatherResponse:
        """
        Get weather information for a city.

        In a real implementation, this would call a weather API like OpenWeatherMap.
        For now, we return mock data.
        """
        # Simulate API call delay
        await asyncio.sleep(0.1)

        # Generate mock weather data
        temperature = random.uniform(-10, 35)
        descriptions = [
            "Sunny",
            "Cloudy",
            "Rainy",
            "Partly cloudy",
            "Clear sky",
            "Light rain",
            "Overcast",
        ]
        description = random.choice(descriptions)

        return WeatherResponse(
            city=city.title(),
            temperature=round(temperature, 1),
            humidity=random.randint(30, 90),
            description=description,
            is_mock=True,
        )

    async def get_random_quote(self) -> QuoteResponse:
        """Get a random inspirational quote."""
        await asyncio.sleep(0.05)

        quote_data = random.choice(self.mock_quotes)
        return QuoteResponse(
            quote=quote_data["quote"],
            author=quote_data["author"],
            category=quote_data.get("category"),
        )

    async def get_random_fact(self) -> FactResponse:
        """Get a random interesting fact."""
        await asyncio.sleep(0.05)

        fact_data = random.choice(self.mock_facts)
        return FactResponse(fact=fact_data["fact"], source=fact_data.get("source"))

    async def get_random_joke(self) -> dict:
        """Get a random programming joke."""
        await asyncio.sleep(0.05)

        joke_data = random.choice(self.mock_jokes)
        return {
            "joke": joke_data["joke"],
            "category": joke_data.get("category", "general"),
            "type": "programming_humor",
        }


# Global service instance
external_service = ExternalAPIService()


async def post_external_weather(request: WeatherRequest) -> WeatherResponse:
    """天気情報取得エンドポイント用のサービス関数"""
    try:
        result = await external_service.get_weather(city=request.city)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"天気情報の取得に失敗しました: {str(e)}"
        )


async def get_external_quote() -> QuoteResponse:
    """名言取得エンドポイント用のサービス関数"""
    try:
        result = await external_service.get_random_quote()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"名言の取得に失敗しました: {str(e)}"
        )


async def get_external_fact() -> FactResponse:
    """豆知識取得エンドポイント用のサービス関数"""
    try:
        result = await external_service.get_random_fact()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"豆知識の取得に失敗しました: {str(e)}"
        )


async def get_external_joke() -> JokeResponse:
    """ジョーク取得エンドポイント用のサービス関数"""
    try:
        joke_data = await external_service.get_random_joke()
        return JokeResponse(
            joke=joke_data["joke"], type=joke_data.get("category", "programming")
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"ジョークの取得に失敗しました: {str(e)}"
        )
