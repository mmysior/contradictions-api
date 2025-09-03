from typing import List

from pydantic import BaseModel, Field


class Parameter(BaseModel):
    id: int
    name: str = Field(..., description="The name of the parameter.")
    description: str = Field("", description="A brief description of the parameter.")
    examples: List[str] = Field([], description="Examples of the parameter values.")


class ScoredParameter(BaseModel):
    parameter: Parameter
    score: float = Field(..., description="Similarity score (0.0 to 1.0)")


class Parameters(BaseModel):
    parameters: List[Parameter]
