#controller.py
from tkinter import messagebox
from model import ParkingModel
from datetime import datetime

class ParkingController:
    def __init__(self, view):
        self.view = view
        self.model = ParkingModel()

    def valider_date_heure(self, date_str, heure_debut, heure_fin):
        """
        Valide le format de la date et des heures.
        """
        try:
            # Validation de la date
            datetime.strptime(date_str, '%Y-%m-%d')
            
            # Validation des heures
            datetime.strptime(heure_debut, '%H:%M')
            datetime.strptime(heure_fin, '%H:%M')
            
            # Vérifier que l'heure de fin est après l'heure de début
            if heure_fin <= heure_debut:
                return False, "L'heure de fin doit être après l'heure de début"
                
            return True, None
        except ValueError:
            return False, "Format de date ou d'heure invalide"

    def reserver_place(self):
        """
        Gère la réservation d'une place avec vérification de disponibilité temporelle.
        """
        try:
            # Récupérer les données du formulaire
            numero_place = self.view.numero_place_entry.get()
            nom_utilisateur = self.view.nom_utilisateur_entry.get()
            type_vehicule = self.view.type_vehicule_var.get()

            # Construire la date
            jour = self.view.jour_entry.get()
            mois = self.view.mois_entry.get()
            annee = self.view.annee_entry.get()
            date_reservation = f"{annee}-{mois}-{jour}"

            # Construire les heures
            heure_debut = f"{self.view.heure_debut_h.get()}:{self.view.heure_debut_m.get()}"
            heure_fin = f"{self.view.heure_fin_h.get()}:{self.view.heure_fin_m.get()}"

            # Vérifier que tous les champs sont remplis
            if not all([numero_place, nom_utilisateur, date_reservation, heure_debut, heure_fin, type_vehicule]):
                messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
                return

            # Valider le format de la date et des heures
            valid, error_message = self.valider_date_heure(date_reservation, heure_debut, heure_fin)
            if not valid:
                messagebox.showerror("Erreur", error_message)
                return

            # Vérifier si la date n'est pas dans le passé
            date_actuelle = datetime.now().date()
            date_reservation_obj = datetime.strptime(date_reservation, '%Y-%m-%d').date()
            if date_reservation_obj < date_actuelle:
                messagebox.showerror("Erreur", "La date de réservation ne peut pas être dans le passé.")
                return

            # Préparer les données pour la réservation
            data = (numero_place, nom_utilisateur, date_reservation, heure_debut, heure_fin, type_vehicule)

            # Tenter la réservation
            result = self.model.reserver_place(data)
            if result is True:
                messagebox.showinfo("Succès", "Place réservée avec succès !")
                self.actualiser_disponibilite()
                self.view.vider_champs_reservation()
            else:
                messagebox.showerror("Erreur", result)

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    def actualiser_disponibilite(self):
        """
        Actualise l'affichage des places disponibles.
        """
        try:
            # Vider le tableau actuel
            for item in self.view.disponibilite_tree.get_children():
                self.view.disponibilite_tree.delete(item)

            # Récupérer les filtres actuels
            type_vehicule = self.view.filter_type_var.get()
            
            # Si des dates et heures sont sélectionnées dans les filtres
            if hasattr(self.view, 'filtre_date_active') and self.view.filtre_date_active.get():
                # Construire la date et les heures du filtre
                jour = self.view.filtre_jour_entry.get()
                mois = self.view.filtre_mois_entry.get()
                annee = self.view.filtre_annee_entry.get()
                date_filtre = f"{annee}-{mois}-{jour}"
                heure_debut = f"{self.view.filtre_heure_debut_h.get()}:{self.view.filtre_heure_debut_m.get()}"
                heure_fin = f"{self.view.filtre_heure_fin_h.get()}:{self.view.filtre_heure_fin_m.get()}"
                
                # Récupérer les places disponibles selon les filtres temporels
                places = self.model.verifier_disponibilite_date_heure(date_filtre, heure_debut, heure_fin)
            else:
                # Sinon, récupérer toutes les places disponibles
                if type_vehicule == "Tous":
                    places = self.model.verifier_disponibilite()
                else:
                    places = self.model.verifier_disponibilite_par_type(type_vehicule)

            # Ajouter les places dans le tableau
            for place in places:
                self.view.disponibilite_tree.insert("", "end", values=place)

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    def enregistrer_entree(self):
        """
        Enregistre l'entrée d'un véhicule.
        """
        try:
            id_place = self.view.id_place_entry.get()

            # Vérifier que l'ID est un entier
            try:
                id_place = int(id_place)
            except ValueError:
                messagebox.showerror("Erreur", "L'ID de la place doit être un nombre entier.")
                return

            # Vérifier la disponibilité
            if not self.model.verifier_disponibilite_par_id(id_place):
                messagebox.showerror("Erreur", "Cette place est déjà occupée.")
                return

            self.model.enregistrer_entree(id_place)
            messagebox.showinfo("Succès", "Entrée enregistrée avec succès !")
            self.actualiser_disponibilite()
            self.view.id_place_entry.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    def enregistrer_sortie(self):
        """
        Enregistre la sortie d'un véhicule.
        """
        try:
            id_place = self.view.id_place_entry.get()

            # Vérifier que l'ID est un entier
            try:
                id_place = int(id_place)
            except ValueError:
                messagebox.showerror("Erreur", "L'ID de la place doit être un nombre entier.")
                return

            # Vérifier si la place est déjà libre
            if self.model.verifier_disponibilite_par_id(id_place):
                messagebox.showerror("Erreur", "Cette place est déjà libre.")
                return

            self.model.enregistrer_sortie(id_place)
            messagebox.showinfo("Succès", "Sortie enregistrée avec succès !")
            self.actualiser_disponibilite()
            self.view.id_place_entry.delete(0, 'end')

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {str(e)}")

    def appliquer_filtre(self):
        """
        Applique les filtres de recherche de places disponibles.
        """
        try:
            self.actualiser_disponibilite()
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de l'application du filtre : {str(e)}")