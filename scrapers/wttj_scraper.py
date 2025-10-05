from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import sys
sys.path.append('..')
import time
from database.connection import get_db
from database.models import Job
from wttj_salary_cleaner import *
from wttj_skills_extractors import *
from wttj_location_analyzer import *
from wttj_seniority import *

class WTTJScraper():
    
    def __init__(self):
        options = Options()
        options.add_argument('--headless') 
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
    
    def get_page_html(self, url):
        try:
            self.driver.get(url)
            time.sleep(5)
            return self.driver.page_source
        except Exception as e:
            print(f"Erreur lors de la récupération de {url}: {e}")
            return None
    
    def extract_jobs_from_page(self, html):
        if not html:
            return []
            
        soup = BeautifulSoup(html, 'html.parser')
        job_containers = soup.find_all('li', {'data-testid': 'search-results-list-item-wrapper'})
        res = []
        
        for job in job_containers:
            try:
                title_elem = job.find('h2', class_='sc-izXThL fnsHVh wui-text')
                title = title_elem.get_text(strip=True) if title_elem else "N/A"
                
                entreprise_elem = job.find('span', class_='sc-izXThL fFdRYJ sc-fxgerm ZAtaP wui-text')
                if not entreprise_elem:
                    entreprise_elem = job.find('span', string=lambda x: x and len(x.strip()) > 2)
                    if not entreprise_elem:
                        entreprise_elem = job.find('div', class_=lambda x: x and any('company' in c.lower() for c in x))
                entreprise = entreprise_elem.get_text(strip=True) if entreprise_elem else "N/A"
                
                location_elem = job.find('span', class_='sc-gFGBys sdDDd')
                if not location_elem:
                    location_elem = job.find('span', string=lambda x: x and any(city in x for city in ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Lille', 'Bordeaux', 'Nantes', 'Strasbourg', 'Montpellier', 'Rennes']))
                    if not location_elem:
                        location_elem = job.find('span', string=lambda x: x and any(char.isdigit() for char in x) and len(x) < 50)
                location = location_elem.get_text(strip=True) if location_elem else "N/A"
                
                lien_elem = job.find('a', href=lambda x: x and '/jobs/' in x)
                if not lien_elem:
                    lien_elem = job.find('a', {'role': 'link'})
                lien = lien_elem.get('href') if lien_elem else "N/A"
                
                salary_elem = job.find('span', class_="sc-brzPDJ kVqhOm")
                if salary_elem and "Salaire" in salary_elem.get_text():
                    parent_text = salary_elem.parent.get_text()
                    salary = parent_text.replace("Salaire :", "").strip()
                else:
                    salary = "N/A"
                parse = parse_salary(salary)
                
                if lien != "N/A" and not lien.startswith('http'):
                    lien = "https://www.welcometothejungle.com" + lien
                    
                if lien == "N/A":
                    print(f"Pas de lien trouvé pour: {title}")
                    continue
                    
                print(f"Traitement de: {title} - {lien}")
                link = self.get_page_html(lien)
                
                if not link:
                    print(f"Impossible de récupérer le contenu de: {lien}")
                    continue
                    
                soup2 = BeautifulSoup(link, 'html.parser')
                poste_elem = soup2.find('div', {'id': 'the-position-section'})
                description = poste_elem.get_text(strip=True) if poste_elem else "N/A"
                skills = extract_skills_from_title(description)
                
                locations = process_location(location)
                
                contract_elem = job.find('div', class_='sc-fibHhp gqJNlp')
                if contract_elem:
                    contract_text = contract_elem.get_text(strip=True)
                    contract = contract_text if contract_text else "N/A"
                else:
                    contract = "N/A"
                
                seniority = exctract_seniority_from_title(title)
                if seniority == "N/A":
                    seniority = exctract_seniority_from_salary(parse["salary_min"])
                
                is_remote = job.find('span', string=lambda t: t and "Télétravail" in t)
                if is_remote:
                    is_remote_text = is_remote.get_text(strip=True)
                    if is_remote_text == "Télétravail fréquent" or \
                    is_remote_text == "Télétravail occasionnel" or is_remote_text == "Télétravail total":
                        is_remote = True
                    else:
                        is_remote = False
                else:
                    is_remote = False
                
                job_name = extract_name_from_title(title)
                        
                infos = {
                    "title": title,
                    "entreprise": entreprise,
                    "location": locations["clean_location"],
                    "lien": lien,
                    "salary_min": convert_to_annual(parse["salary_min"]),
                    "salary_max": convert_to_annual(parse["salary_max"]),
                    "skills": skills,
                    "is_remote": is_remote,
                    "latitude": locations["latitude"],
                    "longitude": locations["longitude"],
                    "geocoding_quality": locations["quality"],
                    "contract": contract,
                    "seniority": seniority,
                    "job_name": job_name
                }
                res.append(infos)
                
            except Exception as e:
                print(f"Erreur lors de l'extraction d'un job: {e}")
                continue
        
        return res
    
    def scrape_multiple_pages(self, base_url, max_pages=5):
        offers = []
        for i in range(1, max_pages + 1):
            print(f"Scraping page {i}/{max_pages}...")
            url = base_url + f"&page={i}"
            html = self.get_page_html(url)
            if html:
                page = self.extract_jobs_from_page(html)
                offers.extend(page)
                print(f"Page {i}: {len(page)} jobs trouvés")
            time.sleep(2)
        return offers
    
    def save_to_database(self, jobs_list):
        db = get_db()
        for offer in jobs_list:
            try:
                new_job = Job()
                new_job.title = offer["title"]
                new_job.company = offer["entreprise"]
                new_job.location = offer["location"]
                new_job.url = offer["lien"]
                new_job.source = "WTTJ"
                new_job.scraped_at = datetime.now()
                new_job.salary_min = offer["salary_min"]
                new_job.salary_max = offer["salary_max"]
                new_job.skills = str(offer["skills"])
                new_job.latitude = offer["latitude"]
                new_job.longitude = offer["longitude"]
                new_job.is_remote = offer["is_remote"]
                new_job.geocoding_quality = offer["geocoding_quality"]
                new_job.contract_type = offer["contract"]
                new_job.seniority = offer["seniority"]
                new_job.job_name = offer["job_name"]
                db.add(new_job)
                db.commit()
            except Exception as e:
                print(f"Erreur lors de la sauvegarde: {e}")
                db.rollback()
        db.close()

    
    def close(self):
        if self.driver:
            self.driver.quit()
            
    def clear_database(self):
        db = get_db()
        try:
            db.query(Job).delete()
            db.commit()
            print("Table jobs vidée avec succès")
        except Exception as e:
            print(f"Erreur lors du vidage de la table: {e}")
            db.rollback()
        finally:
            db.close()