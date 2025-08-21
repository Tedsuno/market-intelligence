import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from wttj_scraper import WTTJScraper

scraper = WTTJScraper()
url = "https://www.welcometothejungle.com/fr/jobs?query=data_stage"


try:
    print("Vidage de la table...")
    scraper.clear_database()
    print("Table vidée !")
    
    jobs = scraper.scrape_multiple_pages(url, 3)
    scraper.save_to_database(jobs)
    print("SAUVEGARDE TERMINE")
    
finally:
    scraper.close()