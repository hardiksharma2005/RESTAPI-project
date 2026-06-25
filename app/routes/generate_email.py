from fastapi import APIRouter, HTTPException, status

from app.logger import get_logger
from app.models.schemas import GenerateEmailRequest, GenerateEmailResponse
from app.services.groq_service import groq_service

router = APIRouter(prefix="/generate-email", tags=["Generate Email"])
logger = get_logger(__name__)


@router.post(
    "/",
    response_model=GenerateEmailResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate Email",
    description="Generate a professional email based on context. Supports multiple tones and email types.",
    responses={
        200: {"description": "Email generated successfully"},
        422: {"description": "Validation error - check your request body"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Failed to parse AI response"},
        503: {"description": "AI service unavailable"},
    },
)
async def generate_email(request: GenerateEmailRequest) -> GenerateEmailResponse:
    """Handle POST /generate-email request. Returns AI-generated email subject and body."""
    logger.info(
        "Received email generation request: type=%s, tone=%s",
        request.email_type,
        request.tone,
    )
    try:
        result = groq_service.generate_email(
            context=request.context,
            tone=request.tone,
            recipient_name=request.recipient_name,
            sender_name=request.sender_name,
            email_type=request.email_type,
        )
        return GenerateEmailResponse(**result)
    except HTTPException:
        raise
    except Exception as exc:
        logger.error("Unexpected error in generate_email endpoint: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from exc
