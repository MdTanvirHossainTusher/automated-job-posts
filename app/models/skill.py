from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship
from app.models.associations import job_skills


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)  

    jobs = relationship("Job", secondary=job_skills, back_populates="required_skills")