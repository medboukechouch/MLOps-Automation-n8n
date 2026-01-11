# Property Price Predictor 🏠

Un système complet de scraping et prédiction des prix immobiliers au Maroc, intégré avec n8n pour l'automatisation.

## 📋 Vue d'ensemble

Ce projet combine:
- **Web Scraping** : Collecte automatisée de données immobilières depuis Mubawab.ma
- **Prétraitement** : Nettoyage et enrichissement des données
- **Machine Learning** : Prédiction des prix avec 4 modèles (Linear Regression, Random Forest, Gradient Boosting, SVR)
- **Automatisation** : Intégration n8n pour le pipeline continu
- **Google Sheets** : Stockage et affichage des résultats en temps réel

## 🚀 Démarrage rapide

### Prérequis

- Python 3.8+
- Chrome/Chromium
- Compte Google Cloud (pour Google Sheets API)
- (Optionnel) n8n pour l'automatisation

### Installation

```bash
# Cloner le projet
git clone https://github.com/medboukechouch/MLOps-Automation-n8n.git
cd MLOps-Automation-n8n

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Configuration

1. **Service Account Google** : Placer `service_account.json` dans le dossier `configs/`
2. **ChromeDriver** : Télécharger et configurer le chemin dans `configs/config.py`
3. **Variables d'environnement** : Créer un fichier `.env` :

```env
# Google Sheets
SHEET_NAME=Scraped Properties
WORKSHEET_NAME=Feuille 1

# n8n (optionnel)
WEBHOOK_URL=http://localhost:5678/webhook/your-webhook-id
MODEL_DIR=./models

# Scraping
CHROMEDRIVER_PATH=C:/webdrivers/chromedriver.exe
BASE_URL=https://www.mubawab.ma/fr/sc/appartements-a-vendre
MAX_ADS=100000

# Service Account
SERVICE_ACCOUNT_PATH=configs/service_account.json
```

## 📁 Structure du projet

```
property-price-predictor/
├── src/                          # Code source principal
│   ├── __init__.py
│   ├── scraper.py               # Web scraping
│   ├── preprocessor.py          # Prétraitement des données
│   ├── models.py                # Chargement et prédictions ML
│   ├── sheets_handler.py        # Intégration Google Sheets
│   └── utils.py                 # Fonctions utilitaires
│
├── models/                       # Modèles ML pré-entraînés
│   ├── modele_Linear_Regression.pkl
│   ├── modele_Random_Forest.pkl
│   ├── modele_Gradient_Boosting.pkl
│   ├── modele_SVR.pkl
│   ├── encoder.pkl              # One-hot encoder
│   ├── scaler.pkl               # StandardScaler
│   └── features_columns.pkl     # Colonnes features
│
├── data/
│   ├── raw/                     # Données brutes
│   └── processed/               # Données nettoyées
│
├── notebooks/                    # Jupyter notebooks
│   ├── 01_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   └── 03_model_training.ipynb
│
├── configs/
│   ├── config.py                # Configuration centralisée
│   ├── service_account.json     # (À ne pas committer)
│   └── n8n_workflow.json        # Configuration n8n
│
├── docs/                        # Documentation
│   ├── INSTALLATION.md
│   ├── USAGE.md
│   └── API.md
│
├── scripts/
│   ├── scrape.py               # Script de scraping standalone
│   ├── predict.py              # Script de prédiction standalone
│   └── train_models.py         # Script d'entraînement
│
├── requirements.txt             # Dépendances Python
├── .gitignore                   # Fichiers à ignorer
├── .env.example                 # Exemple de configuration
└── LICENSE                      # Licence du projet
```

## 🔄 Flux de travail

### 1. Scraping des données
```bash
python scripts/scrape.py
```

Collecte les données immobilières et les envoie à Google Sheets.

### 2. Prédiction des prix
```bash
python scripts/predict.py
```

Charge les données de Google Sheets, applique le prétraitement et génère les prédictions.

### 3. Automatisation avec n8n
Configure un workflow n8n qui:
1. Déclenche le scraping à intervalle régulier
2. Envoie les données à Google Sheets via webhook
3. Lance automatiquement les prédictions

## 📊 Modèles disponibles

Le projet inclut 4 modèles de prédiction:

| Modèle | MAE | RMSE | R² |
|--------|-----|------|-----|
| Linear Regression | 0.31 | 0.45 | 0.80 |
| Random Forest | 0.31 | 0.47 | 0.78 |
| Gradient Boosting | 0.31 | 0.51 | 0.74 |
| XGBoost | 0.31 | 0.44 | 0.81 |

## 🔑 Fonctionnalités principales

### Scraping
- ✅ Extraction complète des annonces (prix, surface, pièces, etc.)
- ✅ Détection des extras (ascenseur, climatisation, etc.)
- ✅ Gestion des utilisateurs-agents
- ✅ Envoi via webhook n8n
- ✅ Stockage dans Google Sheets

### Prétraitement
- ✅ Nettoyage des valeurs manquantes
- ✅ Conversion des unités (EUR → DH)
- ✅ Extraction des zones et villes
- ✅ Encodage one-hot des variables catégorielles
- ✅ Standardisation des variables numériques

### Prédiction
- ✅ Prédictions avec 4 modèles
- ✅ Comparaison automatique
- ✅ Export des résultats dans Google Sheets
- ✅ Support des variables manquantes

## 🛠️ Technologies utilisées

- **Scraping** : Selenium, BeautifulSoup
- **Données** : Pandas, NumPy
- **ML** : Scikit-learn, Joblib
- **Google** : gspread, google-auth
- **Automatisation** : n8n
- **Dev** : Python 3.8+, Git

## 📝 Exemples d'utilisation

### Utilisation basique
```python
from src.scraper import PropertyScraper
from src.preprocessor import DataPreprocessor
from src.models import PricePredictor

