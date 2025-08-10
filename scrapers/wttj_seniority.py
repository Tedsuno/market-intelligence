import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.connection import get_db
import spacy

def get_seniority() :
    return {
        "Junior" : ["junior", "débutant", "apprenti", "stage", "alternant"],
        "Experimente" : ["senior", "expert", "lead", "principal", "architect"],
        "Senior" :["manager", "chef", "directeur", "head", "team lead"],
    }

def exctract_seniority_from_title(title) :
    seniority=get_seniority()
    for s in title.split() :
        if s.lower() in seniority["Junior"] :
            return "Junior"
        elif s.lower() in seniority["Experimente"] :
            return "Experimente" 
        elif s.lower() in seniority["Senior"] :
            return "Senior" 
        else :
            return "N/A"

def exctract_seniority_from_salary(salary_min) :
    if salary_min is None:
        return "Unknown"
    elif salary_min < 35000:
        return "Junior"
    elif salary_min < 55000:
        return "Experimente" 
    elif salary_min < 75000:
        return "Senior"
    else:
        return "Expert/Lead"
    
print(exctract_seniority_from_title("Junior Product Manager (internship)"))