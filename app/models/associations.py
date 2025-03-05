from sqlalchemy import Column, ForeignKey, Integer, Table
from app.database import Base
# from ..database import Base


job_skills = Table( 
    "job_skills",
    Base.metadata,
    Column("job_id", Integer, ForeignKey("jobs.id")),
    Column("skill_id", Integer, ForeignKey("skills.id"))
)
