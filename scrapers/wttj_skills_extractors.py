import spacy # type: ignore

def get_skills_categories():
    
    skills = {
        "langages_programmation": [
            "Python", "JavaScript", "Java", "C++", "PHP", "Ruby", "Go", "Rust", 
            "TypeScript", "C#", "Swift", "Kotlin", "Scala", "R", "MATLAB"
        ],
        
        "frameworks": [
            "Django", "Flask", "React", "Vue", "Angular", "Spring", "Laravel", 
            "Express", "Rails", ".NET", "FastAPI", "Symfony", "Bootstrap", "jQuery"
        ],
        
        "bases_donnees": [
            "MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite", "Oracle", 
            "Elasticsearch", "Cassandra", "MariaDB", "DynamoDB"
        ],
        
        "outils_devops": [
            "Docker", "Kubernetes", "Git", "Jenkins", "AWS", "Azure", "GCP", 
            "Terraform", "Ansible", "GitLab", "CircleCI", "Prometheus"
        ],
        
        "soft_skills": [
            "Leadership", "Communication", "Autonomie", "Équipe", "Team", 
            "Gestion", "Innovation", "Créativité", "Rigueur", "Adaptabilité", 
            "Organisation", "Management"
        ],
        "competences_generales": [
            "développeur", "developer", "dev", "engineer", "ingénieur", 
            "lead", "senior", "junior", "architect", "consultant",
            "full-stack", "backend", "frontend", "devops", "data"
        ]
    }
    
    return skills

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