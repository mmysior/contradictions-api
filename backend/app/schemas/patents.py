from typing import Optional

from pydantic import BaseModel, Field


class PatentContent(BaseModel):
    title: str = Field(..., description="Patent title")
    abstract: str = Field(..., description="Patent abstract")
    description: str = Field(..., description="Patent description")


class PatentClassificationInput(BaseModel):
    title: str = Field(..., description="Patent title")
    abstract: str = Field(..., description="Patent abstract")
    description: str = Field(..., description="Patent description")
    titlepage_image: Optional[str] = Field(
        None, description="Base64 encoded titlepage image"
    )
