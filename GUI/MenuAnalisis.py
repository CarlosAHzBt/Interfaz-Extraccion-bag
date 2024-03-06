#Logica para realizar el procesamiento de los datos extraidos de los archivos .bag

import tkinter as tk
from tkinter import filedialog, messagebox
import os
from LogicaAnalisis import AnalizadorDeterioros # Asegúrate de tener el path correcto


class MenuAnalisis:
    def __init__(self, master):
        self.master = master
        self.master.title("Análisis de Baches")
        self.setup_gui()
        
    def setup_gui(self):
        self.label_carpeta = tk.Label(self.master, text="Selecciona la carpeta para el análisis:")
        self.label_carpeta.pack(pady=5)
        
        self.boton_seleccionar_carpeta = tk.Button(self.master, text="Seleccionar Carpeta y Analizar", command=self.seleccionar_carpeta)
        self.boton_seleccionar_carpeta.pack(pady=10)
    
    def seleccionar_carpeta(self):
        # Abre el diálogo para que el usuario seleccione la carpeta
        carpeta_base = filedialog.askdirectory(title="Selecciona la carpeta con los datos para el análisis")
        if carpeta_base:  # Verifica que el usuario no haya cancelado la selección de carpeta
            self.analizar_datos(carpeta_base)

    def analizar_datos(self, carpeta_base):
        #Ejecutar el análisis de los datos
        analizador = AnalizadorDeterioros()
        analizador.analizar_deterioros(carpeta_base)