#Logica para realizar el procesamiento de los datos extraidos de los archivos .bag

import tkinter as tk
from tkinter import filedialog, messagebox
import os


class MenuAnalisis:
    def __init__(self,master):
        self.master = master
        self.setup_gui()
    
    def setup_gui(self):
        boton_analizar = tk.Button(self.master, text="Analizar Información", command=self.analizar_informacion)
        boton_analizar.pack(pady=10)


    