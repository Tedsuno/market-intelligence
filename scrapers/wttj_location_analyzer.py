import requests
import time
import re

def clean_location(location_text):
    if not location_text:
        return {
            "clean_location": None,
            "is_remote": False,
            "original": location_text
        }
    first_location = location_text.split(",")[0].strip()
    ville_lower = first_location.lower()
    remote_keywords = ["remote", "télétravail", "full remote", "100% remote", "télétravail complet"]
    is_remote = any(keyword in ville_lower for keyword in remote_keywords)
    if is_remote:
        return {
            "clean_location": "Remote",
            "is_remote": True,
            "original": location_text
        }
    clean_ville = first_location.strip().title()   
    return {
        "clean_location": clean_ville,
        "is_remote": False,
        "original": location_text
    }

def geocode_location(city):
    if not city or city == "Remote":
        return {
            "latitude": None,
            "longitude": None,
            "quality": "remote",
            "display_name": "Remote"
        }
    
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": city,
        "format": "json",
        "countrycodes": "FR",
        "limit": 1,
        "addressdetails": 1
    }
    headers = {
        'User-Agent': 'JobScraper/1.0 (Python requests; contact@example.com)'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        time.sleep(1) 
        
        if response.status_code == 200:
            data = response.json()
            
            if data: 
                result = data[0]
                return {
                    "latitude": float(result["lat"]),
                    "longitude": float(result["lon"]),
                    "quality": "exact",
                    "display_name": result.get("display_name", city)
                }
            else:
                return {
                    "latitude": None,
                    "longitude": None,
                    "quality": "not_found",
                    "display_name": city
                }
        else:
            return {
                "latitude": None,
                "longitude": None,
                "quality": "api_error",
                "display_name": city
            }
            
    except requests.exceptions.RequestException as e:
        return {
            "latitude": None,
            "longitude": None,
            "quality": "network_error",
            "display_name": city
        }

def process_location(location_text):
    cleaned = clean_location(location_text)
    if cleaned["is_remote"]:
        return {
            "original": cleaned["original"],
            "clean_location": cleaned["clean_location"],
            "is_remote": True,
            "latitude": None,
            "longitude": None,
            "quality": "remote",
            "display_name": "Remote"
        }
    else:
        geocoded = geocode_location(cleaned["clean_location"])
        return {
            "original": cleaned["original"],
            "clean_location": cleaned["clean_location"],
            "is_remote": False,
            "latitude": geocoded["latitude"],
            "longitude": geocoded["longitude"],
            "quality": geocoded["quality"],
            "display_name": geocoded["display_name"]
        }