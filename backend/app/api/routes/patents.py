import logging
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from ...core.config import settings
from ...schemas.patents import PatentDocument, PatentUrlRequest
from ...services import patents as patents_service

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/patents",
    tags=["patents"],
)


@router.post(
    "/extract-tc/upload",
    response_model=PatentDocument,
    status_code=status.HTTP_200_OK,
)
def extract_tc_from_upload(
    file: UploadFile = File(..., description="Patent PDF file to upload"),
) -> PatentDocument:
    """Extract technical contradictions from an uploaded patent PDF file.

    Upload a PDF file containing patent information, and receive a list of
    technical contradictions extracted from the document.
    """
    logger.info(f"Processing uploaded file: {file.filename}")

    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            content = file.file.read()
            tmp_file.write(content)
            tmp_path = Path(tmp_file.name)

        try:
            result = patents_service.patent_tc_pipeline(
                source=tmp_path,
                model=settings.DEFAULT_MODEL,
                provider=settings.DEFAULT_PROVIDER,
            )
            return result
        finally:
            # Clean up temporary file
            tmp_path.unlink(missing_ok=True)

    except Exception as e:
        logger.error(f"Failed to extract contradictions from uploaded file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract contradictions from uploaded file: {str(e)}",
        )


@router.post(
    "/extract-tc/from-url",
    response_model=PatentDocument,
    status_code=status.HTTP_200_OK,
)
def extract_tc_from_url(
    request: PatentUrlRequest,
) -> PatentDocument:
    """Extract technical contradictions from a patent PDF available at a URL.

    Provide a URL to a PDF file containing patent information, and receive a list
    of technical contradictions extracted from the document.
    """
    logger.info(f"Processing patent from URL: {request.url}")

    try:
        result = patents_service.patent_tc_pipeline(
            source=request.url,
            model=settings.DEFAULT_MODEL,
            provider=settings.DEFAULT_PROVIDER,
        )
        return result

    except Exception as e:
        logger.error(f"Failed to extract contradictions from URL: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to extract contradictions from URL: {str(e)}",
        )


# @router.post(
#     "/classify",
#     response_model=List[ScoredPrinciple],
#     status_code=status.HTTP_200_OK,
# )
# def classify_patent_solutions(
#     patent: PatentClassificationInput,
#     limit: int = Query(10, description="Maximum number of principles to return", ge=1, le=40),
# ) -> List[ScoredPrinciple]:
#     """Classify patent solutions to TRIZ inventive principles with relevance scores."""
#     logger.info(f"Classifying patent solutions (limit={limit})")
#     try:
#         result = classify_patent_to_principles(
#             patent,
#             model=settings.DEFAULT_MODEL,
#             provider=settings.DEFAULT_PROVIDER,
#             max_principles=limit,
#         )
#         logger.info(f"Classified patent to {len(result)} principles")
#         return result
#     except Exception as e:
#         logger.error(f"Failed to classify patent solutions: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Failed to classify patent solutions: {str(e)}",
#         )
