from dotenv import load_dotenv
import os

load_dotenv()

def _from_pg_env():
    host = os.getenv("PGHOST")
    db   = os.getenv("PGDATABASE")
    user = os.getenv("PGUSER")
    pwd  = os.getenv("PGPASSWORD")
    port = os.getenv("PGPORT", "5432")
    sslm = os.getenv("PGSSLMODE")  # ex: require
    if host and db and user and pwd:
        url = f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{db}"
        if sslm:
            url += f"?sslmode={sslm}"
        return url
    return None

# 1) Streamlit Secrets
DATABASE_URL = None
try:
    import streamlit as st
    DATABASE_URL = st.secrets.get("DATABASE_URL")
except Exception:
    DATABASE_URL = None

# 2) Variable d'env DATABASE_URL (fallback local)
if not DATABASE_URL:
    DATABASE_URL = os.getenv("DATABASE_URL")

# 3) Variables PG* (fallback style “ton pote”)
if not DATABASE_URL:
    DATABASE_URL = _from_pg_env()

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL manquante")
