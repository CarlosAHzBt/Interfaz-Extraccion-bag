#Logica para realizar la grabacion de los archivos .bag con la informacion de los sensores.

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import threading
import subprocess
import sys
from LogicaCapturaDatos.GrabadorBag import GrabadorBag  # Asegúrate de tener el path correcto

class MenuGrabacion:
    def __init__(self, master):
        self.master = master
        self.setup_gui()
        self.grabador = GrabadorBag()
        self.carpeta_destino = None

    def setup_gui(self):
        self.label_carpeta = tk.Label(self.master, text="Carpeta de destino no seleccionada")
        self.label_carpeta.pack(pady=5)

        boton_seleccionar_carpeta = tk.Button(self.master, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        boton_seleccionar_carpeta.pack(pady=5)

        boton_grabar = tk.Button(self.master, text="Iniciar Grabación", command=self.iniciar_grabacion)
        boton_grabar.pack(pady=5)

    def seleccionar_carpeta(self):
        if sys.platform == 'win32':
            # Comando para abrir el diálogo de selección de carpeta en Windows
            carpeta_destino = subprocess.check_output('powershell -command "Add-Type -AssemblyName System.windows.forms; $folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog; [void]$folderBrowser.ShowDialog(); $folderBrowser.SelectedPath"', shell=True).decode().strip()
        elif sys.platform == 'darwin':
            # Comando para abrir el diálogo de selección de carpeta en macOS
            carpeta_destino = subprocess.check_output('osascript -e \'tell app "Finder" to return POSIX path of (choose folder)\'', shell=True).decode().strip()
        else:
            # Comando para abrir el diálogo de selección de carpeta en Linux
            carpeta_destino = subprocess.check_output('zenity --file-selection --directory', shell=True).decode().strip()

        if carpeta_destino:
            self.carpeta_destino = carpeta_destino
            self.label_carpeta.config(text="Carpeta de destino seleccionada: " + self.carpeta_destino)
        else:
            self.label_carpeta.config(text="Carpeta de destino no seleccionada")

    def iniciar_grabacion(self):
        if not self.carpeta_destino:
            messagebox.showerror("Error", "Por favor selecciona una carpeta de destino.")
            return
        self.grabador.iniciar_grabacion(self.carpeta_destino)
        messagebox.showinfo("Grabación Iniciada", "La grabación ha comenzado.")
        self.master.destroy()

    