#main.py
import tkinter as tk
from view import ParkingView
from controller import ParkingController

if __name__ == "__main__":
    root = tk.Tk()
    controller = ParkingController(None)  # Le contrôleur sera lié à la vue
    view = ParkingView(root, controller)
    controller.view = view  # Lier la vue au contrôleur
    root.mainloop()