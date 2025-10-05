import streamlit as st
import pandas as pd
from sqlalchemy import text
import ast
from .connection import get_db

def get_jobs_from_database():
    db = get_db()
    try:
        rows = db.execute(text("SELECT * FROM jobs;")).fetchall()
        cols = db.execute(text("SELECT * FROM jobs LIMIT 0;")).keys()
        return pd.DataFrame(rows, columns=cols)
    finally:
        db.close()




def clip_final(v):
    if v is None or pd.isna(v) or v <= 0:
        return 0
    if 200_000 < v < 20_000_000:
        v = v / 1000
    return min(max(int(v), 15_000), 200_000)



def skills_to_list(x):
    if isinstance(x, list):
        return [str(v).strip() for v in x]
    if x is None or x == "{}" or (isinstance(x, float) and pd.isna(x)):
        return []
    s = str(x).strip()
    if s == "":
        return []
    try:
        val = ast.literal_eval(s)
        if isinstance(val, (list, tuple)):
            return [str(v).strip() for v in val]
    except Exception:
        pass
    s = s.strip("{}[]")
    if not s:
        return []
    parts = [p.strip().strip("'\"") for p in s.split(",") if p.strip()]
    return parts

def prepare_dataframe(df):
    df["salary_min"] = pd.to_numeric(df.get("salary_min"), errors="coerce")
    df["salary_max"] = pd.to_numeric(df.get("salary_max"), errors="coerce")

    smin = df["salary_min"]
    smax = df["salary_max"]

    cnt = (~smin.isna()).astype(int) + (~smax.isna()).astype(int)

    somme = smin.fillna(0) + smax.fillna(0)
    df["salary_average"] = somme / cnt.replace(0, 1)   
    df.loc[cnt == 0, "salary_average"] = 0             

    df["salary_avg_clean"] = df["salary_average"].apply(clip_final)
    df["skills_clean"] = df["skills"].apply(skills_to_list)
    return df



def get_top_cities(df, top_n=12):
    df_ville = (df.groupby("location", as_index=False)["salary_avg_clean"]
                  .agg(['median', 'min', 'max'])
                  .sort_values("median", ascending=False)
                  .head(top_n)
                  .reset_index())
    df_ville['error_minus'] = df_ville['median'] - df_ville['min']
    df_ville['error_plus'] = df_ville['max'] - df_ville['median']
    return df_ville



def get_skills_analysis(df):
    base = df[~df["salary_avg_clean"].isna()].copy()
    
    skills_df = (
        base.explode("skills_clean")
            .dropna(subset=["skills_clean"])
            .groupby("skills_clean", as_index=False)
            .agg(nb_offres=("id", "count"),
                 salaire_moyen=("salary_avg_clean", "mean"))
            .sort_values("nb_offres", ascending=False)
    )
    
    return skills_df



def get_remote_comparison(df):
    df = df.copy()
    df['is_remote'] = df['is_remote'].astype(bool)
    df['type_travail'] = df['is_remote'].map({
        True: "Remote", 
        False: "Présentiel"
    })
    
    results = []
    
    for work_type in ["Remote", "Présentiel"]:
        subset = df[df['type_travail'] == work_type]
        with_salary = subset[subset['salary_avg_clean'] > 0]
        
        if len(with_salary) > 0:
            median_salary = with_salary['salary_avg_clean'].median()
            mean_salary = with_salary['salary_avg_clean'].mean()
        else:
            median_salary = 0
            mean_salary = 0
        
        results.append({
            'type_travail': work_type,
            'salary_avg_clean': median_salary,
            'salaire_moyen': mean_salary,
            'nb_offres': len(subset),
            'nb_avec_salaire': len(with_salary)
        })
    
    return pd.DataFrame(results)


def get_heatmap_data(df, top_cities_n=20, top_skills_n=15):
    top_villes = df.groupby("job_name").size().head(top_cities_n).index.tolist()
    
    skills_df = get_skills_analysis(df)
    top_skills = skills_df.head(top_skills_n)['skills_clean'].tolist()
    
    df_exploded = df.explode("skills_clean")
    df_heatmap_filtered = df_exploded[
        df_exploded["job_name"].isin(top_villes) & 
        df_exploded["skills_clean"].isin(top_skills)
    ]
    
    counts = df_heatmap_filtered.groupby(["job_name", "skills_clean"]).size().reset_index(name='count')
    matrix = counts.pivot_table(index="job_name", columns="skills_clean", values="count").fillna(0)
    
    return matrix


def apply_dashboard_styles():
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            color: white;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .metric-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin: 0.5rem;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        
        .section-header {
            background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin: 1rem 0;
            text-align: center;
            font-weight: bold;
            font-size: 1.2em;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>Dashboard Market Intelligence - Python Jobs</h1>
        <p style="font-size: 1.1em; margin-top: 10px;">Analyse du marché de l'emploi en temps réel</p>
    </div>
    """, unsafe_allow_html=True)


def render_metric(icon, value, label):
    st.markdown(f"""
    <div class="metric-container">
        <h2 style="margin: 0;">{icon}</h2>
        <h3 style="margin: 0;">{value}</h3>
        <p style="margin: 0;">{label}</p>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)


def render_footer():
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown(
        "<div style='text-align: center; color: #666; padding: 20px;'>"
        "TechJobs Intelligence Dashboard"
        "</div>", 
        unsafe_allow_html=True
    )