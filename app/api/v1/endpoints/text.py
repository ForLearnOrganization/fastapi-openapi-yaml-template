"""テキスト生成エンドポイント"""

import logging

from fastapi import APIRouter, HTTPException

from app.models import GenerateTextRequest, GenerateTextResponse
from app.services.text_service import TextService

router = APIRouter()
text_service = TextService()
logger = logging.getLogger(__name__)


@router.post("/generate", response_model=GenerateTextResponse)
async def generate_text(request: GenerateTextRequest):
    """
    入力プロンプトに基づいてテキストを生成します。

    外部モデルアクセスが利用できないため、このエンドポイントでは
    シンプルなルールベースアプローチを使用してテキストを生成します。
    """
    try:
        result = await text_service.generate_text(
            prompt=request.prompt,
            max_length=request.max_length or 50,
            temperature=request.temperature or 1.0,
        )
        return result
    except Exception as e:
        logger.error(f"テキスト生成に失敗しました: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"テキスト生成に失敗しました: {str(e)}"
        )


@router.post("/echo", response_model=dict)
async def echo_text(request: GenerateTextRequest):
    """
    入力テキストをメタデータ付きでエコーバックします。

    処理情報と共に入力を返すシンプルなエンドポイントです。
    """
    return {
        "original_text": request.prompt,
        "character_count": len(request.prompt),
        "word_count": len(request.prompt.split()),
        "processed_at": "now",
        "settings": {
            "max_length": request.max_length,
            "temperature": request.temperature,
        },
    }
