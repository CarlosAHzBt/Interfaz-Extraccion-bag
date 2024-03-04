#Logica del menu para acceder al resto de los menus

import tkinter as tk
from tkinter import filedialog, messagebox
import os
from GUI.MenuExtraccion import MenuExtraccion
from GUI.MenuGrabacion import MenuGrabacion
from GUI.MenuAnalisis import MenuAnalisis

class MenuPrincipal:
    def __init__(self, master):
        self.master = master
        self.setup_gui()

    def setup_gui(self):
        boton_menu_extraccion = tk.Button(self.master, text="Menu de Extracción", command=self.abrir_menu_extraccion)
        boton_menu_extraccion.pack(pady=10)

        boton_menu_grabacion = tk.Button(self.master, text="Menu de Grabación", command=self.abrir_menu_grabacion)
        boton_menu_grabacion.pack(pady=10)

        boton_menu_analisis = tk.Button(self.master, text="Menu de Análisis", command=self.abrir_menu_analisis)
        boton_menu_analisis.pack(pady=10)

    def abrir_menu_extraccion(self):
        self.nueva_ventana = tk.Toplevel(self.master)
        self.app_secundaria = MenuExtraccion(master=self.nueva_ventana)

    def abrir_menu_grabacion(self):
        self.nueva_ventana = tk.Toplevel(self.master)
        self.app_secundaria = MenuGrabacion(master=self.nueva_ventana)

    def abrir_menu_analisis(self):
        self.nueva_ventana = tk.Toplevel(self.master)
        self.app_secundaria = MenuAnalisis(master=self.nueva_ventana)
        