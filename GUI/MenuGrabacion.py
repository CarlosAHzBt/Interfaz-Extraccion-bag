#Logica para realizar la grabacion de los archivos .bag con la informacion de los sensores.

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
from LogicaCapturaDatos.GrabadorBag import GrabadorBag  # Asegúrate de tener el path correcto

class MenuGrabacion:
    def __init__(self, master):
        self.master = master
        self.setup_gui()
        self.grabador = GrabadorBag()

    def setup_gui(self):
        self.label_carpeta = tk.Label(self.master, text="Carpeta de destino no seleccionada")
        self.label_carpeta.pack(pady=5)

        boton_seleccionar_carpeta = tk.Button(self.master, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        boton_seleccionar_carpeta.pack(pady=5)

        boton_grabar = tk.Button(self.master, text="Iniciar Grabación", command=self.iniciar_grabacion)
        boton_grabar.pack(pady=5)

    def seleccionar_carpeta(self):
        self.carpeta_destino = filedialog.askdirectory()
        if self.carpeta_destino:
            self.label_carpeta.config(text="Carpeta de destino seleccionada: " + self.carpeta_destino)

    def iniciar_grabacion(self):
        if not self.carpeta_destino:
            messagebox.showerror("Error", "Por favor selecciona una carpeta de destino.")
            return
        self.grabador.start_recording(self.carpeta_destino)
        messagebox.showinfo("Grabación Iniciada", "La grabación ha comenzado.")
        self.master.destroy()