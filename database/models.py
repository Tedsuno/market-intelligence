from sqlalchemy import Boolean, Column, Integer, String, DateTime, create_engine,Float
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
    salary_min= Column(Float) 
    salary_max= Column(Float)  
    skills= Column(String(255)) 
    latitude = Column(Float)
    longitude = Column(Float)
    is_remote = Column(Boolean, default=False)
    geocoding_quality = Column(String(20)) 
    contract_type = Column(String(255))
    seniority = Column(String(255))
    job_name = Column(String(255))