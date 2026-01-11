"""
Configuration centralisée pour le projet Property Price Predictor
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Chemins
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / "src"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
CONFIGS_DIR = BASE_DIR / "configs"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"

# Google Sheets
SHEET_NAME = os.getenv("SHEET_NAME", "Scraped Properties")
INPUT_WORKSHEET_NAME = os.getenv("INPUT_WORKSHEET_NAME", "Feuille 1")
OUTPUT_WORKSHEET_NAME = os.getenv("OUTPUT_WORKSHEET_NAME", "Predictions")
SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH", str(CONFIGS_DIR / "service_account.json"))

# n8n Webhook
WEBHOOK_URL = os.getenv("WEBHOOK_URL", None)
SEND_TO_WEBHOOK = WEBHOOK_URL is not None

# Scraping
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH", "C:/webdrivers/chromedriver.exe")
BASE_URL = os.getenv("BASE_URL", "https://www.mubawab.ma/fr/sc/appartements-a-vendre")
MAX_ADS = int(os.getenv("MAX_ADS", "100000"))

# Models
MODEL_DIR = os.getenv("MODEL_DIR", str(MODELS_DIR))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# === Configuration de scraping ===
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
]

EXTRAS_LIST = [
    "Ascenseur", "Concierge", "Sécurité", "Porte blindée", "Garage", "Terrasse", 
    "Étage du bien", "Jardin", "Cuisine équipée", "Réfrigérateur", "Four", 
    "Machine à laver", "Climatisation", "Chauffage central", "Façade extérieure", 
    "Antenne parabolique", "Double vitrage", "Salon Marocain", "Salon européen", 
    "Meublé", "Chambre rangement", "Vue sur mer", "Vue sur les montagnes"
]

# === Modèles ML disponibles ===
MODELS = {
    "Linear_Regression": "modele_Linear_Regression.pkl",
    "Random_Forest": "modele_Random_Forest.pkl",
    "Gradient_Boosting": "modele_Gradient_Boosting.pkl",
    "SVR": "modele_SVR.pkl"
}

# === Fichiers encoder et scaler ===
ENCODER_FILE = "encoder.pkl"
SCALER_FILE = "scaler.pkl"
FEATURES_COLUMNS_FILE = "features_columns.pkl"

# === Colonnes à supprimer ===
COLUMNS_TO_DROP = [
    "titre", "url", "prix", "type de bien", "étage du bien", "Porte blindée", 
    "Jardin", "Réfrigérateur", "Four", "type_bien", "Machine à laver", 
    "Façade extérieure", "Antenne parabolique", "Salon Marocain", "Meublé"
]

# === Colonnes numériques ===
NUMERICAL_COLUMNS = ['surface', 'pièces', 'chambres', 'salles_de_bain']
CATEGORICAL_COLUMNS = ['ville', 'zone']

# === Configuration de validation ===
PRICE_MIN = 10000  # Prix minimum accepté en DH
PRICE_MAX = 100000000  # Prix maximum accepté en DH
SURFACE_MIN = 10  # Surface minimum en m²
SURFACE_MAX = 10000  # Surface maximum en m²
