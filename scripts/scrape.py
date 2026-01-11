#!/usr/bin/env python3
"""
Script de scraping autonome
Collecte les données immobilières et les envoie à Google Sheets
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper import PropertyScraper
from src.sheets_handler import SheetsHandler
from src.utils import get_logger

logger = get_logger(__name__)


def main():
    """Scrape et envoie les données"""
    try:
        logger.info("=== Démarrage du scraping ===")
        
        # Scraper les propriétés
        scraper = PropertyScraper()
        df = scraper.scrape()
        
        if df is not None and len(df) > 0:
            logger.info(f"{len(df)} propriétés collectées")
            
            # Envoyer à Google Sheets
            try:
                handler = SheetsHandler()
                handler.write_output(df, worksheet_name="Scraped Properties")
                logger.info("✅ Scraping et upload réussi!")
            except Exception as e:
                logger.error(f"Erreur Google Sheets: {e}")
                # Sauvegarder en CSV de secours
                df.to_csv("data/raw/backup_properties.csv", index=False)
                logger.info("Données sauvegardées en CSV de secours")
        else:
            logger.warning("Aucune propriété n'a été collectée")
    
    except Exception as e:
        logger.error(f"Erreur critique: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
