# Guide d'installation détaillé

## Prérequis système

- Windows, macOS ou Linux
- Python 3.8 ou supérieur
- Pip (gestionnaire de paquets Python)
- Google Chrome/Chromium
- Compte Google Cloud

## Étape 1: Cloner le repository

```bash
git clone https://github.com/medboukechouch/MLOps-Automation-n8n.git
cd property-price-predictor
```

## Étape 2: Créer un environnement virtuel

**Sur Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Sur macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

## Étape 3: Installer les dépendances

```bash
pip install -r requirements.txt
```

## Étape 4: Configurer Google Sheets

### 4.1 Créer un projet Google Cloud

1. Aller sur [Google Cloud Console](https://console.cloud.google.com)
2. Créer un nouveau projet
3. Activer l'API "Google Sheets API"
4. Créer une clé de service (Service Account):
   - Aller à "Service Accounts"
   - Créer un compte de service
   - Créer une clé JSON
5. Télécharger le fichier `service_account.json`

### 4.2 Placer la clé

```bash
# Copier le fichier téléchargé
cp ~/Downloads/service_account.json configs/service_account.json
```

### 4.3 Configurer Google Sheets

1. Créer un Google Sheet nommé "Scraped Properties"
2. Créer des onglets:
   - "Feuille 1" (pour les données scrappées)
   - "Predictions" (sera créé automatiquement)
3. Partager le Sheet avec l'email du service account

## Étape 5: Configurer ChromeDriver

### Option A: Installation automatique (recommandée)

```bash
pip install webdriver-manager
# Le driver sera téléchargé automatiquement
```

### Option B: Installation manuelle

1. Télécharger [ChromeDriver](https://chromedriver.chromium.org/)
2. Placer dans `C:\webdrivers\chromedriver.exe` (Windows)
   ou `/usr/local/bin/chromedriver` (macOS/Linux)
3. Rendre exécutable sur macOS/Linux:
   ```bash
   chmod +x /usr/local/bin/chromedriver
   ```

## Étape 6: Configurer les variables d'environnement

```bash
# Copier le fichier exemple
cp .env.example .env

# Éditer .env avec vos paramètres
# nano .env  ou  code .env
```

Exemple de contenu `.env`:
```env
SHEET_NAME=Scraped Properties
SERVICE_ACCOUNT_PATH=configs/service_account.json
CHROMEDRIVER_PATH=C:/webdrivers/chromedriver.exe
WEBHOOK_URL=http://localhost:5678/webhook/your-id  # optionnel
```

## Étape 7: Vérifier l'installation

```bash
# Tester l'import des modules
python -c "from src.scraper import PropertyScraper; print('✅ Installation OK!')"
```

## Dépannage

### Erreur: "service_account.json not found"
- Vérifier que le fichier est dans `configs/service_account.json`
- Vérifier le chemin dans `.env`

### Erreur: "ChromeDriver not found"
- Vérifier que ChromeDriver est dans le bon répertoire
- Vérifier le chemin dans `config.py`
- Essayer d'installer `webdriver-manager`: `pip install webdriver-manager`

### Erreur: "Google Sheets API not enabled"
- Aller sur Google Cloud Console
- Activer l'API Google Sheets
- Donner les permissions au service account

### Erreur: "Permission denied" sur macOS/Linux
```bash
chmod +x scripts/scrape.py
chmod +x scripts/predict.py
```

## Prochaines étapes

- [Guide d'utilisation](USAGE.md)
- [Configuration n8n](N8N_SETUP.md)
- [Référence API](API.md)
