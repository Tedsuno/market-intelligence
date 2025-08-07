import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wttj_scraper import WTTJScraper

scraper = WTTJScraper()
url = "https://www.welcometothejungle.com/fr/jobs?query=python"

try:
    jobs = scraper.scrape_multiple_pages(url, 15)
    scraper.save_to_database(jobs)
    print("SAUVEGARDE TERMINE")
    
finally:
    scraper.close()