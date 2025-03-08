# from pyasn1.type.univ import Boolean
from sqlalchemy import Integer, Column, String, Boolean

from app.database import Base


class CareerSite(Base):
    __tablename__ = "career_sites"

    id = Column(Integer, primary_key=True, index=True)
    site_url = Column(String, unique=True)
    deleted = Column(Boolean, default=False)