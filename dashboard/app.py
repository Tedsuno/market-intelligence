import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd

from database.utils import (
    get_jobs_from_database, 
    prepare_dataframe, 
    get_top_cities,
    get_skills_analysis,
    get_remote_comparison,
    get_heatmap_data,
    apply_dashboard_styles,
    render_header,
    render_metric,
    render_section_header,
    render_footer
)
import plotly.express as px

st.set_page_config(page_title="TechJobs Intelligence", layout="wide")


def apply_filters(df):
    with st.sidebar:
        st.markdown("## Filtres Interactifs")
        cities = ['Toutes'] + sorted(df['location'].dropna().unique().tolist())
        selected_city = st.selectbox("Filtrer par ville", cities)

        include_no_salary = st.checkbox("Inclure les offres sans info salaire", value=True)

        salary_range = st.slider(
            "Fourchette de salaire (€)", 
            min_value=0, max_value=200000, value=(0, 100000), step=5000
        )
        remote_filter = st.radio("Type de travail", ["Tous", "Remote seulement", "Présentiel seulement"])

    df_filtered = df.copy()
    df_filtered["salary_avg_clean"] = pd.to_numeric(df_filtered["salary_avg_clean"], errors="coerce").fillna(0)

    if selected_city != 'Toutes':
        df_filtered = df_filtered[df_filtered['location'] == selected_city]

    if remote_filter == "Remote seulement":
        df_filtered = df_filtered[df_filtered['is_remote'] == True]
    elif remote_filter == "Présentiel seulement":
        df_filtered = df_filtered[df_filtered['is_remote'] == False]

    if include_no_salary:
        df_filtered = df_filtered[
            (df_filtered['salary_avg_clean'] == 0) |
            ((df_filtered['salary_avg_clean'] > 0) &
             (df_filtered['salary_avg_clean'] >= salary_range[0]) &
             (df_filtered['salary_avg_clean'] <= salary_range[1]))
        ]
    else:
        df_filtered = df_filtered[
            (df_filtered['salary_avg_clean'] > 0) &
            (df_filtered['salary_avg_clean'] >= salary_range[0]) &
            (df_filtered['salary_avg_clean'] <= salary_range[1])
        ]

    return df_filtered



def render_kpis(df):
    is_remote = (df['is_remote'] == True).sum()
    df_with_salary = df[df['salary_avg_clean'] > 0]
    if len(df_with_salary) > 0:
        avg_salary = df_with_salary['salary_avg_clean'].mean()
    else:
        avg_salary = 0
    
    remote_pct = (is_remote / len(df)) * 100 if len(df) > 0 else 0
    offers_without_salary = len(df[df['salary_avg_clean'] == 0])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_metric("📶", f"{len(df):,}", "Total offres")
    
    with col2:
        if avg_salary > 0:
            render_metric("💲", f"{avg_salary:,.0f} €", "Salaire moyen")
        else:
            render_metric("💲", "N/A", "Salaire moyen")
    
    with col3:
        render_metric("🏠︎", f"{remote_pct:.1f}%", "% Remote")
    
    with col4:
        render_metric("❔", f"{offers_without_salary:,}", "Sans salaire")


