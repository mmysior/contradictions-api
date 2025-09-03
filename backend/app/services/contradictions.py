import logging
from typing import List

import llmsuite as llm
from dotenv import load_dotenv

from app.schemas.contradictions import TCModels, TechnicalContradiction
from app.services import parameters as params_service
from app.services import principles as princs_service

logger = logging.getLogger(__name__)

load_dotenv()


def extract_tc(text: str, model: str, provider: str, max_parameters: int = 3) -> List[TechnicalContradiction]:
    """Extract technical contradictions from text description with full TRIZ analysis."""
    prompt = llm.get_prompt("extract_tc_from_text")
    messages = llm.build_messages(
        provider=provider,
        text=text,
        system_prompt=prompt.compile(),
    )
    result: TCModels = llm.extract(
        messages,
        TCModels,
        model=model,
        provider=provider,
    )

    technical_contradictions = []
    for tc_model in result.contradictions:
        # Find parameters that match the positive and negative effects
        improving_results = params_service.search_parameters(tc_model.positive_effect, top_k=max_parameters)
        improving_params = [param.id for param, score in improving_results[:max_parameters]]

        preserving_results = params_service.search_parameters(tc_model.negative_effect, top_k=max_parameters)
        preserving_params = [param.id for param, score in preserving_results[:max_parameters]]

        # Get principles from the contradiction matrix
        principle_objects = princs_service.get_principles_from_matrix(improving_params, preserving_params)
        principles = [p.name for p in principle_objects]

        # Create the full TechnicalContradiction object
        technical_contradiction = TechnicalContradiction(
            action=tc_model.action,
            positive_effect=tc_model.positive_effect,
            negative_effect=tc_model.negative_effect,
            parameters_to_improve=improving_params,
            parameters_to_preserve=preserving_params,
            principles=principles,
        )

        technical_contradictions.append(technical_contradiction)

    return technical_contradictions
