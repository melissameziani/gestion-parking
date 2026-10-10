<div align="center">

# 🅿️ Gestion de Parking

**Application de bureau pour gérer les réservations, la disponibilité et les entrées / sorties d'un parking**

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/Interface-Tkinter-FFCC00)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?logo=mysql&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-MVC-2EA44F)

</div>

---

## 🎯 Présentation

Cette application permet à un gestionnaire de parking de :

- **réserver une place** pour un client, à une date et sur un créneau horaire précis ;
- **consulter en temps réel** les places libres ;
- **enregistrer l'entrée et la sortie** des véhicules.

Le parking compte **40 places** : 20 pour les voitures (`V1` à `V20`) et 20 pour les motos (`M1` à `M20`).

## ✨ Fonctionnalités

**📅 Réservation**
- Choix de la place, du client, du type de véhicule, de la date et des heures
- **Détection des conflits** : une place ne peut pas être réservée deux fois sur le même créneau
- Vérification que la place correspond au type de véhicule (une moto ne peut pas prendre une place voiture)
- Refus des dates passées et des créneaux incohérents (heure de fin avant l'heure de début)

**🔎 Disponibilité**
- Tableau des places libres
- Filtre par type de véhicule : tous, voiture ou moto

**🚗 Entrées / sorties**
- Enregistrement de l'arrivée d'un véhicule : la place devient occupée
- Enregistrement du départ : la place est libérée et la réservation effacée

**🎨 Interface**
- Trois onglets clairs, thème sombre, messages d'erreur et de confirmation explicites

## 🏗️ Architecture (MVC)

```
gestion_parking/
├── main.py          # Point d'entrée : crée la fenêtre et relie la vue au contrôleur
├── model.py         # Modèle : accès à la base MySQL (requêtes, réservations)
├── view.py          # Vue : interface graphique Tkinter (onglets, formulaires, tableau)
├── controller.py    # Contrôleur : validation des saisies et logique de l'application
├── database.sql     # Script de création de la base et des 40 places
└── requirements.txt # Dépendances Python
```

## 🛠️ Technologies

- **Python 3** avec **Tkinter** pour l'interface graphique
- **MySQL** pour la base de données, via `mysql-connector-python`
- Architecture **MVC** (Modèle – Vue – Contrôleur)

## 🚀 Installation et lancement

**Prérequis :** Python 3.10 ou plus, et MySQL (par exemple avec XAMPP).

**1. Récupérer le projet**

```bash
git clone https://github.com/melissameziani/gestion-parking.git
cd gestion-parking
```

**2. Installer les dépendances**

```bash
pip install -r requirements.txt
```

**3. Créer la base de données**

Démarrez MySQL, puis importez le fichier `database.sql`, au choix :
- avec **phpMyAdmin** : onglet *Importer*, puis choisir `database.sql` ;
- ou en ligne de commande :

```bash
mysql -u root < database.sql
```

**4. Lancer l'application**

```bash
python main.py
```

> Par défaut, l'application se connecte à MySQL avec l'utilisateur `root` sans mot de passe (configuration de XAMPP).
> Pour d'autres identifiants, définissez les variables d'environnement `PARKING_DB_HOST`, `PARKING_DB_USER`, `PARKING_DB_PASSWORD` et `PARKING_DB_NAME`.

## 👩‍💻 Autrice

**Melissa MEZIANI** — Développeuse web full stack
[GitHub](https://github.com/melissameziani) · [LinkedIn](https://www.linkedin.com/in/melissa-meziani-b0ba4b299) · [mezianimelissa37@gmail.com](mailto:mezianimelissa37@gmail.com)
