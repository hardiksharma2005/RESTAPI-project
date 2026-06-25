from fastapi import APIRouter, HTTPException, status

from app.logger import get_logger
from app.models.schemas import SummarizeRequest, SummarizeResponse
from app.services.groq_service import groq_service

router = APIRouter(prefix="/summarize", tags=["Summarize"])
logger = get_logger(__name__)


@router.post(
    "/",
    response_model=SummarizeResponse,
    status_code=status.HTTP_200_OK,
    summary="Summarize Text",
    description="Summarize a long piece of text into a concise version using AI. Supports multiple languages.",
    responses={
        200: {"description": "Text summarized successfully"},
        422: {"description": "Validation error - check your request body"},
        429: {"description": "Rate limit exceeded"},
        503: {"description": "AI service unavailable"},
    },
)
async def summarize_text(request: SummarizeRequest) -> SummarizeResponse:
    """Handle POST /summarize request. Validates input and returns AI-generated summary."""
    logger.info("Received summarize request: %d characters", len(request.text))
    try:
        result = groq_service.summarize(
            text=request.text,
            max_length=request.max_length,
            language=request.language,
        )
        return SummarizeResponse(**result)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Unexpected error in summarize endpoint: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from exc
