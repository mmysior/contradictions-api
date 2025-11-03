import uuid
from typing import List

from pydantic import BaseModel, Field


class TCModel(BaseModel):
    action: str = Field(..., description="Concise description of the action.")
    positive_effect: str = Field(..., description="The improvement caused by the action.")
    negative_effect: str = Field(..., description="The deterioration caused by the action.")


class TCModels(BaseModel):
    contradictions: List[TCModel]


class TechnicalContradiction(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique identifier.")
    action: str = Field(..., description="Concise description of the action.")
    positive_effect: str = Field(..., description="The improvement caused by the action.")
    negative_effect: str = Field(..., description="The deterioration caused by the action.")


class TContradictions(BaseModel):
    contradictions: List[TechnicalContradiction] = Field(
        ..., description="List of technical contradictions extracted from the text"
    )


class TextInput(BaseModel):
    description: str
