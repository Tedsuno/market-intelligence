# Market Intelligence - Analyse des Offres d'Emploi Tech

Analyse automatisée de 500+ offres d'emploi tech pour détecter les tendances salariales et les compétences émergentes en temps réel.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)](https://postgresql.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io)

## Aperçu

Ce projet crée un dashboard intelligent qui scrape automatiquement les offres d'emploi tech, extrait les compétences et salaires via NLP, analyse les tendances du marché en temps réel, et visualise les insights dans un dashboard interactif.

**Valeur ajoutée :** Analyser 500+ offres d'emploi tech en temps réel pour détecter les tendances salariales et les compétences qui explosent sur le marché.

## Architecture

```
Sites Emploi → Scraping → Traitement NLP → PostgreSQL → Dashboard Analytics
    WTTJ        Python       spaCy         Données        Streamlit
   Indeed    BeautifulSoup   TextBlob     Structurées    Visualisations
```

## Technologies

- **Backend :** Python, PostgreSQL
- **Scraping :** BeautifulSoup, Scrapy, Selenium
- **NLP :** spaCy, TextBlob
- **Data :** Pandas, NumPy
- **Frontend :** Streamlit, Plotly
- **Base de données :** PostgreSQL

## Démarrage Rapide

### Prérequis
- Python 3.8+
- PostgreSQL 13+

### Installation

```bash
git clone https://github.com/Tedsuno/market-intelligence
cd market-intelligence

python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

pip install -r requirements.txt

# Configuration base de données
createdb market_intelligence
cp .env.example .env
# Éditer .env avec votre configuration

# Lancement
python main.py
streamlit run dashboard/app.py
```

## Structure du Projet

```
├── config/
│   └── settings.py          # Configuration globale
├── dashboard/
│   └── app.py              # Dashboard Streamlit
├── database/
│   ├── connection.py       # Connexion PostgreSQL
│   ├── models.py          # Modèles de données
│   └── utils.py           # Utilitaires base
├── scrapers/
│   ├── wttj_scraper.py           # Scraper principal
│   ├── wttj_pipeline.py          # Pipeline de traitement
│   ├── wttj_salary_analyzer.py   # Extraction salaires
│   ├── wttj_location_analyzer.py # Analyse localisation
│   └── wttj_skills_extractors.py # Extraction compétences
├── main.py                 # Point d'entrée
└── requirements.txt        # Dépendances
```

## Fonctionnalités

### Implémenté
- Scraping automatique des offres (Welcome to the jungle)
- Extraction et nettoyage des salaires
- Analyse géographique des localisations
- Stockage PostgreSQL
- Pipeline de traitement des données
- Extraction de compétences par NLP
- Dashboard Streamlit interactif
- Analyse des tendances
- Visualisations avancées

### Roadmap
- Support multi-sites (Welcome to the jungle)
- Prédictions par machine learning
- API REST
- Rapports automatisés

## Planning de Développement

**Jour 1-2 :** Infrastructure, scraping, schéma base de données
**Jour 3 :** Traitement NLP, extraction compétences, nettoyage données
**Jour 4 :** Analyse tendances, calculs statistiques
**Jour 5 :** Développement dashboard, déploiement, documentation

## Contribution

1. Forker le projet
2. Créer une branche feature (`git checkout -b feature/NouvelleFonctionnalite`)
3. Commiter les changements (`git commit -m 'Ajout NouvelleFonctionnalite'`)
4. Pousser vers la branche (`git push origin feature/NouvelleFonctionnalite`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

