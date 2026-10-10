#view.py
import tkinter as tk
from datetime import date
from tkinter import ttk

class ParkingView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.title("Système de Gestion de Parking")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2E3440")  # Fond sombre

        # Style des widgets
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Thème sombre
        self.style.configure("TNotebook", background="#3B4252", foreground="#ECEFF4")
        self.style.configure("TNotebook.Tab", background="#4C566A", foreground="#ECEFF4", padding=[10, 5], font=("Helvetica", 12))
        self.style.configure("TFrame", background="#3B4252")
        self.style.configure("TLabel", background="#3B4252", foreground="#ECEFF4", font=("Helvetica", 14))
        self.style.configure("TButton", background="#5E81AC", foreground="#ECEFF4", font=("Helvetica", 12), padding=10, borderwidth=0, focusthickness=3, focuscolor="#5E81AC")
        self.style.map("TButton", background=[("active", "#FF007F")])  # Changement de couleur au survol
        self.style.configure("TEntry", font=("Helvetica", 12), fieldbackground="#4C566A", foreground="#ECEFF4")
        self.style.configure("Treeview", background="#4C566A", foreground="#ECEFF4", fieldbackground="#4C566A", font=("Helvetica", 12))
        self.style.configure("Treeview.Heading", background="#5E81AC", foreground="#ECEFF4", font=("Helvetica", 14, "bold"))

        # Création des onglets
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)

        # Onglet de réservation
        self.reservation_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.reservation_tab, text="Réserver une place")
        self.create_reservation_tab()

        # Onglet de disponibilité
        self.disponibilite_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.disponibilite_tab, text="Consulter la disponibilité")
        self.create_disponibilite_tab()

        # Onglet de gestion des entrées/sorties
        self.gestion_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.gestion_tab, text="Gérer les entrées/sorties")
        self.create_gestion_tab()

    def create_reservation_tab(self):
        """
        Crée le formulaire de réservation.
        """
        # Titre
        ttk.Label(self.reservation_tab, text="Réserver une place", style="TLabel").pack(pady=10)

        # Formulaire de réservation
        form_frame = ttk.Frame(self.reservation_tab)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="Numéro de place :").grid(row=0, column=0, padx=10, pady=10)
        self.numero_place_entry = ttk.Entry(form_frame, font=("Helvetica", 12))
        self.numero_place_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(form_frame, text="Nom de l'utilisateur :").grid(row=1, column=0, padx=10, pady=10)
        self.nom_utilisateur_entry = ttk.Entry(form_frame, font=("Helvetica", 12))
        self.nom_utilisateur_entry.grid(row=1, column=1, padx=10, pady=10)

        # Sélecteur de type de véhicule
        ttk.Label(form_frame, text="Type de véhicule :").grid(row=2, column=0, padx=10, pady=10)
        self.type_vehicule_var = tk.StringVar()
        self.type_vehicule_combobox = ttk.Combobox(form_frame, textvariable=self.type_vehicule_var, values=["voiture", "moto"], font=("Helvetica", 12))
        self.type_vehicule_combobox.set("voiture")  # Valeur par défaut
        self.type_vehicule_combobox.grid(row=2, column=1, padx=10, pady=10)

        # Sélecteur de date personnalisé (jour, mois, année)
        ttk.Label(form_frame, text="Date de réservation :").grid(row=3, column=0, padx=10, pady=10)
        date_frame = ttk.Frame(form_frame)
        date_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Jour (1 à 31)
        self.jour_entry = ttk.Combobox(date_frame, values=[f"{i:02d}" for i in range(1, 32)], width=3, font=("Helvetica", 12))
        self.jour_entry.grid(row=0, column=0)

        ttk.Label(date_frame, text="/", style="TLabel").grid(row=0, column=1)

        # Mois (1 à 12)
        self.mois_entry = ttk.Combobox(date_frame, values=[f"{i:02d}" for i in range(1, 13)], width=3, font=("Helvetica", 12))
        self.mois_entry.grid(row=0, column=2)

        ttk.Label(date_frame, text="/", style="TLabel").grid(row=0, column=3)

        # Année (de l'année en cours à +5 ans)
        annee_actuelle = date.today().year
        self.annee_entry = ttk.Combobox(date_frame, values=[f"{i}" for i in range(annee_actuelle, annee_actuelle + 6)], width=5, font=("Helvetica", 12))
        self.annee_entry.grid(row=0, column=4)

        # Par défaut : la date du jour
        self.date_par_defaut()

        # Heure de début
        ttk.Label(form_frame, text="Heure de début :").grid(row=4, column=0, padx=10, pady=10)
        heure_debut_frame = ttk.Frame(form_frame)
        heure_debut_frame.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.heure_debut_h = ttk.Combobox(heure_debut_frame, values=[f"{i:02d}" for i in range(24)], width=3, font=("Helvetica", 12))
        self.heure_debut_h.set("00")  # Valeur par défaut
        self.heure_debut_h.grid(row=0, column=0)

        ttk.Label(heure_debut_frame, text=":", style="TLabel").grid(row=0, column=1)

        self.heure_debut_m = ttk.Combobox(heure_debut_frame, values=[f"{i:02d}" for i in range(60)], width=3, font=("Helvetica", 12))
        self.heure_debut_m.set("00")  # Valeur par défaut
        self.heure_debut_m.grid(row=0, column=2)

        # Heure de fin
        ttk.Label(form_frame, text="Heure de fin :").grid(row=5, column=0, padx=10, pady=10)
        heure_fin_frame = ttk.Frame(form_frame)
        heure_fin_frame.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.heure_fin_h = ttk.Combobox(heure_fin_frame, values=[f"{i:02d}" for i in range(24)], width=3, font=("Helvetica", 12))
        self.heure_fin_h.set("00")  # Valeur par défaut
        self.heure_fin_h.grid(row=0, column=0)

        ttk.Label(heure_fin_frame, text=":", style="TLabel").grid(row=0, column=1)

        self.heure_fin_m = ttk.Combobox(heure_fin_frame, values=[f"{i:02d}" for i in range(60)], width=3, font=("Helvetica", 12))
        self.heure_fin_m.set("00")  # Valeur par défaut
        self.heure_fin_m.grid(row=0, column=2)

        # Bouton avec une ombre et une couleur de survol
        ttk.Button(form_frame, text="Réserver", command=self.controller.reserver_place, style="TButton").grid(row=6, column=0, columnspan=2, pady=20)

    def create_disponibilite_tab(self):
        """
        Crée le tableau des places disponibles avec un filtre par type de véhicule.
        """
        # Titre
        ttk.Label(self.disponibilite_tab, text="Places disponibles", style="TLabel").pack(pady=10)

        # Filtre par type de véhicule
        filter_frame = ttk.Frame(self.disponibilite_tab)
        filter_frame.pack(pady=10)

        ttk.Label(filter_frame, text="Filtrer par type de véhicule :", style="TLabel").grid(row=0, column=0, padx=10, pady=10)
        self.filter_type_var = tk.StringVar()
        self.filter_type_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_type_var, values=["Tous", "voiture", "moto"], font=("Helvetica", 12))
        self.filter_type_combobox.set("Tous")  # Valeur par défaut
        self.filter_type_combobox.grid(row=0, column=1, padx=10, pady=10)

        # Bouton pour appliquer le filtre
        ttk.Button(filter_frame, text="Appliquer", command=self.controller.appliquer_filtre, style="TButton").grid(row=0, column=2, padx=10, pady=10)

        # Liste des places disponibles
        self.disponibilite_tree = ttk.Treeview(
            self.disponibilite_tab,
            columns=("ID", "Numéro", "Type", "Disponible"),
            show="headings"
        )
        self.disponibilite_tree.heading("ID", text="ID")
        self.disponibilite_tree.heading("Numéro", text="Numéro")
        self.disponibilite_tree.heading("Type", text="Type")
        self.disponibilite_tree.heading("Disponible", text="Disponible")
        self.disponibilite_tree.pack(fill="both", expand=True, padx=20, pady=20)

        # Bouton avec une ombre et une couleur de survol
        ttk.Button(self.disponibilite_tab, text="Actualiser", command=self.controller.actualiser_disponibilite, style="TButton").pack(pady=10)

    def create_gestion_tab(self):
        """
        Crée l'interface de gestion des entrées/sorties.
        """
        # Titre
        ttk.Label(self.gestion_tab, text="Gérer les entrées et sorties", style="TLabel").pack(pady=10)

        # Formulaire de gestion
        form_frame = ttk.Frame(self.gestion_tab)
        form_frame.pack(pady=20)

        ttk.Label(form_frame, text="ID de la place :").grid(row=0, column=0, padx=10, pady=10)
        self.id_place_entry = ttk.Entry(form_frame, font=("Helvetica", 12))
        self.id_place_entry.grid(row=0, column=1, padx=10, pady=10)

        # Boutons avec des ombres et des couleurs de survol
        ttk.Button(form_frame, text="Enregistrer l'entrée", command=self.controller.enregistrer_entree, style="TButton").grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(form_frame, text="Enregistrer la sortie", command=self.controller.enregistrer_sortie, style="TButton").grid(row=1, column=1, padx=10, pady=10)

    def date_par_defaut(self):
        """
        Place la date du jour dans le sélecteur de date de réservation.
        """
        aujourd_hui = date.today()
        self.jour_entry.set(f"{aujourd_hui.day:02d}")
        self.mois_entry.set(f"{aujourd_hui.month:02d}")
        self.annee_entry.set(f"{aujourd_hui.year}")

    def vider_champs_reservation(self):
        """
        Efface le contenu des champs du formulaire de réservation.
        """
        self.numero_place_entry.delete(0, tk.END)
        self.nom_utilisateur_entry.delete(0, tk.END)
        self.date_par_defaut()  # Remettre la date du jour
        self.heure_debut_h.set("00")  # Réinitialiser l'heure de début
        self.heure_debut_m.set("00")
        self.heure_fin_h.set("00")  # Réinitialiser l'heure de fin
        self.heure_fin_m.set("00")