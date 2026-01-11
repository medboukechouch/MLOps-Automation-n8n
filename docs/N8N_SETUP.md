# Configuration n8n

## 📋 Qu'est-ce que n8n?

n8n est une plateforme d'automatisation open-source qui permet de créer des workflows sans coder (ou avec du code).

## Installation

### Option 1: Cloud (Recommandé pour démarrer)

1. Aller sur [cloud.n8n.io](https://cloud.n8n.io)
2. S'enregistrer avec un compte Google
3. Créer un nouveau workflow

### Option 2: Installation locale

```bash
# Avec Node.js et npm
npm install -g n8n

# Lancer n8n
n8n

# Accéder sur http://localhost:5678
```

### Option 3: Docker

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

## 🔄 Workflow: Scraping automatique

### 1. Configuration de base

**Nœud 1: Cron (Trigger temporel)**
- Type: "Cron"
- Planification: `0 18 * * *` (18h00 tous les jours)
- Description: "Démarrer le scraping"

**Nœud 2: Execute Command**
- Commande: 
  ```bash
  python "C:\path\to\scripts\scrape.py"
  ```
- Ou sur Linux/macOS:
  ```bash
  /path/to/venv/bin/python scripts/scrape.py
  ```

**Nœud 3: Notification (optionnel)**
- Type: "Email" ou "Slack"
- Message: "Scraping terminé: {{ $node[\"Execute\"].json.stdout }}"

### 2. Workflow complet (Scraping + Prédictions)

```
Cron (18h)
    ↓
Execute: scrape.py
    ↓
Wait 2 minutes  [optionnel: attendre que Google Sheets se mette à jour]
    ↓
Execute: predict.py
    ↓
Slack Notification
    ↓
Email Notification
```

### 3. Détails du workflow

**Nœud 1: Cron**
```
Mode: Every day
Time: 18:00
Timezone: (selon votre fuseau horaire)
```

**Nœud 2: Execute Scraping**
```
Command: python C:\path\to\scripts\scrape.py
Working Directory: C:\path\to\project
Continue on fail: false
```

**Nœud 3: Attendre (optionnel)**
```
Type: "Wait"
Duration: 2 minutes
```

**Nœud 4: Execute Predictions**
```
Command: python C:\path\to\scripts\predict.py
Working Directory: C:\path\to\project
Continue on fail: false
```

**Nœud 5: Notification Slack (optionnel)**
```
Webhook URL: [votre webhook Slack]
Text: "Prédictions mises à jour ✅"
```

## 🌐 Intégration Webhook

### Recevoir les données scrapy via n8n

**Dans le projet Python:**

```python
# config.py
WEBHOOK_URL = "http://localhost:5678/webhook/yourwebhookid"
SEND_TO_WEBHOOK = True

# scraper.py
if SEND_TO_WEBHOOK:
    scraper.send_to_webhook(property_data)
```

**Workflow n8n:**

```
Webhook (POST)
    ↓
Process Data
    ↓
Google Sheets
```

### Configuration du Webhook n8n

1. Créer un nouveau nœud "Webhook"
2. Configuration:
   - HTTP Method: POST
   - Accept Binary File: No
3. Copier l'URL (elle contient votre webhook ID)
4. Coller dans `.env`:
   ```env
   WEBHOOK_URL=http://localhost:5678/webhook/yourwebhookid
   ```

## 📊 Variables d'environnement dans n8n

Pour passer des variables au script:

```bash
python scripts/scrape.py \
  SHEET_NAME="Mon Sheet" \
  MAX_ADS=5000 \
  WEBHOOK_URL="http://..."
```

Ou créer un fichier `.env` que n8n charge avant d'exécuter.

## 🔐 Sécurité

### Bonnes pratiques

1. **Utiliser des secrets dans n8n:**
   - N8n supporte les variables secrètes
   - Ne pas mettre les clés en dur dans les workflows

2. **Limiter les permissions:**
   - Service account: permissions minimales
   - Google Sheets: partage seulement nécessaire

3. **HTTPS obligatoire** pour les webhooks en production

### Exemple avec secrets n8n

```
Set Variables:
- SHEET_NAME: {{ $secrets.SHEET_NAME }}
- SERVICE_ACCOUNT: {{ $secrets.SERVICE_ACCOUNT }}
```

## 📈 Logs et monitoring

### Vérifier les exécutions

1. Dans l'interface n8n:
   - Cliquer sur "Executions"
   - Voir les logs de chaque run
   - Filtrer par date/statut

### Intégration des logs

```bash
# Envoyer les logs à n8n
python scripts/scrape.py 2>&1 | tee /tmp/n8n.log
```

## 🧪 Test du workflow

1. **Test local d'abord:**
   ```bash
   python scripts/scrape.py
   python scripts/predict.py
   ```

2. **Test dans n8n:**
   - Activer le mode test (commutateur en haut à gauche)
   - Cliquer sur "Execute Workflow"
   - Vérifier les résultats

3. **Vérifier Google Sheets:**
   - Aller sur votre Google Sheet
   - Vérifier que les données arrivent

## ⚠️ Troubleshooting

### Le workflow ne s'exécute pas à l'heure

- Vérifier le fuseau horaire de n8n
- Vérifier que n8n est allumé
- Consulter les logs d'exécution

### Erreur: "Python not found"

- Utiliser le chemin absolu: `C:\python.exe`
- Ou: `/usr/bin/python3`
- Tester: `which python` (Linux/macOS)

### Erreur: "Permission denied"

- Rendre le script exécutable:
  ```bash
  chmod +x scripts/scrape.py
  ```
- Ou exécuter: `python scripts/scrape.py` au lieu de `./scripts/scrape.py`

### Google Sheets n'est pas à jour

- Vérifier que le service account a les permissions
- Vérifier l'URL du Google Sheet
- Vérifier `SHEET_NAME` dans la configuration

## 📚 Ressources

- [Documentation n8n](https://docs.n8n.io)
- [Webhooks n8n](https://docs.n8n.io/nodes/n8n-nodes-base.webhook/)
- [Community Forum](https://community.n8n.io)

## 💡 Prochaines étapes

- [Créer un Dashboard Metabase](METABASE.md) pour visualiser les données
- [API REST](API.md) pour intégrations avancées
- [Alertes intelligentes](ALERTS.md) basées sur les prédictions
