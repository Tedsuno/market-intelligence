from dotenv import load_dotenv
import os
load_dotenv()

def _build_from_pg_env():
    host = os.getenv("PGHOST")
    db   = os.getenv("PGDATABASE")
    user = os.getenv("PGUSER")
    pwd  = os.getenv("PGPASSWORD")
    port = os.getenv("PGPORT", "5432")
    sslm = os.getenv("PGSSLMODE")  # ex: require
    if not (host and db and user and pwd):
        return None
    url = f"postgresql+psycopg://{user}:{pwd}@{host}:{port}/{db}"
    if sslm:
        url += f"?sslmode={sslm}"
    return url

def _get_db_url():
    # 1) Streamlit secrets (prod)
    try:
        import streamlit as st
        url = st.secrets.get("DATABASE_URL")
    except Exception:
        url = None
    # 2) DATABASE_URL
    if not url:
        url = os.getenv("DATABASE_URL")
    # 3) Build via PG* (comme ton pote)
    if not url:
        url = _build_from_pg_env()
    if not url:
        raise RuntimeError("Aucune URL DB trouvée")
    return url

DATABASE_URL = _get_db_url()
#
