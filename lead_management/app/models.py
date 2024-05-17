from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    resume = Column(String)
    state = Column(String, default="PENDING")
    created_at = Column(DateTime, default=datetime.now())
