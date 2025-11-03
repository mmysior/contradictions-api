import logging

from fastapi import APIRouter, HTTPException, Query, status

from app.services import contradictions as contradictions_service

from ...core.config import settings
from ...schemas.contradictions import TContradictions, TextInput

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/contradictions",
    tags=["contradictions"],
)


# ================================================================================================
# Technical Contradictions
# ================================================================================================


@router.post(
    "/extract-tc",
    response_model=TContradictions,
    status_code=status.HTTP_200_OK,
)
def extract_technical_contradiction(text_input: TextInput) -> TContradictions:
    """Extract technical contradiction from text description."""
    logger.info(
        f"Extracting technical contradictions (text_length={len(text_input.description)})"
    )
    try:
        result = contradictions_service.extract_tc(
            text_input.description,
            model=settings.DEFAULT_MODEL,
            provider=settings.DEFAULT_PROVIDER,
        )
        logger.info(
            f"Successfully extracted {len(result.contradictions)} technical contradictions"
        )
        return result
    except Exception as e:
        logger.error(f"Failed to extract technical contradiction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract technical contradiction: {str(e)}",
        )


@router.post(
    "/solve-tc",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
def solve_technical_contradiction():
    """Solve technical contradiction."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Technical contradiction solving not yet implemented",
    )


# ================================================================================================
# Physical Contradictions
# ================================================================================================

# Not implemented yet
