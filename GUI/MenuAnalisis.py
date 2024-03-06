#Logica para realizar el procesamiento de los datos extraidos de los archivos .bag

import tkinter as tk
from tkinter import filedialog, messagebox
from LogicaAnalisis.AnalizadorDeterioros import AnalizadorDeterioros # Asegúrate de tener el path correcto
import os
import subprocess
import sys

class MenuAnalisis:
    def __init__(self, master):
        self.master = master
        self.master.title("Análisis de Baches")
        self.setup_gui()
        self.carpeta_destino = None
        
    def setup_gui(self):
        self.label_carpeta = tk.Label(self.master, text="Selecciona la carpeta para el análisis:")
        self.label_carpeta.pack(pady=5)
        
        self.boton_seleccionar_carpeta = tk.Button(self.master, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        self.boton_seleccionar_carpeta.pack(pady=10)

        self.boton_empezar_analisis= tk.Button(self.master, text="Empezar Análisis", command=self.analizar_datos)
        self.boton_empezar_analisis.pack(pady=10)

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

    def analizar_datos(self):
        #Ejecutar el análisis de los datos
        analizador = AnalizadorDeterioros()
        analizador.analizar_deterioros(self.carpeta_destino)