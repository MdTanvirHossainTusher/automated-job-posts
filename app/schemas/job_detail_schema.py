from typing import Optional, List

from pydantic import BaseModel


class JobDetailResponse(BaseModel):
    job_title: Optional[str] = None
    required_experience: Optional[str] = None
    job_url: Optional[str] = None
    deadline: Optional[str] = None
    company_name: Optional[str] = None
    company_image: Optional[str] = None


class Jobs(JobDetailResponse):
    jobs: List[JobDetailResponse]