def render_city_chart(df):
    df_with_salary = df[df['salary_avg_clean'] > 0]
    
    if len(df_with_salary) == 0:
        st.warning("Aucune offre avec salaire pour afficher ce graphique.")
        return
    
    df_ville = get_top_cities(df_with_salary)
    
    fig = px.bar(
        df_ville, 
        x="location", 
        y="median",
        error_y_minus="error_minus",
        error_y="error_plus",
        title="Top 12 villes — Salaire médian (€)",
        color="median",
        color_continuous_scale="viridis"
    )
    
    fig.update_layout(
        xaxis_tickangle=-90, 
        yaxis_title="Salaire médian (€)",
        height=420, 
        margin=dict(l=8, r=8, t=40, b=8),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_skills_chart(df):
    skills_df = get_skills_analysis(df)

    skills_df_with_salary = skills_df[skills_df['salaire_moyen'] > 0].head(20)
    
    if len(skills_df_with_salary) == 0:
        st.warning("Aucune compétence avec salaire pour afficher ce graphique.")
        return
    
    fig = px.scatter(
        skills_df_with_salary,
        x="nb_offres",
        y="salaire_moyen",
        size="nb_offres",
        color="salaire_moyen",
        hover_name="skills_clean",
        title="Top compétences : Demande vs Salaire moyen",
        color_continuous_scale="plasma",
        size_max=60
    )
    
    fig.update_layout(
        xaxis_title="Nombre d'offres", 
        yaxis_title="Salaire moyen (€)",
        height=420, 
        margin=dict(l=8, r=8, t=40, b=8),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_map(df):
    map_df = df[
        df["latitude"].notna() & 
        df["longitude"].notna()
    ].copy()
    
    if len(map_df) > 0:
        map_df = map_df.astype({"latitude": "float", "longitude": "float"})
        
        map_df['salary_display'] = map_df['salary_avg_clean'].apply(
            lambda x: x if x > 0 else 30000
        )
        map_df['has_salary'] = map_df['salary_avg_clean'] > 0
        
        fig = px.scatter_mapbox(
            map_df,
            lat="latitude",
            lon="longitude",
            color="salary_display",
            mapbox_style="open-street-map",
            zoom=4,
            center={"lat": 46.5, "lon": 2.5},
            color_continuous_scale="turbo",
            size="salary_display",
            size_max=30,
            hover_data=['location', 'salary_avg_clean']
        )
        
        fig.update_layout(height=520, margin=dict(l=0, r=0, t=40, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée géographique disponible pour les filtres sélectionnés.")


def render_remote_comparison(df):
    df_with_salary = df[df['salary_avg_clean'] > 0]
    
    if len(df_with_salary) == 0:
        st.warning("Aucune offre avec salaire pour cette comparaison.")
        return
    
    group = get_remote_comparison(df)
    
    fig = px.bar(
        group,
        x="type_travail",
        y="salary_avg_clean",
        title="Comparaison salaires : Remote vs Présentiel",
        color="type_travail", 
        color_discrete_map={"Remote": "#FF6B6B", "Présentiel": "#4ECDC4"},
        text="salary_avg_clean"
    )
    
    fig.update_layout(
        xaxis_title="Type de travail",
        yaxis_title="Salaire médian (€)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    
    fig.update_traces(texttemplate='%{text:,.0f}€', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)


def render_heatmap(df):
    matrix = get_heatmap_data(df)
    
    if not matrix.empty:
        fig = px.imshow(
            matrix, 
            color_continuous_scale="Viridis",  
            title="Heatmap Skills par Ville", 
            text_auto=True,
            aspect="auto"
        )
        
        fig.update_layout(
            height=700, 
            margin=dict(l=120, r=80, t=80, b=120), 
            title_font_size=18,
            font=dict(size=12)
        )
        
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Pas assez de données pour afficher la heatmap avec les filtres sélectionnés.")


def main():
    apply_dashboard_styles()
    render_header()
    
    try:
        df = get_jobs_from_database()
        df = prepare_dataframe(df)
        
        df_filtered = apply_filters(df)
        
        if len(df_filtered) == 0:
            st.warning("Aucune donnée ne correspond aux filtres sélectionnés.")
            return
        
        render_kpis(df_filtered)
        st.markdown("<br>", unsafe_allow_html=True)
        
        render_section_header("Analyses Principales")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            render_city_chart(df_filtered)
        
        with col2:
            render_skills_chart(df_filtered)
            
        render_section_header("Heatmap Skills par Métier ")
        render_heatmap(df_filtered)
        
        render_section_header("Carte des offres en France")
        render_map(df_filtered)
        
        render_section_header("Remote vs Présentiel")
        render_remote_comparison(df_filtered)
        
        
        render_footer()
        
    except Exception as e:
        st.error(f"Erreur lors du chargement des données : {str(e)}")
        st.info("Vérifiez que la base de données est accessible et contient des données.")


if __name__ == "__main__":
    main()