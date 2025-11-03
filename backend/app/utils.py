import base64
import json
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Literal

from PIL import Image

from .core.config import settings
from .schemas.parameters import Parameter
from .schemas.principles import Principle

type MessageRole = Literal["system", "user", "assistant"]
type Base64Image = tuple[str, str]


def load_json_data(file_path: str) -> dict:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_parameters() -> List[Parameter]:
    parameters_data = load_json_data(str(settings.PARAMETERS_FILE_PATH))
    return [Parameter(**p) for p in parameters_data["parameters"]]


def get_principles() -> List[Principle]:
    principles_data = load_json_data(str(settings.PRINCIPLES_FILE_PATH))
    return [Principle(**p) for p in principles_data]


# LLM utility functions
def load_image(image_path: Path, max_size: tuple[int, int] = (1024, 1024)) -> Image.Image:
    """Load an image from path and resize it.

    Args:
        image_path: Path to the image file
        max_size: Maximum dimensions for the image (width, height)

    Returns:
        PIL Image object
    """
    img = Image.open(image_path)
    img.thumbnail(max_size)
    return img


def encode_image(image: Image.Image, quality: int = 85) -> Base64Image:
    """Encode a PIL Image to base64 PNG.

    Args:
        image: PIL Image object
        quality: Quality setting for PNG optimization

    Returns:
        Tuple of (media_type, base64_string)
    """
    buffer = BytesIO()
    image.save(buffer, format="PNG", quality=quality, optimize=True)
    base64_string = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return ("image/png", base64_string)


def format_openai_image_content(text: str, image: tuple[str, str]) -> List[Dict[str, Any]]:
    """Format message content with image for OpenAI-compatible APIs.

    Args:
        text: The text content of the message
        image: Tuple of (media_type, base64_string)

    Returns:
        List of content dictionaries for OpenAI message format
    """
    media_type, base64_data = image
    image_url = f"data:{media_type};base64,{base64_data}"

    return [
        {"type": "text", "text": text},
        {
            "type": "image_url",
            "image_url": {"url": image_url},
        },
    ]


def format_anthropic_image_content(text: str, image: tuple[str, str]) -> List[Dict[str, Any]]:
    """Format message content with image for Anthropic API.

    Args:
        text: The text content of the message
        image: Tuple of (media_type, base64_string)

    Returns:
        List of content dictionaries for Anthropic message format
    """
    media_type, base64_data = image

    return [
        {"type": "text", "text": text},
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": base64_data,
            },
        },
    ]
