# from fastapi import APIRouter
# from sqlalchemy.orm import Session
# from app.database import get_db
# from fastapi import Depends
# from app.schemas.job_schema import JobCreateRequest, JobUpdateRequest, JobResponse, JobDetailResponse
# from app.services.job_service import JobService
#
# router = APIRouter(prefix="/jobs", tags=["Job"])
#
#
# @router.get("", response_model=list[JobResponse])
# async def get_all_jobs(db: Session = Depends(get_db)):
#     return JobService(db).get_all_companies()
#
#
# @router.get("/{job_id}")
# async def get_job(job_id: int, db: Session = Depends(get_db)):
#     return JobService(db).get_job_by_id(job_id)
#
#
# @router.post("")
# async def create_job(job: JobCreateRequest, db: Session = Depends(get_db)):
#     return JobService(db).create_job(job)
#
#
# @router.put("/{job_id}")
# async def update_job(job_id: int, updated_job: JobUpdateRequest, db: Session = Depends(get_db)):
#     return JobService(db).update_job(job_id, updated_job)
#
#
# @router.delete("/{job_id}")
# async def delete_job(job_id: int, db: Session = Depends(get_db)):
#     return JobService(db).delete_job(job_id)
