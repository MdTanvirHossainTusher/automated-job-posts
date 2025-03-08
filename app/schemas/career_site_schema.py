from typing import Optional

from pydantic import BaseModel, Field, HttpUrl
from pydantic.v1 import root_validator


class CareerSiteBase(BaseModel):
    id: int
    site_url: str = Field(..., min_length=2, max_length=250, description='Career site url')


class CareerSiteCreateRequest(BaseModel):
    site_url: str = Field(..., min_length=2, max_length=250, description='Career site url')

    @root_validator
    def url_must_not_be_empty(cls, values):
        site_url = values.get("site_url")
        if site_url.strip() == "":
            raise ValueError("Career Site URL can't be empty!")
        return values


class CareerSiteUpdateRequest(CareerSiteCreateRequest):
    pass


class CareerSiteResponse(CareerSiteBase):
    class Config:
        from_attributes = True