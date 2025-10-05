from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_URL = None
try:
    import streamlit as st  # dispo en cloud
    DATABASE_URL = st.secrets.get("DATABASE_URL", None)
except Exception:
    pass

if not DATABASE_URL:
    DATABASE_URL = os.getenv("DATABASE_URL")
