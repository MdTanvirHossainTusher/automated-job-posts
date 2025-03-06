from typing import Optional

from pydantic import BaseModel, Field, HttpUrl
from pydantic.v1 import root_validator


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description='Company name')
    website: Optional[HttpUrl] = None
    location: Optional[str] = None
    description: Optional[str] = None
    size: Optional[str] = Field(None, pattern=r'^(Startup|Small|Medium|Large|Enterprise)$')
    is_multi_national: bool = False


class CompanyCreateRequest(CompanyBase):
    @root_validator
    def name_must_not_be_empty(cls, values):
        name = values.get("name")
        if name.strip() == "":
            raise ValueError("Company name can't be empty!")
        return values


class CompanyUpdateRequest(BaseModel):
    website: Optional[HttpUrl] = None
    location: Optional[str] = None
    description: Optional[str] = None
    size: Optional[str] = Field(None, pattern=r'^(Startup|Small|Medium|Large|Enterprise)$')
    is_multi_national: bool = False


class CompanyResponse(CompanyBase):
    id: int
    total_jobs: int = 0

    class Config:
        from_attributes = True


class CompanyDetailResponse(CompanyResponse):
    companies: list[CompanyResponse]