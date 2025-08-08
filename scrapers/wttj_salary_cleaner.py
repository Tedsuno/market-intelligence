from database.connection import get_db
import re
from database.models import Job

def clean_text(text):
    text = text.replace(",", ".")
    text = text.replace(" ", "") 
    text = text.replace("\xa0", "")
    return text.strip()

def parse_salary(salary_text):
    salary_text = clean_text(salary_text)
    res = {}
    salary_min = None
    salary_max = None

    # Cas 1 : 38K à 45K €
    regex = re.compile(r'(\d+(?:\.\d+)?)\s*[kK]\s*à\s*(\d+(?:\.\d+)?)\s*[kK]\s*€')
    match = regex.match(salary_text)
    if match:
        salary_min = float(match.group(1)) * 1000
        salary_max = float(match.group(2)) * 1000

    # Cas 2 : 800 à 1 000 € par mois
    elif re.match(r'(\d+)\s*à\s*(\d+)\s*€\s*par\s*mois', salary_text):
        match = re.match(r'(\d+)\s*à\s*(\d+)\s*€\s*par\s*mois', salary_text)
        salary_min = int(match.group(1))
        salary_max = int(match.group(2))

    # Cas 3 : < 6 € par jour
    elif re.match(r'<\s*(\d+(?:\.\d+)?)\s*€\s*par\s*jour', salary_text):
        match = re.match(r'<\s*(\d+(?:\.\d+)?)\s*€\s*par\s*jour', salary_text)
        salary_min = 0
        salary_max = float(match.group(1))

    # Cas 4 : ≥ 40K €
    elif re.match(r'≥\s*(\d+(?:\.\d+)?)\s*[kK]\s*€', salary_text):
        match = re.match(r'≥\s*(\d+(?:\.\d+)?)\s*[kK]\s*€', salary_text)
        salary_min = float(match.group(1)) * 1000
        salary_max = None

    # Cas 5 : salaire unique (1,5K € par mois)
    elif re.match(r'(\d+(?:\.\d+)?)\s*[kK]\s*€', salary_text):
        match = re.match(r'(\d+(?:\.\d+)?)\s*[kK]\s*€', salary_text)
        salary_min = salary_max = float(match.group(1)) * 1000

    # Cas 6 : valeurs en euros sans K → ex : 40 000 à 52 000 €
    elif re.match(r'(\d+(?:\s?\d+)*)\s*à\s*(\d+(?:\s?\d+)*)\s*€', salary_text):
        match = re.match(r'(\d+(?:\s?\d+)*)\s*à\s*(\d+(?:\s?\d+)*)\s*€', salary_text)
        salary_min = int(match.group(1).replace(" ", ""))
        salary_max = int(match.group(2).replace(" ", ""))

    # Cas 7 : salaire unique sans K → ex : 55 €
    elif re.match(r'(\d+(?:\.\d+)?)\s*€', salary_text):
        match = re.match(r'(\d+(?:\.\d+)?)\s*€', salary_text)
        salary_min = salary_max = float(match.group(1))

    # Cas 8 : valeurs mixtes K et décimales → ex : 1,5K à 2K €
    elif re.match(r'(\d+(?:\.\d+)?)\s*[kK]\s*à\s*(\d+(?:\.\d+)?)\s*[kK]', salary_text):
        match = re.match(r'(\d+(?:\.\d+)?)\s*[kK]\s*à\s*(\d+(?:\.\d+)?)\s*[kK]', salary_text)
        salary_min = float(match.group(1)) * 1000
        salary_max = float(match.group(2)) * 1000

    res = {
        "salary_min": int(salary_min) if salary_min is not None else None,
        "salary_max": int(salary_max) if salary_max is not None else None
    }
    return res

    
    
def convert_to_annual(amount, is_monthly=False) :
    if is_monthly : return amount*12 
    else : return amount
    

