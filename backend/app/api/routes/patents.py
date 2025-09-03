from typing import List

from fastapi import APIRouter, HTTPException, Query, status

from app.core.config import settings
from app.schemas.contradictions import TechnicalContradiction
from app.schemas.patents import PatentClassificationInput, PatentContent
from app.schemas.principles import ScoredPrinciple
from app.services.patents import classify_patent_to_principles, extract_patent_contradictions

router = APIRouter(
    prefix="/patents",
    tags=["patents"],
)


@router.post(
    "/extract",
    response_model=List[TechnicalContradiction],
    status_code=status.HTTP_200_OK,
)
def extract_contradictions_from_patent(
    patent: PatentContent,
    limit: int = Query(3, description="Maximum number of parameters to assign per effect", ge=1, le=10)
) -> List[TechnicalContradiction]:
    """Extract technical contradictions from patent content."""
    try:
        return extract_patent_contradictions(
            patent,
            model=settings.DEFAULT_MODEL,
            provider=settings.DEFAULT_PROVIDER,
            max_parameters=limit,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract contradictions from patent: {str(e)}",
        )


@router.post(
    "/classify",
    response_model=List[ScoredPrinciple],
    status_code=status.HTTP_200_OK,
)
def classify_patent_solutions(
    patent: PatentClassificationInput,
    limit: int = Query(10, description="Maximum number of principles to return", ge=1, le=40)
) -> List[ScoredPrinciple]:
    """Classify patent solutions to TRIZ inventive principles with relevance scores."""
    try:
        return classify_patent_to_principles(
            patent,
            model=settings.DEFAULT_MODEL,
            provider=settings.DEFAULT_PROVIDER,
            max_principles=limit,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to classify patent solutions: {str(e)}",
        )