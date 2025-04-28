import uuid
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, EventType, UserUtteranceReverted
from datetime import datetime
import psycopg2

# Configuration de ta BDD PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "dbname": "restaurantdb",
    "user": "postgres",
    "password": "postgres"
}

#YES I KNOW NOT SMART TO PUT THE HOOK IN CLEAR TEXT HERE BUT im gonna delete soon the discord 

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1366479496806400000/FzJ09kvA4pAMGtL4g3ZejEbOt2TxYPqPQyIsqVvRFIhZh3rVnyrHmZVgfn42f87r3pDl"

def envoyer_webhook_discord(message: str):
    payload = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=payload)

# Connexion à la BDD PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        # Create tables if they don't exist
        ensure_tables_exist(conn)
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la BDD : {e}")
        return None

# Ensure database tables exist
def ensure_tables_exist(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id VARCHAR(50) PRIMARY KEY,
                nom VARCHAR(100),
                date DATE NOT NULL,
                personnes INT NOT NULL,
                telephone VARCHAR(20) NOT NULL,
                commentaire TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Erreur lors de la création des tables : {e}")
        conn.rollback()

# Save reservation to database
def save_reservation_to_db(reservation_id, data):
    try:
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            # Extract data from reservation
            date_str = data['date'].split('T')[0] if 'T' in data['date'] else data['date']
            
            # Insert into reservations table
            cursor.execute("""
                INSERT INTO reservations (id, date, personnes, telephone, commentaire)
                VALUES (%s, %s, %s, %s, %s)
            """, (reservation_id, date_str, data['personnes'], data['telephone'], data.get('commentaire', '')))
            
            conn.commit()
            cursor.close()
            conn.close()
            envoyer_webhook_discord(f"✅ Nouvelle réservation : {data['personnes']} personnes le {date_str}. Téléphone : {data['telephone']}. ID : {reservation_id}")
            return True
        return False
    except Exception as e:
        print(f"Erreur lors de l'enregistrement de la réservation: {e}")
        if conn:
            conn.close()
        return False

# In-memory reservation store (you can replace with DB later)
reservations = {}

class ValidateReservationForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_reservation_form"

    def validate_telephone(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict:
        if value.isdigit() and len(value) == 10:
            return {"telephone": value}
        dispatcher.utter_message(text="📵 Merci de fournir un numéro de téléphone valide à 10 chiffres.")
        return {"telephone": None}

    def validate_personnes(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict:
        try:
            nb = int(value)
            if 1 <= nb <= 20:
                return {"personnes": value}
        except:
            pass
        dispatcher.utter_message(text="👥 Merci d'indiquer un nombre de personnes valide (1 à 20).")
        return {"personnes": None}

    def validate_date(self, value: Text, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> Dict:
        try:
            if "T" in value:
                date_str = value.split("T")[0]
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                if date_obj >= datetime.today():
                    return {"date": value}
        except:
            pass
        dispatcher.utter_message(text="📅 Merci d'indiquer une date valide dans le futur.")
        return {"date": None}

class ActionReserverTable(Action):
    def name(self) -> Text:
        return "action_reserver_table"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        date = tracker.get_slot("date")
        personnes = tracker.get_slot("personnes")
        telephone = tracker.get_slot("telephone")

        reservation_id = "RES-" + str(uuid.uuid4())[:8]

        # Store reservation (in memory for now)
        reservations[reservation_id] = {
            "date": date,
            "personnes": personnes,
            "telephone": telephone
        }

        message = (
            f"📋 Voici le récapitulatif de votre réservation :\n"
            f"👥 Nombre de personnes : {personnes}\n"
            f"📅 Date : {date}\n"
            f"📞 Téléphone : {telephone}\n"
            f"🔢 Numéro de réservation : {reservation_id}\n"
            f"Souhaitez-vous confirmer cette réservation ? (oui / non)")

        dispatcher.utter_message(text=message)
        return [
            SlotSet("reservation_id", reservation_id),
            SlotSet("confirmation_pending", True),
            SlotSet("recap_message", message)
        ]

class ActionAfficherReservation(Action):
    def name(self) -> Text:
        return "action_afficher_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        reservation_id = tracker.get_slot("reservation_id")
        telephone = tracker.get_slot("telephone")
        date = tracker.get_slot("date")

        conn = connect_db()
        cursor = conn.cursor()

        if reservation_id:
            # 🔍 Requête avec ID unique
            cursor.execute("""
                SELECT id, nom, date, personnes, telephone, commentaire
                FROM reservations
                WHERE id = %s
            """, (reservation_id,))
        elif telephone and date:
            # 🔍 Recherche alternative par téléphone + date
            cursor.execute("""
                SELECT id, nom, date, personnes, telephone, commentaire
                FROM reservations
                WHERE telephone = %s AND date::date = %s::date
                ORDER BY date DESC LIMIT 1
            """, (telephone, date))
        else:
            dispatcher.utter_message(text="❌ Merci de fournir un numéro de réservation ou vos infos (téléphone et date).")
            return []

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            res_id, nom, res_date, personnes, tel, commentaire = row
            dispatcher.utter_message(text=(
                f"📄 Détails de la réservation {res_id} :\n"
                f"👤 Nom : {nom or 'non fourni'}\n"
                f"👥 {personnes} personnes\n"
                f"📅 {res_date}\n"
                f"📞 {tel}\n"
                f"💬 Commentaire : {commentaire or 'aucun'}"
            ))
        else:
            dispatcher.utter_message(text="❌ Aucune réservation trouvée avec ces informations.")
        
        return []


class ActionConfirmerReservation(Action):
    def name(self) -> Text:
        return "action_confirmer_reservation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        reservation_id = tracker.get_slot("reservation_id")
        if reservation_id in reservations:
            # Get reservation data from in-memory store
            reservation_data = reservations[reservation_id]
            
            # Save to database
            if save_reservation_to_db(reservation_id, reservation_data):
                dispatcher.utter_message(text=f"✅ Réservation confirmée avec succès ! Numéro : {reservation_id}")
            else:
                dispatcher.utter_message(text=f"⚠️ Réservation enregistrée mais problème de sauvegarde en base de données. Numéro : {reservation_id}")
                
            # Remove from in-memory store after saving to DB
            del reservations[reservation_id]
        else:
            dispatcher.utter_message(text="Aucune réservation à confirmer.")
        
        return [
            SlotSet("reservation_id", None),
            SlotSet("confirmation_pending", None),
            SlotSet("recap_message", None),
            SlotSet("date", None),
            SlotSet("personnes", None),
            SlotSet("telephone", None)
        ]

class ActionAnnulerReservation(Action):
    def name(self) -> Text:
        return "action_annuler_reservation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        reservation_id = tracker.get_slot("reservation_id")
        if reservation_id in reservations:
            del reservations[reservation_id]
            dispatcher.utter_message(text="❌ Votre réservation a été annulée.")
        else:
            dispatcher.utter_message(text="Aucune réservation trouvée à annuler.")
        return [
            SlotSet("reservation_id", None),
            SlotSet("confirmation_pending", None),
            SlotSet("recap_message", None),
            SlotSet("date", None),
            SlotSet("personnes", None),
            SlotSet("telephone", None)
        ]


class ActionAfficherReservation(Action):
    def name(self) -> Text:
        return "action_afficher_reservation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        reservation_id = tracker.get_slot("reservation_id")
        telephone = tracker.get_slot("telephone")
        date = tracker.get_slot("date")

        conn = connect_db()
        cursor = conn.cursor()

        if reservation_id:
            cursor.execute("""
                SELECT id, nom, date, personnes, telephone, commentaire
                FROM reservations
                WHERE id = %s
            """, (reservation_id,))
        else :
            dispatcher.utter_message(text="Quel est votre numéro de réservation ?")
            return []

        row = cursor.fetchone()
        cursor.close()
        conn.close()

        if row:
            res_id, nom, res_date, personnes, tel, commentaire = row
            dispatcher.utter_message(text=(
                f"📄 Réservation {res_id} :\n"
                f"👥 {personnes} personnes\n"
                f"📅 {res_date}\n"
                f"📞 {tel}\n"
                f"💬 Commentaire : {commentaire or 'aucun'}"
            ))
        else:
            dispatcher.utter_message(text="❌ Aucune réservation trouvée avec ces informations.")
        
        return []

