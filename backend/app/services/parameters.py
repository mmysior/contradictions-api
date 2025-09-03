from typing import List, Tuple

from app.core.vectors import get_vector_store
from app.schemas.parameters import Parameter


def get_all_parameters() -> List[Parameter]:
    """Get all TRIZ parameters."""
    vector_store = get_vector_store()
    return vector_store.parameters


def search_parameters(query: str, top_k: int = 5) -> List[Tuple[Parameter, float]]:
    """Search TRIZ parameters by semantic similarity."""
    vector_store = get_vector_store()
    return vector_store.search_parameters(query, top_k)


def get_parameter_by_id(parameter_id: int) -> Parameter:
    """Get a specific TRIZ parameter by ID."""
    vector_store = get_vector_store()
    parameter = next((p for p in vector_store.parameters if p.id == parameter_id), None)
    if not parameter:
        raise ValueError(f"Parameter with id {parameter_id} not found")
    return parameter