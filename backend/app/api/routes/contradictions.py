from typing import List

from fastapi import APIRouter, HTTPException, Query, status

from app.core.config import settings
from app.schemas.contradictions import TechnicalContradiction, TextInput
from app.services.contradictions import extract_tc

router = APIRouter(
    prefix="/contradictions",
    tags=["contradictions"],
)


# ================================================================================================
# Technical Contradictions
# ================================================================================================


@router.post(
    "/extract-tc",
    response_model=List[TechnicalContradiction],
    status_code=status.HTTP_200_OK,
)
def extract_technical_contradiction(
    text_input: TextInput,
    limit: int = Query(3, description="Maximum number of parameters to assign per effect", ge=1, le=10)
) -> List[TechnicalContradiction]:
    """Extract technical contradiction from text description."""
    try:
        return extract_tc(
            text_input.description,
            model=settings.DEFAULT_MODEL,
            provider=settings.DEFAULT_PROVIDER,
            max_parameters=limit,
        )
    except Exception as e:
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
