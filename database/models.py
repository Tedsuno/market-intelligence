from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()  

class Job(Base):
    __tablename__ = 'jobs'
    
    id = Column(Integer, primary_key=True)           
    title = Column(String(255))
    company = Column(String(255))
    location = Column(String(255))
    url = Column(String(255))
    source = Column(String(255))
    scraped_at = Column(DateTime)                    