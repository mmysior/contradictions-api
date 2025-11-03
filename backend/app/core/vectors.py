import logging
from functools import lru_cache
from typing import List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.core.config import settings
from app.schemas.parameters import Parameter
from app.schemas.principles import Principle
from app.utils import get_parameters, get_principles

logger = logging.getLogger(__name__)


@lru_cache()
def get_encoder() -> SentenceTransformer:
    try:
        encoder = SentenceTransformer(settings.EMBEDDING_MODEL, device="cpu")
        logger.info("Loaded embedding model: %s", settings.EMBEDDING_MODEL)
        return encoder
    except Exception as e:
        logger.error("Failed to load embedding model: %s", e)
        raise


class VectorStore:
    def __init__(self):
        self.encoder = get_encoder()
        self.parameters = get_parameters()
        self.principles = get_principles()
        self.parameter_embeddings = self._compute_embeddings(
            [p.name for p in self.parameters]
        )
        self.principle_embeddings = self._compute_embeddings(
            [p.name for p in self.principles]
        )
        logger.info(
            "Loaded %d parameters and %d principles",
            len(self.parameters),
            len(self.principles),
        )

    def _compute_embeddings(self, texts: List[str]) -> np.ndarray:
        return self.encoder.encode(texts)

    def search_parameters(
        self, query: str, top_k: int = 5
    ) -> List[Tuple[Parameter, float]]:
        logger.info(f"Searching parameters with semantic similarity (query='{query}', top_k={top_k})")
        query_embedding = self.encoder.encode([query])
        similarities = cosine_similarity(query_embedding, self.parameter_embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [(self.parameters[i], similarities[i]) for i in top_indices]

    def search_principles(
        self, query: str, top_k: int = 5
    ) -> List[Tuple[Principle, float]]:
        logger.info(f"Searching principles with semantic similarity (query='{query}', top_k={top_k})")
        query_embedding = self.encoder.encode([query])
        similarities = cosine_similarity(query_embedding, self.principle_embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [(self.principles[i], similarities[i]) for i in top_indices]


@lru_cache()
def get_vector_store() -> VectorStore:
    return VectorStore()
