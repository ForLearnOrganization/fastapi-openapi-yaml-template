"""外部APIエンドポイント"""

import logging

from fastapi import APIRouter, HTTPException

from app.models import FactResponse, QuoteResponse, WeatherRequest, WeatherResponse
from app.services.external_service import ExternalAPIService

router = APIRouter()
external_service = ExternalAPIService()
logger = logging.getLogger(__name__)


@router.post("/weather", response_model=WeatherResponse)
async def get_weather(request: WeatherRequest):
    """
    都市の天気情報を取得します。

    現在の環境では外部APIアクセスが制限される可能性があるため、
    このエンドポイントはモック天気データを提供します。
    """
    try:
        result = await external_service.get_weather(request.city, request.country_code)
        return result
    except Exception as e:
        logger.error(f"天気API呼び出しに失敗しました: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"天気データが利用できません: {str(e)}"
        )


@router.get("/quote", response_model=QuoteResponse)
async def get_random_quote():
    """
    ランダムな名言を取得します。

    厳選されたコレクションからランダムな名言を返します。
    """
    try:
        result = await external_service.get_random_quote()
        return result
    except Exception as e:
        logger.error(f"名言API呼び出しに失敗しました: {str(e)}")
        raise HTTPException(status_code=500, detail=f"名言が利用できません: {str(e)}")


@router.get("/fact", response_model=FactResponse)
async def get_random_fact():
    """
    ランダムな興味深い豆知識を取得します。

    ランダムな教育的事実を返します。
    """
    try:
        result = await external_service.get_random_fact()
        return result
    except Exception as e:
        logger.error(f"豆知識API呼び出しに失敗しました: {str(e)}")
        raise HTTPException(status_code=500, detail=f"豆知識が利用できません: {str(e)}")


@router.get("/joke", response_model=dict)
async def get_random_joke():
    """
    ランダムなプログラミングジョークを取得します。

    ランダムなプログラミング関連のジョークを返します。
    """
    try:
        result = await external_service.get_random_joke()
        return result
    except Exception as e:
        logger.error(f"ジョークAPI呼び出しに失敗しました: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"ジョークが利用できません: {str(e)}"
        )
