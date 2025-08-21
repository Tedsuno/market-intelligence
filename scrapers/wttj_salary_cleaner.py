from database.connection import get_db
import re
from database.models import Job
import pandas as pd

def clean_text(text):
    text = text.replace(",", ".")
    text = text.replace(" ", "") 
    text = text.replace("\xa0", "")
    return text.strip()

def _clip(v):
    if v is None or pd.isna(v):
        return None  
    try:
        v = float(v)
    except (ValueError, TypeError):
        return None
    if v <= 0:
        return None
    if 200_000 < v < 20_000_000:
        v = v / 1000
    elif v > 20_000_000:  
        return None
    return int(min(max(v, 15_000), 200_000))

def k_to_euros(x):
    if not x or pd.isna(x):
        return None
    try:
        v = float(str(x).replace(" ", "").replace(",", "."))
        return int(v * 1000) if v < 1000 else int(v)
    except (ValueError, TypeError):
        return None


def parse_salary(salary_text):
    salary_text = clean_text(salary_text)
    res = {}
    salary_min = None
    salary_max = None

    # Cas 1 : 38K à 45K €
    regex = re.compile(r'(\d+(?:\.\d+)?)\s*[kK]\s*à\s*(\d+(?:\.\d+)?)\s*[kK]\s*€')
    match = regex.match(salary_text)
    if match:
        salary_min = k_to_euros(match.group(1))
        salary_max = k_to_euros(match.group(2))

    # Cas 2 : 800 à 1 000 € par mois
    elif re.match(r'(\d+)\s*à\s*(\d+)\s*€\s*par\s*mois', salary_text):
        match = re.match(r'(\d+)\s*à\s*(\d+)\s*€\s*par\s*mois', salary_text)
        salary_min = convert_to_annual(int(match.group(1)), is_monthly=True)
        salary_max = convert_to_annual(int(match.group(2)), is_monthly=True)
    # Cas 3 : < 6 € par jour
    elif re.match(r'<\s*(\d+(?:\.\d+)?)\s*€\s*par\s*jour', salary_text):
        match = re.match(r'<\s*(\d+(?:\.\d+)?)\s*€\s*par\s*jour', salary_text)
        salary_min = 0
        salary_max = convert_to_annual(float(match.group(1)) * 220)  # 220 jours ouvrés/an
    # Cas 4 : ≥ 40K €
    elif re.match(r'≥\s*(\d+(?:\.\d+)?)\s*[kK]\s*€', salary_text):
        match = re.match(r'≥\s*(\d+(?:\.\d+)?)\s*[kK]\s*€', salary_text)
        salary_min = k_to_euros(match.group(1))
        salary_max = None

    # Cas 5 : salaire unique (1,5K € par mois)
    elif re.match(r'(\d+(?:\.\d+)?)\s*[kK]\s*€\s*par\s*mois', salary_text):
        match = re.match(r'(\d+(?:\.\d+)?)\s*[kK]\s*€\s*par\s*mois', salary_text)
        v = k_to_euros(match.group(1))
        salary_min = salary_max = convert_to_annual(v, is_monthly=True)

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
        salary_min = k_to_euros(match.group(1))
        salary_max = k_to_euros(match.group(2))

    res = {"salary_min": _clip(salary_min), "salary_max": _clip(salary_max)}
    return res

    
    
def convert_to_annual(amount, is_monthly=False) :
    if not amount or pd.isna(amount):
        return None
    try:
        return int(amount * 12) if is_monthly else int(amount)
    except (ValueError, TypeError):
        return None
    

