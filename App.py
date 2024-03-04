import tkinter as tk
from GUI.MenuPrincipal import MenuPrincipal
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramienta de Procesamiento")
        self.gui_handler = MenuPrincipal(root)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()