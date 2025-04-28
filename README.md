Restaurant Reservation Chatbot
Ce projet est un chatbot Rasa qui permet de gérer les réservations pour un restaurant. Le chatbot est conçu pour interagir en français et offre des fonctionnalités telles que la réservation de tables, l'affichage de réservations existantes et leur gestion.

Fonctionnalités
Réservation de tables avec collecte des informations (date, nombre de personnes, téléphone)
Validation des entrées utilisateur
Confirmation ou annulation des réservations
Consultation des détails d'une réservation existante
Stockage des réservations dans une base de données PostgreSQL
Notifications Discord pour les nouvelles réservations
Prérequis
Python 3.8+
Docker et Docker Compose
PostgreSQL (ou utiliser la version Docker)
Rasa 3.6.2
Structure du projet
endpo
Installation
Clonez le dépôt
Créez et activez un environnement virtuel Python
Installez Rasa et les dépendances
Configuration de la base de données
Assurez-vous que PostgreSQL est installé et en cours d'exécution
Créez une base de données nommée restaurantdb
Vous pouvez modifier les paramètres de connexion dans le fichier actions.py si nécessaire
Démarrage avec Docker
Construisez et lancez les services avec Docker Compose
Cette commande va démarrer :

Le serveur principal Rasa
Le serveur d'actions personnalisées
Le service Duckling pour l'extraction d'entités (dates, nombres, etc.)
Démarrage manuel (sans Docker)
Démarrez le serveur d'actions dans un terminal
Dans un autre terminal, démarrez le serveur Rasa
Pour tester le chatbot dans la console
Interface Web
Une interface web simple est disponible dans le dossier web-ui. Pour l'utiliser :

Assurez-vous que le serveur Rasa est en cours d'exécution
Ouvrez le fichier index.html dans votre navigateur
Alias pratique
Un alias est inclus dans le fichier .rasaalias pour faciliter le lancement du bot :

Notes importantes
Le webhook Discord est inclus dans le code à des fins de démonstration, pensez à le remplacer ou le supprimer en production
La configuration de la base de données est définie pour un environnement local, modifiez-la selon votre configuration
Utilisation du chatbot
Pour interagir avec le chatbot, vous pouvez :

Utiliser la commande rasa shell
Utiliser l'interface web
Se connecter via l'API REST sur le port 5005
Exemples de phrases pour tester le chatbot :

"Je voudrais réserver une table"
"Réserver pour 4 personnes demain soir"
"Je veux voir ma réservation"