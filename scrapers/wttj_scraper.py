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
                
                entreprise_elem = job.find('span', class_='sc-izXThL fFdRYJ sc-dQnwSX iNIwQv wui-text')
                entreprise = entreprise_elem.get_text(strip=True) if entreprise_elem else "N/A"
                
                location_elem = job.find('span', class_='sc-raRIu jtcPcm')
                location = location_elem.get_text(strip=True) if location_elem else "N/A"
                
                lien_elem = job.find('a', class_='sc-gSmbis fNmfaI')
                lien = lien_elem.get('href') if lien_elem else "N/A"
                
                infos = {
                    "title": title,
                    "entreprise": entreprise,
                    "location": location,
                    "lien": lien
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
                new_job.source="WTTJ"
                new_job.scraped_at=datetime.now()
                db.add(new_job)
                db.commit()
            except Exception as e:
                print(f"Erreur lors de la sauvegarde: {e}")
                db.session.rollback()
        db.close() 
    
    def close(self):
        if self.driver:
            self.driver.quit()