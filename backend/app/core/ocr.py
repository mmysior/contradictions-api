import logging
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, DocumentStream, PdfFormatOption
from dotenv import load_dotenv
from PIL.Image import Image
from pydantic import BaseModel

from ..utils import Base64Image, encode_image
from .logging import setup_logging

load_dotenv()
setup_logging()

logger = logging.getLogger(__name__)


class OCROutput(BaseModel):
    file_name: str
    content: str
    titlepage: tuple[str, str]  # (media_type, base64_string)


def _get_pdf_converter(image_scale: float = 1.5) -> DocumentConverter:
    pipeline_options = PdfPipelineOptions(
        # OCR Options
        do_ocr=True,
        ocr_options=EasyOcrOptions(
            lang=["en"],
            force_full_page_ocr=False,
        ),
        # Image Options
        images_scale=image_scale,
        generate_page_images=True,
        generate_picture_images=False,
        generate_table_images=False,
        # VLM Options
        # do_picture_description=True,
        # picture_description_options=PictureDescriptionVlmOptions(
        #     repo_id="HuggingFaceTB/SmolVLM-256M-Instruct",
        #     prompt="Describe the image in three sentences. Be consise and accurate.",
        # ),
    )

    return DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)}
    )


def get_pdf_content(source: Path | str | DocumentStream) -> OCROutput:
    logger.info(f"Starting PDF content extraction for: {source}")
    converter: DocumentConverter = _get_pdf_converter(image_scale=2.0)
    logger.info("PDF converter initialized")
    name = source if isinstance(source, str) else "external"

    conv_res = converter.convert(source)
    logger.info("PDF conversion completed")

    md_content: str = conv_res.document.export_to_markdown()
    titlepage_image: Image = list(conv_res.document.pages.values())[0].image.pil_image
    titlepage: Base64Image = encode_image(titlepage_image)

    logger.info(f"OCR content extraction completed. Content length: {len(md_content)} characters")
    return OCROutput(file_name=name, content=md_content, titlepage=titlepage)
