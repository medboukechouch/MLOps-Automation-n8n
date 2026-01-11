"""
Module de prédiction avec les modèles ML
"""

import os
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

from configs.config import MODEL_DIR, MODELS
from src.utils import get_logger

logger = get_logger(__name__)


class PricePredictor:
    """Prédit les prix immobiliers avec plusieurs modèles"""
    
    def __init__(self, model_dir=MODEL_DIR):
        self.model_dir = Path(model_dir)
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Charge tous les modèles"""
        logger.info("Chargement des modèles...")
        
        for model_name, model_file in MODELS.items():
            model_path = self.model_dir / model_file
            try:
                self.models[model_name] = joblib.load(model_path)
                logger.info(f"Modèle {model_name} chargé avec succès")
            except Exception as e:
                logger.error(f"Erreur lors du chargement de {model_name}: {e}")
        
        if not self.models:
            raise ValueError("Aucun modèle n'a pu être chargé!")
    
    def predict(self, X):
        """Prédit les prix avec tous les modèles"""
        logger.info(f"Génération des prédictions pour {len(X)} propriétés...")
        
        predictions = {}
        
        for model_name, model in self.models.items():
            try:
                preds = model.predict(X)
                predictions[f"prix_predit_{model_name}"] = preds.flatten()
                logger.info(f"Prédictions générées avec {model_name}")
            except Exception as e:
                logger.error(f"Erreur avec {model_name}: {e}")
                predictions[f"prix_predit_{model_name}"] = [None] * len(X)
        
        return predictions
    
    def predict_ensemble(self, X, weights=None):
        """Prédit avec une moyenne pondérée des modèles"""
        if weights is None:
            weights = {model: 1/len(self.models) for model in self.models}
        
        ensemble_pred = np.zeros(len(X))
        
        for model_name, model in self.models.items():
            weight = weights.get(model_name, 1/len(self.models))
            preds = model.predict(X)
            ensemble_pred += weight * preds
        
        return ensemble_pred
    
    def predict_with_confidence(self, X):
        """Prédit avec un intervalle de confiance (écart-type)"""
        all_predictions = []
        
        for model_name, model in self.models.items():
            preds = model.predict(X)
            all_predictions.append(preds)
        
        all_predictions = np.array(all_predictions)
        mean_pred = np.mean(all_predictions, axis=0)
        std_pred = np.std(all_predictions, axis=0)
        
        return {
            'predictions': mean_pred,
            'lower_bound': mean_pred - 1.96 * std_pred,
            'upper_bound': mean_pred + 1.96 * std_pred
        }


class ModelEvaluator:
    """Évalue les performances des modèles"""
    
    @staticmethod
    def calculate_metrics(y_true, y_pred):
        """Calcule les métriques de performance"""
        from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
        
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
        
        return {
            'MAE': mae,
            'RMSE': rmse,
            'R2': r2,
            'MAPE': mape
        }
    
    @staticmethod
    def compare_models(y_true, predictions_dict):
        """Compare les performances de plusieurs modèles"""
        results = {}
        
        for model_name, y_pred in predictions_dict.items():
            metrics = ModelEvaluator.calculate_metrics(y_true, y_pred)
            results[model_name] = metrics
        
        # Créer un DataFrame pour l'affichage
        df_results = pd.DataFrame(results).T
        
        logger.info("\n=== Comparaison des modèles ===")
        logger.info(df_results.to_string())
        
        return df_results


if __name__ == "__main__":
    # Exemple d'utilisation
    from src.preprocessor import DataPreprocessor
    
    # Charger les données
    df = pd.read_csv("data/processed/prepared_data.csv")
    X = df.drop(columns=['prix_dh'])
    
    # Prédire
    predictor = PricePredictor()
    predictions = predictor.predict(X)
    predictions_ensemble = predictor.predict_ensemble(X)
    
    print(f"Prédictions générées: {len(predictions)}")
