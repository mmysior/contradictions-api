from typing import List

import llmsuite as llm

from ..core.vectors import get_vector_store
from ..schemas.contradictions import TechnicalContradiction, TechnicalContradictions
from ..schemas.patents import PatentClassificationInput, PatentContent
from ..schemas.principles import ScoredPrinciple
from ..services import contradictions as contradictions_service


def extract_patent_contradictions(
    patent: PatentContent, model: str, provider: str, max_parameters: int = 3
) -> List[TechnicalContradiction]:
    """Extract technical contradictions from patent content."""
    # Build patent content as multiline string for the prompt
    patent_text = f"""
    Title: {patent.title}
    Abstract: {patent.abstract}
    Description: {patent.description}
    """

    # Use the common contradiction extraction service with parameter limit
    return contradictions_service.extract_tc(patent_text, model, provider, max_parameters)


def classify_patent_to_principles(
    patent: PatentClassificationInput, model: str, provider: str, max_principles: int = 10
) -> List[ScoredPrinciple]:
    """Classify patent solutions to TRIZ inventive principles with relevance scores."""
    # Get all principles from vector store for reference
    vector_store = get_vector_store()

    # Build patent content for analysis
    patent_text = f"""
    Title: {patent.title}
    Abstract: {patent.abstract}
    Description: {patent.description}
    """

    # For now, use semantic search as a classification approach
    # This finds the most relevant principles based on the patent content
    search_results = vector_store.search_principles(patent_text, top_k=max_principles)

    # Convert to ScoredPrinciple format
    return [
        ScoredPrinciple(principle=principle, score=score)
        for principle, score in search_results
    ]
