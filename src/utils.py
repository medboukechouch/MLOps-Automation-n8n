"""
Utilitaires et fonctions communes
"""

import logging
import re
import os
from pathlib import Path
from configs.config import LOG_LEVEL

# === Configuration du logging ===
logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


class PropertyScraper:
    """Classe utilitaire pour le scraping de propriétés"""
    
    @staticmethod
    def extract_number(text):
        """Extrait le premier nombre d'un texte"""
        if not text or pd.isna(text):
            return None
        match = re.search(r'\d+', str(text).replace(',', ''))
        return int(match.group()) if match else None
    
    @staticmethod
    def extract_price(prix_str):
        """Nettoie et convertit le prix en DH"""
        if pd.isna(prix_str):
            return None
        
        prix_str = str(prix_str)
        
        if 'DH' in prix_str:
            match = re.search(r'(\d[\d\s]*) ?DH', prix_str)
            if match:
                return float(match.group(1).replace(" ", ""))
        elif 'EUR' in prix_str:
            match = re.search(r'(\d[\d\s]*) ?EUR', prix_str)
            if match:
                return float(match.group(1).replace(" ", "")) * 10.5
        
        try:
            return float(prix_str)
        except:
            return None
    
    @staticmethod
    def extract_surface(val):
        """Extrait et convertit la surface en m²"""
        if pd.isna(val):
            return None
        digits = re.sub(r'\D', '', str(val))
        return int(digits) if digits else None


class DataValidator:
    """Classe pour la validation des données"""
    
    @staticmethod
    def is_valid_price(price, min_price=10000, max_price=100000000):
        """Vérifie si le prix est valide"""
        if pd.isna(price):
            return False
        try:
            price = float(price)
            return min_price <= price <= max_price
        except:
            return False
    
    @staticmethod
    def is_valid_surface(surface, min_surface=10, max_surface=10000):
        """Vérifie si la surface est valide"""
        if pd.isna(surface):
            return False
        try:
            surface = float(surface)
            return min_surface <= surface <= max_surface
        except:
            return False
    
    @staticmethod
    def is_valid_rooms(rooms):
        """Vérifie si le nombre de pièces est valide"""
        if pd.isna(rooms):
            return True
        try:
            return 0 <= int(rooms) <= 20
        except:
            return False


def ensure_directory(path):
    """Crée un répertoire s'il n'existe pas"""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def get_logger(name):
    """Retourne un logger configuré"""
    return logging.getLogger(name)


# Import pandas ici pour éviter les imports circulaires
try:
    import pandas as pd
except ImportError:
    logger.warning("pandas not installed")
    pd = None