# Scraper
scraper = PropertyScraper()
data = scraper.scrape_properties()

# Prétraiter
preprocessor = DataPreprocessor()
clean_data = preprocessor.preprocess(data)

# Prédire
predictor = PricePredictor()
predictions = predictor.predict(clean_data)
```

### Avec Google Sheets
```python
from src.sheets_handler import SheetsHandler

sheets = SheetsHandler()
raw_data = sheets.read_input()
predictions = predict(raw_data)
sheets.write_output(predictions)
```

## 🔐 Sécurité

⚠️ **Important** : 
- Ne jamais committer `service_account.json`
- Ne pas exposer les webhooks n8n
- Utiliser des variables d'environnement pour les clés sensibles
- Voir `.gitignore` pour les fichiers ignorés

## 📚 Documentation complète

- [Installation détaillée](docs/INSTALLATION.md)
- [Guide d'utilisation](docs/USAGE.md)
- [Référence API](docs/API.md)
- [Configuration n8n](docs/N8N_SETUP.md)

## 🤝 Contribution

Les contributions sont bienvenues! Veuillez:
1. Fork le projet
2. Créer une branche (`git checkout -b feature/amazing-feature`)
3. Committer vos changements (`git commit -m 'Add amazing feature'`)
4. Pusher vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir [LICENSE](LICENSE) pour plus de détails.

## 👨‍💼 Auteur

Développé par **Mohamed BOUKECHOUCH** et **Mohammed KARRAJI** comme projet fin d'études (PFE)

## 💬 Support

Pour toute question ou problème:
- Ouvrir une [issue](https://github.com/medboukechouch/MLOps-Automation-n8n/issues)
- Contacter directement

## 🎯 Roadmap

- [ ] API REST avec FastAPI
- [ ] Interface web (Streamlit/Django)
- [ ] Support de plusieurs sites immobiliers
- [ ] Modèles d'apprentissage profond (Deep Learning)
- [ ] Dashboard en temps réel
- [ ] Tests unitaires complets

---

**Dernière mise à jour** : Janvier 2026
