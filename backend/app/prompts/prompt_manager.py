import logging
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, cast

import frontmatter
from jinja2 import Environment, FileSystemLoader, StrictUndefined
from pydantic import BaseModel, Field

from app.core.config import settings

logger = logging.getLogger(__name__)

# ------------------------------------------
# Pydantic Models
# ------------------------------------------


class TemplateMetadata(BaseModel):
    type: Literal["system", "developer", "user"] = "system"
    author: str = ""
    version: int = 1
    labels: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    config: Dict[str, Any] = Field(default_factory=dict)
    json_schema: Optional[Dict[str, Any]] = None


class PromptModel(TemplateMetadata):
    name: str
    prompt: str

    def compile(self, **kwargs) -> str:
        env = Environment(undefined=StrictUndefined, trim_blocks=True, lstrip_blocks=True)
        template = env.from_string(self.prompt)
        content = template.render(**kwargs)
        return content


class TemplateSource(BaseModel):
    content: str
    metadata: TemplateMetadata


# ------------------------------------------
# Jinja Environment and Template Loading
# ------------------------------------------


def get_env(templates_dir: Optional[Path] = None) -> Environment:
    if templates_dir is None:
        templates_dir = settings.TEMPLATES_DIR

    templates_dir.mkdir(parents=True, exist_ok=True)

    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )


def load_template_source(template_name: str, env: Environment) -> TemplateSource:
    """Load and parse a template file with frontmatter metadata."""
    logger.info(f"Loading template: {template_name}")
    try:
        if env.loader is None:
            raise FileNotFoundError(f"No template loader configured for template: {template_name}")

        template_source, _, _ = env.loader.get_source(env, template_name)
        post = frontmatter.loads(template_source)
        metadata = cast(Dict[str, Any], post.metadata)

        logger.info(f"Successfully loaded template: {template_name}")
        return TemplateSource(
            content=post.content,
            metadata=TemplateMetadata(
                **{
                    "type": metadata.get("type", "system"),
                    "author": metadata.get("author", ""),
                    "version": int(metadata.get("version", 1)),
                    "labels": metadata.get("labels", []),
                    "tags": metadata.get("tags", []),
                    "config": metadata.get("config", {}),
                }
            ),
        )
    except Exception as e:
        logger.error(f"Failed to load template {template_name}: {str(e)}")
        raise FileNotFoundError(
            f"Template file not found: {template_name}. Error: {str(e)}"
        ) from e


def get_prompt(name: str, templates_dir: Optional[Path] = None) -> PromptModel:
    env = get_env(templates_dir)
    template = load_template_source(f"{name}.j2", env)

    return PromptModel(
        name=name,
        prompt=template.content,
        **template.metadata.model_dump(),
    )
