# 🍽️ Restaurant Reservation Chatbot

Un chatbot Rasa qui permet de gérer les réservations pour un restaurant. Le chatbot est conçu pour interagir en français et facilite la réservation de tables, l'affichage et la gestion des réservations existantes.

## ✨ Fonctionnalités

- 📅 Réservation de tables avec collecte des informations (date, nombre de personnes, téléphone)
- ✅ Validation des entrées utilisateur (format du téléphone, dates valides, etc.)
- 🔄 Confirmation ou annulation des réservations
- 🔍 Consultation des détails d'une réservation existante
- 💾 Stockage des réservations dans une base de données PostgreSQL
- 📣 Notifications Discord pour les nouvelles réservations

## 🛠️ Prérequis

- Python 3.8+
- Docker et Docker Compose (pour le déploiement conteneurisé)
- PostgreSQL (ou utiliser la version Docker)
- Rasa 3.6.2

## 📂 Structure du projet

```
ChatbotRasa/
├── actions/              # Actions personnalisées et logique métier
│   ├── actions.py        # Implémentation des actions
│   ├── Dockerfile        # Dockerfile pour le serveur d'actions
│   └── requirements.txt  # Dépendances pour les actions
├── data/                 # Données d'entraînement
│   ├── nlu.yml           # Exemples d'intentions utilisateur
│   ├── rules.yml         # Règles de conversation
│   ├── stories.yml       # Flux de conversation
│   └── regex_features.yml # Expressions régulières
├── database/             # Scripts de base de données
│   └── init.sql          # Initialisation des tables
├── web-ui/               # Interface web simple
│   └── index.html        # Page de chat
├── config.yml            # Configuration du pipeline NLP
├── credentials.yml       # Identifiants pour les canaux
├── domain.yml            # Définition du domaine (intentions, actions, etc.)
└── endpoints.yml         # Configuration des endpoints
```

## 🚀 Installation

### Clonage du dépôt

```bash
git clone https://github.com/votre-utilisateur/ChatbotRasa.git
cd ChatbotRasa
```

### Option 1: Installation avec Docker (recommandée)

1. **Démarrage des services**:
   ```bash
   docker-compose up -d
   ```
   
   Cette commande démarre:
   - 🤖 Le serveur principal Rasa (port 5005)
   - ⚙️ Le serveur d'actions personnalisées (port 5055)
   - 🦆 Le service Duckling pour l'extraction d'entités (port 8000)

2. **Pour arrêter les services**:
   ```bash
   docker-compose down
   ```

### Option 2: Installation manuelle

1. **Créez et activez un environnement virtuel**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

2. **Installez Rasa et les dépendances**:
   ```bash
   pip install rasa==3.6.2
   pip install -r actions/requirements.txt
   ```

3. **Configuration de la base de données**:
   - Assurez-vous que PostgreSQL est installé et en cours d'exécution
   - Créez une base de données nommée `restaurantdb`
   - Vous pouvez modifier les paramètres de connexion dans le fichier `actions/actions.py` si nécessaire

4. **Démarrage des serveurs**:
   ```bash
   # Terminal 1: Démarrer le serveur d'actions
   rasa run actions

   # Terminal 2: Démarrer le serveur Rasa
   rasa run --enable-api --cors "*"
   ```

## 💬 Utilisation du chatbot

Pour interagir avec le chatbot, vous pouvez:

1. **Utiliser la console**:
   ```bash
   rasa shell
   ```

2. **Utiliser l'interface web**:
   - Assurez-vous que le serveur Rasa est en cours d'exécution
   - Ouvrez le fichier `web-ui/index.html` dans votre navigateur

3. **Se connecter via l'API REST** sur le port 5005

### Exemples de phrases pour tester le chatbot

- "Je voudrais réserver une table"
- "Réserver pour 4 personnes demain soir"
- "Je veux voir ma réservation"
- "Mon numéro de réservation est RES-12345678"

## ⚙️ Configuration

### Alias pratique

Un alias est inclus dans le fichier `.rasaalias` pour faciliter le lancement du bot:

```bash
source .rasaalias  # Active l'alias 'rasabot'
rasabot            # Lance le chatbot
```

## ⚠️ Notes importantes

- Le webhook Discord est inclus dans le code à des fins de démonstration, pensez à le remplacer ou le supprimer en production
- La configuration de la base de données est définie pour un environnement local, modifiez-la selon votre configuration