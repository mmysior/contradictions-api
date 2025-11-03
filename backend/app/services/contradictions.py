import logging

from dotenv import load_dotenv

from app.core.llm import build_messages, extract
from app.prompts import get_prompt
from app.schemas.contradictions import TCModels, TContradictions, TechnicalContradiction

logger = logging.getLogger(__name__)

load_dotenv()


def extract_tc(text: str, model: str, provider: str) -> TContradictions:
    """Extract technical contradictions from text description with full TRIZ analysis."""
    prompt = get_prompt("extract_tc_from_text")
    messages = build_messages(
        provider=provider,
        text=text,
        system_prompt=prompt.compile(),
    )
    result: TCModels = extract(
        messages,
        TCModels,
        model=model,
        provider=provider,
    )

    technical_contradictions = []
    for tc_model in result.contradictions:
        technical_contradiction = TechnicalContradiction(
            action=tc_model.action,
            positive_effect=tc_model.positive_effect,
            negative_effect=tc_model.negative_effect,
        )

        technical_contradictions.append(technical_contradiction)

    return TContradictions(contradictions=technical_contradictions)
