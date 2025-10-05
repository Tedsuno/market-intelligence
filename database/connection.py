from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from database.models import Base
from config.settings import DATABASE_URL

ENGINE = create_engine(DATABASE_URL, pool_pre_ping=True)

def get_db():
    Session = sessionmaker(bind=ENGINE, autoflush=False, autocommit=False)
    return Session()

def init_db():
    Base.metadata.create_all(ENGINE)

def test_connection():
    try:
        with ENGINE.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("OK")
        return True
    except Exception as e:
        print(e)
        return False
