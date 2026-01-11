"""
Module de scraping des propriétés immobilières
"""

import time
import random
import re
import json
import requests
from pathlib import Path
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from configs.config import CHROMEDRIVER_PATH, BASE_URL, MAX_ADS, USER_AGENTS, EXTRAS_LIST, WEBHOOK_URL
from src.utils import get_logger, PropertyScraper, DataValidator

logger = get_logger(__name__)


class PropertyScraper:
    """Scrape les propriétés immobilières depuis Mubawab.ma"""
    
    def __init__(self, base_url=BASE_URL, max_ads=MAX_ADS, chromedriver_path=CHROMEDRIVER_PATH):
        self.base_url = base_url
        self.max_ads = max_ads
        self.chromedriver_path = chromedriver_path
        self.driver = None
        self.data = []
        self.validator = DataValidator()
    
    def setup_driver(self):
        """Initialise le driver Selenium"""
        logger.info("Initialisation du driver Chrome...")
        try:
            options = Options()
            options.add_argument("--window-size=1920,1080")
            options.add_argument("user-agent=" + random.choice(USER_AGENTS))
            options.add_argument("--disable-blink-features=AutomationControlled")
            
            service = Service(self.chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=options)
            logger.info("Driver Chrome initialisé avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation du driver: {e}")
            raise
    
    def safe_extract(self, selectors):
        """Extrait le texte de manière sécurisée"""
        for selector in selectors:
            try:
                element = WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                return element.text.strip()
            except:
                continue
        return None
    
    def extract_property(self):
        """Extrait les informations d'une propriété"""
        property_data = {}
        
        try:
            # Titre
            property_data['titre'] = self.safe_extract([
                '.listing-title', '.ad-title', 'h1'
            ])
            
            # Prix
            price_text = self.safe_extract([
                '.price', '.listing-price', '[data-price]'
            ])
            property_data['prix'] = price_text
            
            # Surface
            surface_text = self.safe_extract([
                '.surface', '[data-surface]', '.area'
            ])
            property_data['surface'] = surface_text
            
            # Pièces, chambres, salles de bain
            property_data['pièces'] = self.safe_extract(['.rooms', '[data-rooms]'])
            property_data['chambres'] = self.safe_extract(['.bedrooms', '[data-bedrooms]'])
            property_data['salles_de_bain'] = self.safe_extract(['.bathrooms', '[data-bathrooms]'])
            
            # Localisation
            property_data['localisation'] = self.safe_extract([
                '.location', '[data-location]', '.address'
            ])
            
            # URL
            try:
                link = self.driver.find_element(By.CSS_SELECTOR, 'a[href*="/listing/"]')
                property_data['url'] = link.get_attribute('href')
            except:
                property_data['url'] = None
            
            # Type de bien
            property_data['type_bien'] = self.safe_extract([
                '.property-type', '[data-type]'
            ])
            
            # Extras (équipements)
            for extra in EXTRAS_LIST:
                try:
                    element = self.driver.find_element(By.XPATH, f"//*[contains(text(), '{extra}')]")
                    property_data[extra] = 1
                except:
                    property_data[extra] = 0
            
            return property_data
        
        except Exception as e:
            logger.warning(f"Erreur lors de l'extraction d'une propriété: {e}")
            return None
    
    def scrape(self):
        """Lance le scraping"""
        logger.info(f"Démarrage du scraping depuis {self.base_url}")
        
        try:
            self.setup_driver()
            self.driver.get(self.base_url)
            time.sleep(3)
            
            ads_count = 0
            page = 1
            
            while ads_count < self.max_ads:
                logger.info(f"Scraping page {page}...")
                
                try:
                    # Attendre que les annonces se chargent
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.listing-item'))
                    )
                    
                    listings = self.driver.find_elements(By.CSS_SELECTOR, '.listing-item')
                    
                    for listing in listings:
                        if ads_count >= self.max_ads:
                            break
                        
                        try:
                            listing.click()
                            time.sleep(1)
                            
                            property_data = self.extract_property()
                            if property_data:
                                self.data.append(property_data)
                                ads_count += 1
                                logger.info(f"Annonce {ads_count} extraite")
                                
                                # Envoyer à webhook si configuré
                                if WEBHOOK_URL:
                                    self.send_to_webhook(property_data)
                        
                        except Exception as e:
                            logger.warning(f"Erreur sur une annonce: {e}")
                            continue
                    
                    # Aller à la page suivante
                    try:
                        next_btn = self.driver.find_element(By.CSS_SELECTOR, 'a.next-page')
                        next_btn.click()
                        time.sleep(2)
                        page += 1
                    except:
                        logger.info("Dernière page atteinte")
                        break
                
                except Exception as e:
                    logger.error(f"Erreur lors du scraping de la page {page}: {e}")
                    break
            
            logger.info(f"Scraping terminé! {ads_count} annonces collectées")
            return pd.DataFrame(self.data)
        
        finally:
            if self.driver:
                self.driver.quit()
    
    def send_to_webhook(self, data):
        """Envoie les données à un webhook n8n"""
        try:
            response = requests.post(WEBHOOK_URL, json=data, timeout=5)
            if response.status_code == 200:
                logger.info("Données envoyées au webhook avec succès")
            else:
                logger.warning(f"Erreur webhook: {response.status_code}")
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi au webhook: {e}")
    
    def to_csv(self, filepath):
        """Sauvegarde les données en CSV"""
        df = pd.DataFrame(self.data)
        df.to_csv(filepath, index=False, encoding='utf-8')
        logger.info(f"Données sauvegardées dans {filepath}")
        return df


if __name__ == "__main__":
    scraper = PropertyScraper()
    df = scraper.scrape()
    scraper.to_csv("data/raw/properties.csv")
