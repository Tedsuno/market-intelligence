import streamlit as st
import pandas as pd
from sqlalchemy import text
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.connection import get_db
import plotly.express as px
import numpy as np
import ast
def get_jobs_from_database():
    db = get_db()
    jobs = db.execute(text("SELECT * FROM Jobs;"))
    rows = jobs.fetchall()
    columns = jobs.keys()
    return pd.DataFrame(rows, columns=columns)
df = get_jobs_from_database()
is_remote=(df['is_remote']==True).sum()
print(is_remote)