#model.py
import os

import mysql.connector

# Paramètres de connexion : modifiables avec des variables d'environnement,
# sinon valeurs par défaut de XAMPP (utilisateur root sans mot de passe)
DB_CONFIG = {
    "host": os.getenv("PARKING_DB_HOST", "localhost"),
    "user": os.getenv("PARKING_DB_USER", "root"),
    "password": os.getenv("PARKING_DB_PASSWORD", ""),
    "database": os.getenv("PARKING_DB_NAME", "gestion_parking"),
}


class ParkingModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print(f"Erreur de connexion à la base de données: {err}")
            raise

    def reserver_place(self, data):
        numero_place, nom_utilisateur, date_reservation, heure_debut, heure_fin, type_vehicule = data

        try:
            # Vérifier si la place existe et correspond au type de véhicule
            query_check = """
            SELECT id, type_vehicule, disponible 
            FROM places_reservations 
            WHERE numero_place = %s
            """
            self.cursor.execute(query_check, (numero_place,))
            result = self.cursor.fetchone()

            if not result:
                return "La place n'existe pas." 

            id_place, type_place, disponible = result

            # Vérifier les conflits de réservation
            query_conflict = """
            SELECT COUNT(*) 
            FROM places_reservations 
            WHERE numero_place = %s 
            AND date_reservation = %s 
            AND disponible = 0
            AND (
                (heure_debut <= %s AND heure_fin > %s)
                OR (heure_debut < %s AND heure_fin >= %s)
                OR (heure_debut >= %s AND heure_fin <= %s)
            )
            """
            self.cursor.execute(query_conflict, (numero_place, date_reservation,
                                               heure_debut, heure_debut,
                                               heure_fin, heure_fin,
                                               heure_debut, heure_fin))
            if self.cursor.fetchone()[0] > 0:
                return "Cette place est déjà réservée pour cette période."

            # Vérifier que le type de véhicule correspond
            if (numero_place.startswith('V') and type_vehicule != 'voiture') or \
               (numero_place.startswith('M') and type_vehicule != 'moto'):
                return f"Cette place est réservée uniquement pour les {type_place}s."

            # Réserver la place
            query_reserve = """
            UPDATE places_reservations 
            SET nom_utilisateur = %s, date_reservation = %s, 
                heure_debut = %s, heure_fin = %s, disponible = 0 
            WHERE id = %s
            """
            self.cursor.execute(query_reserve, (nom_utilisateur, date_reservation, 
                                              heure_debut, heure_fin, id_place))
            self.connection.commit()
            return True

        except mysql.connector.Error as err:
            print(f"Erreur lors de la réservation: {err}")
            return f"Erreur lors de la réservation: {err}"
    
    def verifier_disponibilite(self):
        """
        Retourne toutes les places disponibles.
        """
        try:
            query = """
            SELECT id, numero_place, type_vehicule, disponible
            FROM places_reservations
            WHERE disponible = 1
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erreur lors de la vérification de disponibilité: {err}")
            return []

    def verifier_disponibilite_par_id(self, id_place):
        """
        Vérifie si une place est disponible par son ID.
        Retourne True si la place est disponible, False sinon.
        """
        try:
            query = """
            SELECT disponible FROM places_reservations
            WHERE id = %s
            """
            self.cursor.execute(query, (id_place,))
            result = self.cursor.fetchone()
            return result[0] == 1 if result else False
        except mysql.connector.Error as err:
            print(f"Erreur lors de la vérification de disponibilité par ID: {err}")
            return False

    def enregistrer_entree(self, id_place):
        """
        Enregistre l'entrée d'un véhicule.
        """
        try:
            query = "UPDATE places_reservations SET disponible = 0 WHERE id = %s"
            self.cursor.execute(query, (id_place,))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Erreur lors de l'enregistrement de l'entrée: {err}")

    def enregistrer_sortie(self, id_place):
        """
        Enregistre la sortie d'un véhicule.
        """
        try:
            query = """
            UPDATE places_reservations
            SET disponible = 1, nom_utilisateur = NULL, date_reservation = NULL, heure_debut = NULL, heure_fin = NULL
            WHERE id = %s
            """
            self.cursor.execute(query, (id_place,))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"Erreur lors de l'enregistrement de la sortie: {err}")

    def fermer(self):
        """
        Ferme proprement le curseur et la connexion à la base de données.
        """
        try:
            if getattr(self, 'cursor', None) is not None:
                self.cursor.close()
            if getattr(self, 'connection', None) is not None and self.connection.is_connected():
                self.connection.close()
        except (mysql.connector.Error, ReferenceError):
            pass
        finally:
            self.cursor = None
            self.connection = None

    def __del__(self):
        self.fermer()

    def verifier_disponibilite_par_type(self, type_vehicule):
        """
        Retourne toutes les places disponibles pour un type de véhicule donné.
        """
        try:
            query = """
            SELECT id, numero_place, type_vehicule, disponible
            FROM places_reservations
            WHERE disponible = 1 AND type_vehicule = %s
            """
            self.cursor.execute(query, (type_vehicule,))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erreur lors de la vérification de disponibilité par type: {err}")
            return []

    def verifier_disponibilite_date_heure(self, date_reservation, heure_debut, heure_fin):
        """
        Retourne les places disponibles pour une date et une période donnée.
        """
        try:
            query = """
            SELECT p.id, p.numero_place, p.type_vehicule, p.disponible
            FROM places_reservations p
            WHERE NOT EXISTS (
                SELECT 1
                FROM places_reservations r
                WHERE r.id = p.id
                AND r.date_reservation = %s
                AND r.disponible = 0
                AND (
                    (r.heure_debut <= %s AND r.heure_fin > %s)
                    OR (r.heure_debut < %s AND r.heure_fin >= %s)
                    OR (r.heure_debut >= %s AND r.heure_fin <= %s)
                )
            )
            """
            self.cursor.execute(query, (date_reservation, heure_debut, heure_debut,
                                      heure_fin, heure_fin, heure_debut, heure_fin))
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erreur lors de la vérification de disponibilité: {err}")
            return []