#main.py
import tkinter as tk
from view import ParkingView
from controller import ParkingController


def fermer_application(root, controller):
    """
    Ferme la connexion à la base de données puis la fenêtre.
    """
    controller.model.fermer()
    root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    controller = ParkingController(None)  # Le contrôleur sera lié à la vue
    view = ParkingView(root, controller)
    controller.view = view  # Lier la vue au contrôleur
    root.protocol("WM_DELETE_WINDOW", lambda: fermer_application(root, controller))
    root.mainloop()
