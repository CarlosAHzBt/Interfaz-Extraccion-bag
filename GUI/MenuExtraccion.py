#Logica del menu para extraer la informacion de los archivos bag

import tkinter as tk
from tkinter import filedialog, messagebox
import os
from LogicaExtraccionBag.ProcesadorBags import ProcesadorBags  # Asegúrate de tener el path correcto

class MenuExtraccion:
    def __init__(self, master):
        self.master = master
        self.setup_gui()

    def setup_gui(self):
        boton_extraer = tk.Button(self.master, text="Extraer información de Captura", command=self.extraer_informacion)
        boton_extraer.pack(pady=10)

    #FUNCIONALIDAD PARA EXTRAER LA INFORMACION GRABADA EN LOS ARCHIVOS .BAG
    def extraer_informacion(self):
        messagebox.showinfo("Extraer Información", "Selecciona archivos .bag o una carpeta que los contenga.")
        files = filedialog.askopenfilenames(filetypes=[("Bag files", "*.bag")])
        if not files:
            folder = filedialog.askdirectory()
            if folder:
                procesador = ProcesadorBags(folder)
                procesador.process_bag_files()
                messagebox.showinfo("Proceso Completado", "Todos los archivos .bag han sido procesados.")
        else:
            for file_path in files:
                directory, bag_file = os.path.split(file_path)
                procesador = ProcesadorBags(directory)
                procesador.process_bag_file(bag_file)
            messagebox.showinfo("Proceso Completado", "Todos los archivos .bag seleccionados han sido procesados.")