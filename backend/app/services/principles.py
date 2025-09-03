import csv
import logging
import random
from functools import lru_cache
from importlib import resources as pkg_resources
from itertools import product
from typing import List, Set, Tuple

import numpy as np

from app.core.vectors import get_vector_store
from app.schemas.principles import Principle

logger = logging.getLogger(__name__)


@lru_cache()
def _load_matrix() -> np.ndarray:
    """Load the TRIZ contradiction matrix from CSV file."""
    matrix_path = pkg_resources.files("app.data") / "matrix_values.csv"
    with open(matrix_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        matrix_data = list(reader)

    matrix = np.array(matrix_data, dtype=object)
    logger.info("Loaded TRIZ matrix with shape %dx%d", *matrix.shape)
    return matrix


def get_principles_from_matrix(
    improving_parameters: List[int], preserving_parameters: List[int]
) -> List[Principle]:
    """Get inventive principles from TRIZ contradiction matrix based on parameter pairs."""
    if not all(isinstance(x, int) for x in improving_parameters + preserving_parameters):
        raise TypeError("All parameter IDs must be integers")
    if not all(x > 0 for x in improving_parameters + preserving_parameters):
        raise ValueError("All parameter IDs must be positive integers")

    matrix = _load_matrix()
    vector_store = get_vector_store()

    row_indices = [i - 1 for i in improving_parameters]
    col_indices = [i - 1 for i in preserving_parameters]

    principle_ids: Set[int] = set()
    for row, col in product(row_indices, col_indices):
        if row == col:
            continue

        if row >= matrix.shape[0] or col >= matrix.shape[1]:
            continue

        cell_value = matrix[row, col]
        if cell_value and cell_value != "":
            principle_list = cell_value.split(",")
            for p in principle_list:
                try:
                    principle_ids.add(int(p.strip()))
                except (ValueError, AttributeError):
                    continue

    sorted_principle_ids = sorted(principle_ids)
    return [p for p in vector_store.principles if p.id in sorted_principle_ids]


def get_all_principles() -> List[Principle]:
    """Get all TRIZ inventive principles."""
    vector_store = get_vector_store()
    return vector_store.principles


def search_principles(query: str, top_k: int = 5) -> List[Tuple[Principle, float]]:
    """Search TRIZ inventive principles by semantic similarity."""
    vector_store = get_vector_store()
    return vector_store.search_principles(query, top_k)


def get_principle_by_id(principle_id: int) -> Principle:
    """Get a specific TRIZ inventive principle by ID."""
    vector_store = get_vector_store()
    principle = next((p for p in vector_store.principles if p.id == principle_id), None)
    if not principle:
        raise ValueError(f"Principle with id {principle_id} not found")
    return principle


def get_principle_by_name(principle_name: str) -> Principle:
    """Get a specific TRIZ inventive principle by name."""
    vector_store = get_vector_store()
    principle = next((p for p in vector_store.principles if p.name.lower() == principle_name.lower()), None)
    if not principle:
        raise ValueError(f"Principle with name '{principle_name}' not found")
    return principle


def get_random_principles(count: int = 5) -> List[Principle]:
    """Get a specified number of random TRIZ inventive principles."""
    vector_store = get_vector_store()
    all_principles = vector_store.principles

    if count >= len(all_principles):
        return all_principles

    return random.sample(all_principles, count)
