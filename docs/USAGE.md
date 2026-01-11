# Guide d'utilisation

## 🚀 Utilisation rapide

### 1. Scraper les propriétés

```bash
python scripts/scrape.py
```

Cela va:
1. Visiter le site Mubawab.ma
2. Extraire les données des propriétés
3. Envoyer les données à Google Sheets

### 2. Générer les prédictions

```bash
python scripts/predict.py
```

Cela va:
1. Lire les données de Google Sheets
2. Prétraiter les données
3. Générer les prédictions avec 4 modèles
4. Écrire les résultats dans un nouvel onglet "Predictions"

## 📊 Utilisation en Python

### Import basique

```python
from src.scraper import PropertyScraper
from src.preprocessor import DataPreprocessor
from src.models import PricePredictor

# Scraper
scraper = PropertyScraper()
df = scraper.scrape()

# Prétraiter
preprocessor = DataPreprocessor()
df_clean = preprocessor.preprocess(df)

# Prédire
predictor = PricePredictor()
predictions = predictor.predict(df_clean)
```

### Avec Google Sheets

```python
from src.sheets_handler import SheetsHandler

# Lire
handler = SheetsHandler()
df = handler.read_input("Feuille 1")

# Écrire
handler.write_output(df, worksheet_name="Resultats")
```

## 🔧 Configuration avancée

### Modifier les paramètres de scraping

Éditer `configs/config.py`:

```python
BASE_URL = "https://www.mubawab.ma/fr/sc/villas-a-vendre"  # Changer le type de bien
MAX_ADS = 5000  # Limiter le nombre d'annonces
```

### Utiliser des modèles personnalisés

```python
from src.models import PricePredictor

predictor = PricePredictor()

# Prédictions individuelles
predictions = predictor.predict(X_new)

# Moyenne pondérée
weights = {
    "Linear_Regression": 0.1,
    "Random_Forest": 0.4,
    "Gradient_Boosting": 0.4,
    "SVR": 0.1
}
ensemble_pred = predictor.predict_ensemble(X_new, weights=weights)

# Avec intervalle de confiance
result = predictor.predict_with_confidence(X_new)
print(f"Prédiction: {result['predictions'][0]}")
print(f"Intervalle: [{result['lower_bound'][0]}, {result['upper_bound'][0]}]")
```

## 🔄 Automatisation avec n8n

### Configuration simple

1. Installer n8n (ou utiliser cloud.n8n.io)
2. Créer un nouveau workflow
3. Ajouter un trigger "Cron" (pour l'horaire)
4. Ajouter une action "Execute Command"
5. Configurer le script:
   ```bash
   python C:\path\to\scripts\scrape.py
   ```

### Configuration complète (Scraping + Prédictions)

```
┌─────────────────┐
│  Cron Trigger   │ (Chaque jour à 18h)
└────────┬────────┘
         │
┌────────▼────────────┐
│ Execute: scrape.py  │
└────────┬────────────┘
         │
┌────────▼────────────────┐
│ Google Sheets Webhook   │ (Optionnel)
└────────┬────────────────┘
         │
┌────────▼────────────┐
│ Execute: predict.py │
└─────────────────────┘
```

## 📈 Suivi des performances

### Évaluer les modèles

```python
from src.models import ModelEvaluator
import pandas as pd

# Charger les données de test
y_true = pd.read_csv("data/test_prices.csv")['prix']
predictions = {
    'Linear_Regression': [...],
    'Random_Forest': [...],
    'Gradient_Boosting': [...],
    'SVR': [...]
}

# Comparer
results = ModelEvaluator.compare_models(y_true, predictions)
print(results)
```

## 🐛 Dépannage

### Les données ne s'envoient pas à Google Sheets

```bash
# Vérifier la connexion
python -c "from src.sheets_handler import SheetsHandler; SheetsHandler()"
```

### Le scraping est trop lent

```python
# Réduire le nombre d'annonces
from src.scraper import PropertyScraper
scraper = PropertyScraper(max_ads=100)  # Au lieu de 100000
```

### Les prédictions sont nulles

```python
# Vérifier les données préparées
print(X_prepared.head())
print(X_prepared.dtypes)
print(X_prepared.isnull().sum())
```

## 📚 Exemples complets

### Exemple 1: Pipeline complet

```python
import pandas as pd
from src.scraper import PropertyScraper
from src.preprocessor import DataPreprocessor
from src.models import PricePredictor
from src.sheets_handler import SheetsHandler, prepare_output

# 1. Scraper
scraper = PropertyScraper(max_ads=1000)
df = scraper.scrape()

# 2. Prétraiter
preprocessor = DataPreprocessor()
df_clean = preprocessor.preprocess(df)
df_prepared, prix_reel = preprocessor.encode_and_scale(df_clean, fit=False)

# 3. Prédire
predictor = PricePredictor()
predictions = predictor.predict(df_prepared)

# 4. Sauvegarder
output_df = prepare_output(df_clean, predictions, prix_reel)
handler = SheetsHandler()
handler.write_output(output_df)
```

### Exemple 2: Analyse statistique

```python
from src.models import ModelEvaluator
import matplotlib.pyplot as plt

# Comparer les modèles
results = ModelEvaluator.compare_models(y_true, predictions)

# Visualiser
results.plot(kind='bar')
plt.ylabel('Score')
plt.title('Comparaison des modèles')
plt.show()
```

## 🆘 Support

Pour toute question:
- Vérifier les logs dans le terminal
- Ouvrir une issue sur GitHub
- Consulter la [FAQ](FAQ.md)
