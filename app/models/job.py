from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
from app.models.associations import job_skills


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company_name = Column(String)
    job_url = Column(String)
    job_description = Column(String)
    application_deadline = Column(Date)
    required_experience = Column(String)
    location = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))

    company = relationship("Company", back_populates="jobs")

    required_skills = relationship("Skill", secondary=job_skills, back_populates="jobs")