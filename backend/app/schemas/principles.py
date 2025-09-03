from typing import List

from pydantic import BaseModel, Field


class Principle(BaseModel):
    id: int
    name: str = Field(..., description="The name of the principle.")
    description: str = Field("", description="A brief description of the principle.")
    rules: List[str] = Field([], description="The rules to apply the principle.")
    hints: List[str] = Field([], description="Hints for applying the principle.")
    examples: List[str] = Field([], description="Examples of the principle in action.")


class ScoredPrinciple(BaseModel):
    principle: Principle
    score: float = Field(..., description="Similarity score (0.0 to 1.0)")


class Principles(BaseModel):
    principles: List[Principle]
