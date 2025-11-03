import logging
from typing import List

from fastapi import APIRouter, HTTPException, Query, status

from app.schemas.parameters import Parameter, ScoredParameter
from app.services import parameters as parameters_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/parameters",
    tags=["parameters"],
)


@router.get(
    "/",
    response_model=List[Parameter],
    status_code=status.HTTP_200_OK,
)
def get_all_parameters() -> List[Parameter]:
    """Get all TRIZ parameters."""
    try:
        return parameters_service.get_all_parameters()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get parameters: {str(e)}",
        )


@router.get(
    "/search",
    response_model=List[ScoredParameter],
    status_code=status.HTTP_200_OK,
)
def search_parameters(
    q: str = Query(..., description="Search query"),
    limit: int = Query(1, description="Number of results to return", ge=1, le=39),
) -> List[ScoredParameter]:
    """Search TRIZ parameters by semantic similarity."""
    logger.info(f"Searching parameters (query='{q}', limit={limit})")
    try:
        results = parameters_service.search_parameters(q, limit)
        if len(results) == 1:
            logger.info(f"Found 1 parameter match (score={results[0][1]:.2f})")
        elif len(results) > 1:
            scores = [score for _, score in results]
            avg_score = sum(scores) / len(scores)
            logger.info(f"Found {len(results)} parameter matches (avg={avg_score:.2f}, range={min(scores):.2f}-{max(scores):.2f})")
        else:
            logger.info("Found 0 parameter matches")
        return [ScoredParameter(parameter=param, score=score) for param, score in results]
    except Exception as e:
        logger.error(f"Failed to search parameters: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search parameters: {str(e)}",
        )


@router.get(
    "/{parameter_id}",
    response_model=Parameter,
    status_code=status.HTTP_200_OK,
)
def get_parameter_by_id(parameter_id: int) -> Parameter:
    """Get a specific TRIZ parameter by ID."""
    logger.info(f"Getting parameter by ID: {parameter_id}")
    try:
        return parameters_service.get_parameter_by_id(parameter_id)
    except ValueError as e:
        logger.error(f"Parameter not found: {parameter_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
