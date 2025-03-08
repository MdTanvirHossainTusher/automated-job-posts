# from typing import Optional, List
#
# from pydantic import BaseModel, Field, HttpUrl
# from pydantic.v1 import root_validator
# from datetime import date
#
# from app.models import Skill
#
#
# class JobBase(BaseModel):
#     title: str = Field(..., min_length=2, max_length=100, description='Job title')
#     company_name: str = Field(..., min_length=2, max_length=100, description='Company name')
#     job_url: str = Field(..., min_length=2, max_length=250, description='Job url')
#     job_description: Optional[str] = None
#     application_deadline: Optional[date] = None
#     required_experience: Optional[str] = None
#     location: Optional[str] = 'Bangladesh'
#     company_id: int = Field(..., description='Company ID')
#     required_skills: List[Skill] = Field(..., description='Required skill IDs')
#
#
# class JobCreateRequest(JobBase):
#     @root_validator
#     def validate(cls, values):
#         title = values.get("title")
#         company_name = values.get("company_name")
#         job_url = values.get("job_url")
#         if title.strip() == "":
#             raise ValueError("Job title can't be empty!")
#         return values
#
#
# class JobUpdateRequest(BaseModel):
#     website: Optional[HttpUrl] = None
#     location: Optional[str] = None
#     description: Optional[str] = None
#     size: Optional[str] = Field(None, pattern=r'^(Startup|Small|Medium|Large|Enterprise)$')
#     is_multi_national: bool = False
#
#
# class JobResponse(JobBase):
#     id: int
#     total_jobs: int = 0
#
#     class Config:
#         from_attributes = True
#
#
# class JobDetailResponse(JobResponse):
#     companies: list[JobResponse]