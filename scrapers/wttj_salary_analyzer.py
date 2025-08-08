import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.connection import get_db
from database.models import Job
from collections import Counter

def get_all_salaries() :
    db=get_db()
    salary=db.query(Job).filter(Job.salary!="N/A").all()
    return salary

def extract_salary_texts(jobs_list) :
    list_salary_text=[]
    for job in jobs_list:
        list_salary_text.append(job.salary)
    return list_salary_text

def analyze_patterns(salary_texts) :
    pattern=Counter(salary_texts)
    for item, count in pattern.most_common() :
        print(f"{item} -> {count} occurences")

def main():
    salary=get_all_salaries()
    e=extract_salary_texts(salary)
    analyze_patterns(e)

main()