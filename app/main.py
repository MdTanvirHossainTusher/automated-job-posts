from fastapi import FastAPI
from app.database import engine
from app.database import Base
from app.models import Company, Job, Skill
# from app.routes import job_router, company_router, skill_router, career_site_router
from app.routes import career_site_router


Base.metadata.create_all(bind=engine)

app = FastAPI()

# app.include_router(job_router)
# app.include_router(company_router)
# app.include_router(skill_router)

app.include_router(career_site_router)