from fastapi import APIRouter, HTTPException, status

from app.logger import get_logger
from app.models.schemas import TranslateRequest, TranslateResponse
from app.services.groq_service import groq_service

router = APIRouter(prefix="/translate", tags=["Translate"])
logger = get_logger(__name__)


@router.post(
    "/",
    response_model=TranslateResponse,
    status_code=status.HTTP_200_OK,
    summary="Translate Text",
    description="Translate text from one language to another. Set source_language to 'auto' for automatic detection.",
    responses={
        200: {"description": "Text translated successfully"},
        400: {"description": "Bad request - invalid language"},
        422: {"description": "Validation error - check your request body"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "AI service unavailable"},
    },
)
async def translate_text(request: TranslateRequest) -> TranslateResponse:
    """Handle POST /translate request. Validates input and returns translated text."""
    logger.info("Received translate request: target language = %s", request.target_language)
    if not request.target_language.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="target_language cannot be empty",
        )
    try:
        result = groq_service.translate(
            text=request.text,
            source_language=request.source_language,
            target_language=request.target_language,
        )
        return TranslateResponse(**result)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Unexpected error in translate endpoint: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from exc
