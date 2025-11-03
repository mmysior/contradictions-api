from typing import List

from pydantic import BaseModel, Field


class PatentContent(BaseModel):
    description: str = Field(..., description="Patent description")
    claims: List[str] = Field(..., description="List of patent claims")


class PatentMeta(BaseModel):
    title: str = Field(..., description="The title of the patent document")
    abstract: str = Field(..., description="Content of the abstract as parsed from the title page")
    patent_no: str = Field(..., description="Unique identifier/number assigned to the patent")
    inventors: list[str] = Field(..., description="List of names of the patent inventors")
    published_date: str = Field(..., description="Date when the patent was officially published")
    ipc: list[str] = Field(..., description="List of International Patent Classification codes")


class PatentContradiction(BaseModel):
    action_parameter: str = Field(
        ..., description="The Parameter being acted upon in the contradiction."
    )
    positive_effect: str = Field(
        ..., description="The Evaluation Parameter that is improved as a result of the action."
    )
    negative_effect: str = Field(
        ..., description="The Evaluation Parameter that is worsened as a result of the action."
    )


class PatentDocument(BaseModel):
    meta: PatentMeta = Field(..., description="Metadata of the patent document")
    content: PatentContent = Field(..., description="Content of the patent document")
    contradictions: List[PatentContradiction] | None = None


class PatentUrlRequest(BaseModel):
    url: str = Field(..., description="URL to the patent PDF document")
