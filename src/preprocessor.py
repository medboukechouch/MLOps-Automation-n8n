"""
Module de prétraitement des données
"""

import re
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib

from configs.config import (
    NUMERICAL_COLUMNS, CATEGORICAL_COLUMNS, COLUMNS_TO_DROP,
    PRICE_MIN, PRICE_MAX, SURFACE_MIN, SURFACE_MAX
)
from src.utils import get_logger, PropertyScraper

logger = get_logger(__name__)


class DataPreprocessor:
    """Prétraite les données immobilières"""
    
    def __init__(self):
        self.encoder = None
        self.scaler = None
        self.features_columns = None
    
    def clean_price(self, prix):
        """Nettoie et convertit le prix en DH"""
        if pd.isna(prix):
            return np.nan
        
        prix_str = str(prix)
        
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
            return np.nan
    
    def clean_surface(self, val):
        """Extrait et convertit la surface"""
        if pd.isna(val):
            return np.nan
        digits = re.sub(r'\D', '', str(val))
        return int(digits) if digits else np.nan
    
    def extract_location(self, df):
        """Extrait zone et ville de la localisation"""
        zone_list, ville_list = [], []
        
        for loc in df.get('localisation', pd.Series()):
            if pd.isna(loc):
                ville_list.append("Unknown")
                zone_list.append("Unknown")
            elif ' à ' in str(loc):
                parts = str(loc).split(' à ', 1)
                zone_list.append(parts[0].strip())
                ville_list.append(parts[1].strip())
            else:
                ville_list.append(str(loc).strip())
                zone_list.append("Unknown")
        
        df['zone'] = zone_list
        df['ville'] = ville_list
        return df.drop(columns=['localisation'], errors='ignore')
    
    def preprocess(self, df):
        """Prétraitement complet des données"""
        logger.info("Début du prétraitement...")
        
        df_cleaned = df.copy()
        
        # Convertir les colonnes booléennes en int
        bool_cols = df_cleaned.select_dtypes(include='bool').columns
        df_cleaned[bool_cols] = df_cleaned[bool_cols].astype(int)
        
        # Remplacer les chaînes vides par NaN
        df_cleaned.replace(to_replace=["", " ", "  ", "   ", "    "], 
                          value=np.nan, inplace=True)
        
        # Nettoyage prix
        if 'prix' in df_cleaned.columns:
            df_cleaned['prix_dh'] = df_cleaned['prix'].apply(self.clean_price)
        elif 'prix_dh' in df_cleaned.columns:
            df_cleaned['prix_dh'] = df_cleaned['prix_dh'].apply(self.clean_price)
        
        # Nettoyage surface
        if 'surface' in df_cleaned.columns:
            df_cleaned['surface'] = df_cleaned['surface'].apply(self.clean_surface)
        
        # Extraction localisation
        if 'localisation' in df_cleaned.columns:
            df_cleaned = self.extract_location(df_cleaned)
        
        # Remplir zone et ville manquantes
        df_cleaned['zone'] = df_cleaned.get('zone', pd.Series(["Unknown"] * len(df_cleaned))).fillna("Unknown")
        df_cleaned['ville'] = df_cleaned.get('ville', pd.Series(["Unknown"] * len(df_cleaned))).fillna("Unknown")
        
        # Supprimer les colonnes inutiles
        existing_columns_to_drop = [col for col in COLUMNS_TO_DROP if col in df_cleaned.columns]
        df_cleaned = df_cleaned.drop(columns=existing_columns_to_drop, errors="ignore")
        
        # Remplir les colonnes numériques manquantes
        for col in NUMERICAL_COLUMNS:
            if col in df_cleaned.columns:
                df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce').fillna(df_cleaned[col].median())
        
        logger.info("Prétraitement terminé")
        return df_cleaned
    
    def encode_and_scale(self, df, fit=False):
        """One-hot encoding et standardisation"""
        logger.info("Encodage et standardisation...")
        
        df_prepared = df.copy()
        
        # Convertir les booléens
        for col in df_prepared.columns:
            uniques = set(df_prepared[col].dropna().unique())
            if uniques <= {"TRUE", "FALSE", "True", "False", 1, 0, True, False}:
                df_prepared[col] = df_prepared[col].map({
                    "TRUE": 1, "True": 1, True: 1,
                    "FALSE": 0, "False": 0, False: 0,
                    1: 1, 0: 0
                }).astype(float)
        
        # Remplir les colonnes numériques
        for col in NUMERICAL_COLUMNS:
            if col not in df_prepared.columns:
                df_prepared[col] = 0
            else:
                df_prepared[col] = df_prepared[col].fillna(0)
        
        # Sauvegarder prix réel
        prix_reel = None
        if 'prix_dh' in df_prepared.columns:
            prix_reel = df_prepared['prix_dh'].copy()
            df_prepared = df_prepared.drop(columns=['prix_dh'])
        
        # One-hot encoding
        if fit:
            self.encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
            encoded_array = self.encoder.fit_transform(df_prepared[CATEGORICAL_COLUMNS])
        else:
            if self.encoder is None:
                raise ValueError("Encoder not fitted! Use fit=True first")
            encoded_array = self.encoder.transform(df_prepared[CATEGORICAL_COLUMNS])
        
        encoded_df = pd.DataFrame(
            encoded_array,
            columns=self.encoder.get_feature_names_out(CATEGORICAL_COLUMNS)
        )
        encoded_df = encoded_df.astype(int)
        
        df_prepared = pd.concat([df_prepared.reset_index(drop=True), encoded_df], axis=1)
        
        # Standardisation
        if fit:
            self.scaler = StandardScaler()
            df_prepared[NUMERICAL_COLUMNS] = self.scaler.fit_transform(
                df_prepared[NUMERICAL_COLUMNS]
            )
        else:
            if self.scaler is None:
                raise ValueError("Scaler not fitted! Use fit=True first")
            df_prepared[NUMERICAL_COLUMNS] = self.scaler.transform(
                df_prepared[NUMERICAL_COLUMNS]
            )
        
        # Supprimer les colonnes d'origine
        df_prepared = df_prepared.drop(columns=CATEGORICAL_COLUMNS, errors='ignore')
        
        # Sauvegarder les colonnes features
        if fit:
            self.features_columns = df_prepared.columns.tolist()
        else:
            df_prepared = df_prepared.reindex(columns=self.features_columns, fill_value=0)
        
        logger.info("Encodage et standardisation terminés")
        return df_prepared, prix_reel
    
    def save_transformers(self, encoder_path, scaler_path, features_path):
        """Sauvegarde les transformateurs"""
        joblib.dump(self.encoder, encoder_path)
        joblib.dump(self.scaler, scaler_path)
        joblib.dump(self.features_columns, features_path)
        logger.info(f"Transformateurs sauvegardés")
    
    def load_transformers(self, encoder_path, scaler_path, features_path):
        """Charge les transformateurs"""
        self.encoder = joblib.load(encoder_path)
        self.scaler = joblib.load(scaler_path)
        self.features_columns = joblib.load(features_path)
        logger.info(f"Transformateurs chargés")
