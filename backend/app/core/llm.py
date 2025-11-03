import logging
from pathlib import Path
from typing import Any, Callable, Optional, Protocol, Type

import instructor
from anthropic import Anthropic
from openai import OpenAI
from pydantic import BaseModel

from ..utils import (
    Base64Image,
    encode_image,
    format_anthropic_image_content,
    format_openai_image_content,
    load_image,
)
from .config import settings

logger = logging.getLogger(__name__)


type LLMClient = OpenAI | Anthropic
type CompletionFunc = Callable[[LLMClient, dict], str]


class ChatModelProtocol(Protocol):
    def build_messages(
        self,
        text: str,
        image_path: Optional[Path | str] = None,
        system_prompt: Optional[str] = None,
    ) -> list[dict]: ...

    def chat(self, messages: list[dict], **kwargs) -> str: ...

    def extract(self, messages: list[dict], schema: Type[BaseModel], **kwargs) -> Any: ...


# ------------------------------------------------------------------------------
# Chatter function
# ------------------------------------------------------------------------------


def chatter(client: LLMClient) -> CompletionFunc:
    def get_openai_completion(client: OpenAI, completion_params: dict) -> str:
        try:
            logger.info(f"Calling OpenAI API with model: {completion_params.get('model')}")
            completion = client.chat.completions.create(**completion_params)
            logger.info("OpenAI API call successful")
            return completion.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI completion failed: {e}")
            raise RuntimeError(f"OpenAI completion failed: {e}")

    def get_anthropic_completion(client: Anthropic, completion_params: dict) -> str:
        try:
            params = completion_params.copy()
            messages = params.pop("messages")

            if messages and messages[0]["role"] == "system":
                params["system"] = messages[0]["content"]
                messages = messages[1:]

            logger.info(f"Calling Anthropic API with model: {params.get('model')}")
            completion = client.messages.create(messages=messages, **params)
            logger.info("Anthropic API call successful")
            return completion.content[0].text
        except Exception as e:
            logger.error(f"Anthropic completion failed: {e}")
            raise RuntimeError(f"Anthropic completion failed: {e}")

    if isinstance(client, OpenAI):
        return get_openai_completion
    elif isinstance(client, Anthropic):
        return get_anthropic_completion
    else:
        logger.error(f"Unsupported client type: {type(client)}")
        raise ValueError(f"Unsupported client type: {type(client)}")


# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------


def get_client(provider: str) -> LLMClient:
    provider_settings = getattr(settings, provider)

    client_initializers = {
        "openai": lambda s: OpenAI(api_key=s.api_key),
        "ollama": lambda s: OpenAI(base_url=s.base_url, api_key=s.api_key),
        "groq": lambda s: OpenAI(base_url=s.base_url, api_key=s.api_key),
        "perplexity": lambda s: OpenAI(base_url=s.base_url, api_key=s.api_key),
        "lmstudio": lambda s: OpenAI(base_url=s.base_url, api_key=s.api_key),
        "anthropic": lambda s: Anthropic(api_key=s.api_key),
        "together": lambda s: OpenAI(base_url=s.base_url, api_key=s.api_key),
    }

    initializer = client_initializers.get(provider)
    if initializer:
        logger.info(f"Initializing {provider} client")
        return initializer(provider_settings)
    logger.error(f"Unsupported LLM provider: {provider}")
    raise ValueError(f"Unsupported LLM provider: {provider}")


def build_messages(
    provider: str,
    text: str,
    image_path: Optional[Path | Base64Image] = None,
    system_prompt: Optional[str] = None,
) -> list[dict]:
    """Build messages for LLM API calls.

    Args:
        provider: The LLM provider (e.g., 'openai', 'anthropic', 'groq')
        text: The text content of the message
        image_path: Optional image - either a Path to an image file or a base64-encoded string
        system_prompt: Optional system prompt

    Returns:
        List of message dictionaries formatted for the specified provider
    """

    messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
    if not image_path:
        messages.append({"role": "user", "content": text})
    else:
        # Convert image to (media_type, base64) tuple
        if isinstance(image_path, Path):
            image_tuple = encode_image(load_image(image_path))
        else:
            image_tuple = image_path

        # Format for provider
        if provider == "anthropic":
            content = format_anthropic_image_content(text, image_tuple)
        else:
            content = format_openai_image_content(text, image_tuple)
        messages.append({"role": "user", "content": content})
    return messages


# ------------------------------------------------------------------------------
# Completion functions
# ------------------------------------------------------------------------------


def chat(messages: list[dict], model: str, provider: str, **kwargs) -> str:
    logger.debug(f"Starting chat with model: {model}, provider: {provider}")
    provider_settings = getattr(settings, provider)
    client = get_client(provider)

    completion_params = {
        "model": model,
        "temperature": kwargs.get("temperature", provider_settings.temperature),
        "top_p": kwargs.get("top_p", provider_settings.top_p),
        "max_tokens": kwargs.get("max_tokens", provider_settings.max_tokens),
        "messages": messages,
    }

    completion_func = chatter(client)
    return completion_func(client, completion_params)


def extract(
    messages: list[dict],
    schema: Type[BaseModel],
    model: str,
    provider: str,
    **kwargs,
) -> Any:
    logger.debug(
        f"Starting extraction with model: {model}, provider: {provider}, schema: {schema.__name__}"
    )
    provider_settings = getattr(settings, provider)
    client = get_client(provider)

    completion_params = {
        "model": model,
        "temperature": kwargs.get("temperature", provider_settings.temperature),
        "top_p": kwargs.get("top_p", provider_settings.top_p),
        "max_tokens": kwargs.get("max_tokens", provider_settings.max_tokens),
        "messages": messages,
    }

    if isinstance(client, OpenAI):
        mode = instructor.Mode.TOOLS if provider != "ollama" else instructor.Mode.JSON
        patched_client = instructor.from_openai(client, mode=mode)
    elif isinstance(client, Anthropic):
        patched_client = instructor.from_anthropic(client)
    else:
        logger.error(f"Unsupported client for patching: {type(client)}")
        raise ValueError(f"Unsupported client for patching: {type(client)}")

    return patched_client.chat.completions.create(response_model=schema, **completion_params)


# ------------------------------------------------------------------------------
# LLMSuite Factory
# ------------------------------------------------------------------------------


def init_chat_model(
    model: Optional[str] = None, provider: Optional[str] = None
) -> ChatModelProtocol:
    provider = provider or settings.DEFAULT_PROVIDER
    if not provider:
        raise ValueError("Provider must be specified or set in DEFAULT_PROVIDER env variable.")
    model = model or settings.DEFAULT_MODEL
    if not model:
        raise ValueError("Model must be specified or set in DEFAULT_MODEL env variable.")

    logger.debug(f"Initializing chat model with provider: {provider}, model: {model}")

    class ChatModel:
        def __init__(self, provider: str, model: str):
            self._provider = provider
            self._model = model

        def build_messages(
            self,
            text: str,
            image_path: Optional[Path | str] = None,
            system_prompt: Optional[str] = None,
        ) -> list[dict]:
            return build_messages(self._provider, text, image_path, system_prompt)

        def chat(self, messages: list[dict], **kwargs) -> str:
            return chat(messages, self._model, self._provider, **kwargs)

        def extract(self, messages: list[dict], schema: Type[BaseModel], **kwargs) -> Any:
            return extract(messages, schema, self._model, self._provider, **kwargs)

    return ChatModel(provider, model)
