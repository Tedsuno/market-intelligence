from sqlalchemy import Column, Integer, String, DateTime, create_engine,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.models import Base, Job
from config.settings import DATABASE_URL

ENGINE=create_engine(DATABASE_URL)
    
def get_db():
    Session = sessionmaker(bind=ENGINE)
    session = Session()
    return session

def init_db():
    Base.metadata.create_all(ENGINE)
    
def test_connection():
    try:
        session = get_db()
        session.close()
        print("Connexion Railway réussie !")
        return True   
    except Exception as e:
        print(f"Erreur connexion: {e}")
        return False
    