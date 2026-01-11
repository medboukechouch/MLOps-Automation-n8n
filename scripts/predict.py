#!/usr/bin/env python3
"""
Script de prédiction autonome
Prédit les prix à partir des données dans Google Sheets
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from src.sheets_handler import SheetsHandler, prepare_output
from src.preprocessor import DataPreprocessor
from src.models import PricePredictor
from configs.config import MODEL_DIR, ENCODER_FILE, SCALER_FILE, FEATURES_COLUMNS_FILE
from src.utils import get_logger

logger = get_logger(__name__)


def main():
    """Lance les prédictions"""
    try:
        logger.info("=== Démarrage des prédictions ===")
        
        # Lire les données
        logger.info("Lecture des données...")
        handler = SheetsHandler()
        df = handler.read_input()
        
        # Prétraitement
        logger.info("Prétraitement...")
        preprocessor = DataPreprocessor()
        
        # Charger les transformateurs
        encoder_path = Path(MODEL_DIR) / ENCODER_FILE
        scaler_path = Path(MODEL_DIR) / SCALER_FILE
        features_path = Path(MODEL_DIR) / FEATURES_COLUMNS_FILE
        
        preprocessor.load_transformers(encoder_path, scaler_path, features_path)
        
        # Prétraiter
        df_clean = preprocessor.preprocess(df)
        df_prepared, prix_reel = preprocessor.encode_and_scale(df_clean, fit=False)
        
        # Prédictions
        logger.info("Génération des prédictions...")
        predictor = PricePredictor()
        predictions = predictor.predict(df_prepared)
        
        # Préparer la sortie
        output_df = prepare_output(df_clean, predictions, prix_reel)
        
        # Écrire dans Google Sheets
        handler.write_output(output_df, worksheet_name="Predictions")
        
        logger.info("✅ Prédictions générées et écrites avec succès!")
        logger.info(f"   {len(output_df)} prédictions écrites")
    
    except Exception as e:
        logger.error(f"Erreur critique: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
