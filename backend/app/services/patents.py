import logging
from pathlib import Path
from typing import List

from dotenv import load_dotenv

from ..core.config import settings
from ..core.llm import build_messages, extract
from ..core.logging import setup_logging
from ..core.ocr import DocumentStream, OCROutput, get_pdf_content
from ..prompts.prompt_manager import get_prompt
from ..schemas.patents import (
    PatentContent,
    PatentContradiction,
    PatentDocument,
    PatentMeta,
)
from ..utils import Base64Image

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)
type PatentInput = Path | str | DocumentStream

# ------------------------------------------
# Helper functions
# ------------------------------------------


def _get_patent_metadata(titlepage: Base64Image, model: str, provider: str) -> PatentMeta:
    logger.info("Starting patent metadata extraction from title page image")
    prompt = get_prompt("PatentMetaParser")
    logger.info(f"Using prompt: {prompt.name}, version: {prompt.version}")
    messages = build_messages(
        provider=provider,
        text="Extract the patent metadata from this image.",
        image_path=titlepage,
        system_prompt=prompt.compile(),
    )
    try:
        response = extract(
            model=model,
            messages=messages,
            schema=PatentMeta,
            provider=provider,
        )
        logger.info("Patent metadata extraction completed successfully")
        return response
    except Exception as e:
        logger.error(f"Failed to extract patent metadata: {e}")
        raise RuntimeError(f"Provider '{provider}' may not support vision. Error: {e}")


def _get_patent_content(ocr_source: str, model: str, provider: str) -> PatentContent:
    logger.info("Starting patent content extraction from OCR text")
    prompt = get_prompt("PatentContentParser")
    logger.info(f"Using prompt: {prompt.name}, version: {prompt.version}")
    messages = build_messages(
        provider=provider,
        text=f"Extract the patent content from this text: \n\n{ocr_source}",
        system_prompt=prompt.compile(),
    )
    try:
        response = extract(
            model=model,
            messages=messages,
            schema=PatentContent,
            provider=provider,
        )
        logger.info("Patent content extraction completed successfully")
        return response
    except Exception as e:
        logger.error(f"Failed to extract patent content: {e}")
        raise RuntimeError(f"Content extraction failed: {e}")


# ------------------------------------------
# Patent Data Extraction Pipeline
# ------------------------------------------


def parse_patent_data(source: PatentInput) -> PatentDocument:
    logger.info(f"Starting patent data extraction pipeline for: {source}")
    ocr_output: OCROutput = get_pdf_content(source)
    model = settings.DEFAULT_MODEL
    provider = settings.DEFAULT_PROVIDER
    logger.info(f"Using LLM model: {model} from provider: {provider}")
    metadata = _get_patent_metadata(ocr_output.titlepage, model=model, provider=provider)
    patent_content = _get_patent_content(ocr_output.content, model=model, provider=provider)
    logger.info(f"Patent data extraction completed. Patent: {metadata.patent_no}")
    return PatentDocument(meta=metadata, content=patent_content)


def extract_patent_tc(
    source: PatentDocument, model: str, provider: str
) -> List[PatentContradiction]:
    """Extract technical contradictions from patent content."""

    # Build patent content as multiline string for the prompt
    patent_text = f"""
    Title: {source.meta.title}\n
    Abstract: {source.meta.abstract}\n
    Description: {source.content.description}\n
    """

    prompt = get_prompt("extract_tc_from_text")
    messages = build_messages(
        provider=provider,
        text=patent_text,
        system_prompt=prompt.compile(),
    )
    try:
        response = extract(
            model=model,
            messages=messages,
            schema=List[PatentContradiction],
            provider=provider,
        )
        logger.info("Patent TC extraction completed successfully")
        return response
    except Exception as e:
        logger.error(f"Failed to extract patent TC: {e}")
        raise RuntimeError(f"TC extraction failed: {e}")


def patent_tc_pipeline(source: PatentInput, model: str, provider: str) -> PatentDocument:
    """Complete pipeline to extract technical contradictions from a patent source."""
    logger.info(f"Starting patent TC extraction pipeline for source: {source}")
    patent_doc = parse_patent_data(source)
    patent_tc = extract_patent_tc(patent_doc, model=model, provider=provider)
    logger.info(f"Patent TC extraction pipeline completed for patent: {patent_doc.meta.patent_no}")
    return PatentDocument(
        meta=patent_doc.meta,
        content=patent_doc.content,
        contradictions=patent_tc,
    )
