#Logica del menu para extraer la informacion de los archivos bag

import tkinter as tk
from tkinter import filedialog, messagebox
import os
from LogicaExtraccionBag.ProcesadorBags import ProcesadorBags  # Asegúrate de tener el path correcto
import sys
import subprocess
class MenuExtraccion:
    def __init__(self, master):
        self.master = master
        self.setup_gui()
        self.carpeta_destino = None

    def setup_gui(self):
        self.label_carpeta = tk.Label(self.master, text="Selecciona la carpeta para extraer la información:")
        boton_seleccionar_carpeta = tk.Button(self.master, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        boton_seleccionar_carpeta.pack(pady=10)

        boton_extraer = tk.Button(self.master, text="Extraer información de Captura", command=self.extraer_informacion)
        boton_extraer.pack(pady=10)

    #Seleccionar Carpeta
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
                procesador.process_bag_file(bag_file,self.carpeta_destino)
            messagebox.showinfo("Proceso Completado", "Todos los archivos .bag seleccionados han sido procesados.")