import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wttj_scraper import WTTJScraper

scraper = WTTJScraper()
url = "https://www.welcometothejungle.com/fr/jobs?query=python"


try:
    print("Suppression de la colonne salary...")
    scraper.drop_salary_column()
    
finally:
    scraper.close()