import spacy # type: ignore

def get_skills_categories():
    
    skills = {
        "langages_programmation": [
            "Python", "R", "SQL", "JavaScript", "Java", "C++", "PHP", "Ruby", "Go", "Rust", 
            "TypeScript", "C#", "Swift", "Kotlin", "Scala", "MATLAB", "SAS", "Julia", "Spark",
            "PySpark", "Hive", "Pig", "HiveQL", "T-SQL", "PL/SQL", "NoSQL"
        ],
        
        "frameworks_web": [
            "Django", "Flask", "React", "Vue", "Angular", "Spring", "Laravel", 
            "Express", "Rails", ".NET", "FastAPI", "Symfony", "Bootstrap", "jQuery",
            "Streamlit", "Dash", "Gradio", "Shiny"
        ],
        
        "ml_ai_frameworks": [
            "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "XGBoost", "LightGBM",
            "CatBoost", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly",
            "OpenCV", "NLTK", "spaCy", "Transformers", "Hugging Face", "MLflow",
            "Kubeflow", "Apache Spark", "Dask", "Ray", "AutoML", "H2O", "DataRobot"
        ],
        
        "bases_donnees": [
            "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle", 
            "Elasticsearch", "Cassandra", "MariaDB", "DynamoDB", "ClickHouse",
            "BigQuery", "Redshift", "Snowflake", "Databricks", "Apache Hive",
            "HBase", "Neo4j", "ArangoDB", "InfluxDB", "TimescaleDB"
        ],
        
        "outils_bi_visualisation": [
            "Power BI", "Tableau", "Looker", "QlikView", "QlikSense", "Metabase",
            "Grafana", "Superset", "DataStudio", "Excel", "Google Sheets",
            "Spotfire", "SAS Visual Analytics", "IBM Cognos", "MicroStrategy",
            "Sisense", "Chartio", "Mode Analytics", "Periscope", "Domo"
        ],
        
        "cloud_platforms": [
            "AWS", "Azure", "GCP", "Google Cloud", "IBM Cloud", "Alibaba Cloud",
            "DigitalOcean", "Heroku", "Vercel", "Netlify"
        ],
        
        "aws_services": [
            "S3", "EC2", "Lambda", "Redshift", "Athena", "Glue", "EMR", 
            "SageMaker", "Kinesis", "DynamoDB", "RDS", "CloudFormation",
            "Step Functions", "Batch", "ECS", "EKS"
        ],
        
        "azure_services": [
            "Azure Data Factory", "Azure Synapse", "Azure Machine Learning",
            "Azure Databricks", "Cosmos DB", "Azure SQL", "Power Platform",
            "Azure Functions", "Azure Storage", "Azure DevOps"
        ],
        
        "gcp_services": [
            "BigQuery", "Dataflow", "Dataproc", "Cloud ML Engine", "Vertex AI",
            "Cloud Storage", "Cloud SQL", "Pub/Sub", "Datalab", "Cloud Functions"
        ],
        
        "outils_etl_data_pipeline": [
            "Apache Airflow", "Luigi", "Prefect", "Dagster", "Apache Beam",
            "Talend", "Informatica", "SSIS", "Pentaho", "Alteryx", "Fivetran",
            "Stitch", "Airbyte", "dbt", "Apache NiFi", "Kafka", "Apache Kafka",
            "Confluent", "Pulsar", "RabbitMQ"
        ],
        
        "outils_devops_mlops": [
            "Docker", "Kubernetes", "Git", "GitHub", "GitLab", "Jenkins", 
            "Terraform", "Ansible", "CircleCI", "Travis CI", "Azure DevOps",
            "MLflow", "DVC", "Weights & Biases", "Neptune", "ClearML",
            "Kubeflow", "Seldon", "BentoML", "TFX", "Apache Beam"
        ],
        
        "methodologies_data": [
            "CRISP-DM", "KDD", "Agile", "Scrum", "Kanban", "DevOps", "MLOps",
            "DataOps", "LEAN", "Six Sigma", "Design Thinking", "A/B Testing",
            "Statistical Testing", "Hypothesis Testing", "Cross-validation"
        ],
        
        "statistiques_maths": [
            "Statistiques", "Probabilités", "Algèbre linéaire", "Calcul", 
            "Optimisation", "Théorie des graphes", "Analyse multivariée",
            "Séries temporelles", "Econométrie", "Biostatistiques", "ANOVA",
            "Régression", "Classification", "Clustering", "PCA", "SVD"
        ],
        
        "domaines_ia_ml": [
            "Machine Learning", "Deep Learning", "NLP", "Computer Vision", 
            "Reinforcement Learning", "MLOps", "AutoML", "Feature Engineering",
            "Model Selection", "Hyperparameter Tuning", "Ensemble Methods",
            "Neural Networks", "CNN", "RNN", "LSTM", "GAN", "Transformer",
            "BERT", "GPT", "LLM", "Generative AI", "Explainable AI", "XAI"
        ],
        
        "outils_bureautique": [
            "Excel", "Google Sheets", "Word", "PowerPoint", "Outlook", 
            "SharePoint", "Teams", "Slack", "Notion", "Confluence",
            "Jira", "Trello", "Asana", "Monday.com"
        ],
        
        "certifications": [
            "AWS Certified", "Azure Certified", "GCP Certified", "Tableau Certified",
            "Power BI Certified", "SAS Certified", "Databricks Certified",
            "Snowflake Certified", "Cloudera Certified", "Hortonworks Certified"
        ],
        
        "soft_skills": [
            "Leadership", "Communication", "Problem Solving", "Critical Thinking",
            "Project Management", "Team Work", "Analytical Thinking", 
            "Business Acumen", "Stakeholder Management", "Presentation Skills"
        ],
        
        "formats_donnees": [
            "JSON", "XML", "CSV", "Parquet", "Avro", "ORC", "Arrow", 
            "HDF5", "NetCDF", "YAML", "TOML", "Protocol Buffers"
        ],
        
        "gouvernance_qualite": [
            "Data Governance", "Data Quality", "Data Lineage", "Data Catalog",
            "Master Data Management", "MDM", "Data Privacy", "GDPR", "CCPA",
            "Data Security", "Metadata Management", "Business Glossary",
            "Data Stewardship", "Data Architecture"
        ],
        
        "secteurs_metiers": [
            "Finance", "Banking", "Insurance", "Retail", "E-commerce", 
            "Healthcare", "Pharma", "Automotive", "Telecommunications",
            "Energy", "Manufacturing", "Logistics", "Supply Chain",
            "Marketing", "Sales", "HR", "Operations"
        ]
    }
    
    return skills

