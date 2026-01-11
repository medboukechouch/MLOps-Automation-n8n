"""
Module d'intégration avec Google Sheets
"""

import gspread
import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe

from configs.config import SERVICE_ACCOUNT_PATH, SHEET_NAME, INPUT_WORKSHEET_NAME, OUTPUT_WORKSHEET_NAME
from src.utils import get_logger

logger = get_logger(__name__)


class SheetsHandler:
    """Gère la lecture/écriture dans Google Sheets"""
    
    def __init__(self, service_account_path=SERVICE_ACCOUNT_PATH, sheet_name=SHEET_NAME):
        self.service_account_path = service_account_path
        self.sheet_name = sheet_name
        self.gc = None
        self.sh = None
        self.connect()
    
    def connect(self):
        """Se connecte à Google Sheets"""
        logger.info("Connexion à Google Sheets...")
        try:
            self.gc = gspread.service_account(filename=self.service_account_path)
            self.sh = self.gc.open(self.sheet_name)
            logger.info("Connexion réussie!")
        except Exception as e:
            logger.error(f"Erreur de connexion: {str(e)}")
            raise
    
    def read_input(self, worksheet_name=INPUT_WORKSHEET_NAME):
        """Lit les données d'entrée"""
        logger.info(f"Lecture depuis l'onglet '{worksheet_name}'...")
        try:
            worksheet = self.sh.worksheet(worksheet_name)
            df = get_as_dataframe(worksheet, evaluate_formulas=True)
            df = df.dropna(how="all")
            logger.info(f"{len(df)} lignes lues!")
            return df
        except Exception as e:
            logger.error(f"Erreur de lecture: {str(e)}")
            raise
    
    def write_output(self, df, worksheet_name=OUTPUT_WORKSHEET_NAME):
        """Écrit les résultats dans Google Sheets"""
        logger.info(f"Écriture dans l'onglet '{worksheet_name}'...")
        try:
            # Supprimer l'onglet s'il existe
            try:
                output_worksheet = self.sh.worksheet(worksheet_name)
                self.sh.del_worksheet(output_worksheet)
                logger.info(f"Onglet '{worksheet_name}' supprimé")
            except gspread.exceptions.WorksheetNotFound:
                pass
            
            # Créer un nouvel onglet
            max_rows = min(len(df) + 10, 50000)
            max_cols = min(len(df.columns) + 5, 18278)
            output_worksheet = self.sh.add_worksheet(
                title=worksheet_name,
                rows=max_rows,
                cols=max_cols
            )
            
            # Écrire les données
            set_with_dataframe(
                output_worksheet,
                df,
                include_index=False,
                include_column_header=True
            )
            
            logger.info(f"Prédictions écrites dans l'onglet '{worksheet_name}'!")
        except Exception as e:
            logger.error(f"Erreur d'écriture: {str(e)}")
            raise
    
    def append_data(self, df, worksheet_name=INPUT_WORKSHEET_NAME):
        """Ajoute des données à une feuille existante"""
        logger.info(f"Ajout de données à l'onglet '{worksheet_name}'...")
        try:
            worksheet = self.sh.worksheet(worksheet_name)
            set_with_dataframe(
                worksheet,
                df,
                include_index=False,
                include_column_header=False,
                row=len(worksheet.get_all_values()) + 1
            )
            logger.info("Données ajoutées avec succès!")
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout: {str(e)}")
            raise


def prepare_output(df_original, predictions, price_real=None):
    """Prépare les données de sortie"""
    out_df = pd.DataFrame()
    
    # Ajouter le prix réel
    if price_real is not None:
        out_df["prix_reel"] = price_real
    else:
        out_df["prix_reel"] = df_original.get("prix_dh", df_original.get("prix", [None]*len(df_original)))
    
    # Ajouter les prédictions
    for pred_col, pred_vals in predictions.items():
        out_df[pred_col] = pred_vals
    
    # Ajouter les infos supplémentaires
    for col in ['ville', 'zone', 'surface', 'pièces', 'chambres']:
        if col in df_original.columns:
            out_df[col] = df_original[col]
    
    return out_df


if __name__ == "__main__":
    # Exemple d'utilisation
    handler = SheetsHandler()
    
    # Lire les données
    df = handler.read_input()
    print(f"Données lues: {df.shape}")
    
    # Écrire des résultats (exemple)
    results = df.head(5).copy()
    results['prediction'] = [1000000, 1200000, 950000, 1150000, 1050000]
    handler.write_output(results)
