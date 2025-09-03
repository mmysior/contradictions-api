from typing import List

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.principles import Principle, ScoredPrinciple
from app.services import principles as principles_service

router = APIRouter(
    prefix="/principles",
    tags=["principles"],
)


@router.get(
    "/",
    response_model=List[Principle],
    status_code=status.HTTP_200_OK,
)
def get_all_principles() -> List[Principle]:
    """Get all TRIZ inventive principles."""
    try:
        return principles_service.get_all_principles()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get principles: {str(e)}",
        )


@router.get(
    "/search",
    response_model=List[ScoredPrinciple],
    status_code=status.HTTP_200_OK,
)
def search_principles(
    q: str = Query(..., description="Search query"),
    limit: int = Query(1, description="Number of results to return", ge=1, le=40),
) -> List[ScoredPrinciple]:
    """Search TRIZ inventive principles by semantic similarity."""
    try:
        results = principles_service.search_principles(q, limit)
        return [ScoredPrinciple(principle=prin, score=score) for prin, score in results]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search principles: {str(e)}",
        )


@router.get(
    "/by-name/{principle_name}",
    response_model=Principle,
    status_code=status.HTTP_200_OK,
)
def get_principle_by_name(principle_name: str) -> Principle:
    """Get a specific TRIZ inventive principle by name."""
    try:
        return principles_service.get_principle_by_name(principle_name)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/random",
    response_model=List[Principle],
    status_code=status.HTTP_200_OK,
)
def get_random_principles(
    limit: int = Query(5, description="Number of random principles to return", ge=1, le=40),
) -> List[Principle]:
    """Get a specified number of random TRIZ inventive principles."""
    try:
        return principles_service.get_random_principles(limit)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get random principles: {str(e)}",
        )


@router.get(
    "/matrix",
    response_model=List[Principle],
    status_code=status.HTTP_200_OK,
)
def lookup_principles_from_matrix(
    improving: List[int] = Query(..., description="List of improving parameter IDs"),
    preserving: List[int] = Query(..., description="List of preserving parameter IDs"),
) -> List[Principle]:
    """Get inventive principles from TRIZ contradiction matrix based on parameter pairs."""
    try:
        principles = principles_service.get_principles_from_matrix(improving, preserving)
        return principles
    except (TypeError, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to lookup principles: {str(e)}",
        )


@router.get(
    "/{principle_id}",
    response_model=Principle,
    status_code=status.HTTP_200_OK,
)
def get_principle_by_id(principle_id: int) -> Principle:
    """Get a specific TRIZ inventive principle by ID."""
    try:
        return principles_service.get_principle_by_id(principle_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