def get_name_categories():
    jobs = {
        "data_jobs": [
            "Data Scientist", "Data Analyst", "Data Engineer", 
            "Analyste de données", "Scientifique des données",
            "ML Engineer", "BI Analyst",
        ],
        "dev_jobs": [
            "Développeur", "Developer", "Full Stack", 
            "Backend Developer", "Frontend Developer",
            "Software Engineer"
        ]
    }
    return jobs



def extract_skills_from_title(job_title) :
    nlp=spacy.load('fr_core_news_sm')
    res=[]
    skills_job=nlp(job_title)
    skills_dict = get_skills_categories() 
    all_skills = []                        
    for skill_list in skills_dict.values():  
        all_skills.extend(skill_list)  
    all_skills = [skill.lower() for skill in all_skills]       
    for skill_job in skills_job :
        if skill_job.lemma_.lower() in all_skills :
            res.append(skill_job.lemma_.lower())
    return list(set(res))

def extract_name_from_title(job_title):
    job_title_lower = job_title.lower()
    
    if any(word in job_title_lower for word in ["data scientist", "scientist","datascientist"]):
        return "Data Scientist"
    elif any(word in job_title_lower for word in ["data analyst","dataanalyst","dataanalyse","dataanalysis","dataanalyste"]):
        return "Data Analyst"
    elif any(word in job_title_lower for word in ["data engineer", "ingénieur data","dataengineer"]):
        return "Data Engineer"
    elif any(word in job_title_lower for word in ["business analyst", "bi analyst","buisness"]):
        return "BI Analyst"
    
    return "Autres métier data..."