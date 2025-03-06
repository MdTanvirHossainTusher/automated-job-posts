from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy_utils import URLType
from app.database import Base
from sqlalchemy.orm import relationship

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    website = Column(URLType, unique=True)
    location = Column(String)
    description = Column(String)
    size = Column(String)
    is_multi_national = Column(Boolean)

    jobs = relationship("Job", back_populates="company")