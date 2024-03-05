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
        self.grabador = GrabadorBag(15)
        self.carpeta_destino = None

        # Añade un manejador de evento para el cierre de la ventana
        self.master.protocol("WM_DELETE_WINDOW", self.on_cerrar)
        

    def setup_gui(self):
        self.label_carpeta = tk.Label(self.master, text="Carpeta de destino no seleccionada")
        self.label_carpeta.pack(pady=5)

        boton_seleccionar_carpeta = tk.Button(self.master, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        boton_seleccionar_carpeta.pack(pady=5)

        boton_grabar = tk.Button(self.master, text="Iniciar Grabación", command=self.iniciar_grabacion)
        boton_grabar.pack(pady=5)

        boton_detener_grabacion = tk.Button(self.master, text="Detener Grabación", command=self.detener_grabacion)
        boton_detener_grabacion.pack(pady=5)
        # Asumiendo que el resto de la inicialización de la clase permanece igual
        boton_cerrar_pipeline = tk.Button(self.master, text="Cerrar Pipeline", command=self.cerrar_pipeline)
        boton_cerrar_pipeline.pack(pady=5)
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
        self.hilo_grabacion = threading.Thread(target=self.grabador.ejecutar_grabacion, args=(self.carpeta_destino,), daemon=True)
        self.hilo_grabacion.start()
        messagebox.showinfo("Grabación Iniciada", "La grabación ha comenzado.")

    def detener_grabacion(self):
        if not self.carpeta_destino:  # Si no se ha seleccionado carpeta o iniciado la grabación, no hacer nada
            return
        self.grabador.detener_grabacion()  # Configura `self.grabando` en `False` para detener la grabación
        self.hilo_grabacion.join()  # Espera a que el hilo de grabación termine
        messagebox.showinfo("Grabación Detenida", "La grabación ha sido detenida correctamente.")

    def on_cerrar(self):
        """Manejador para el evento de cierre de la ventana."""
        if messagebox.askokcancel("Salir", "¿Estás seguro de que quieres salir?"):
            self.detener_grabacion()  # Asegura la detención adecuada de la grabación
            self.grabador.cerrar_pipeline()  # Asegura que el pipeline se cierra correctamente
            self.master.destroy()  # Cierra la ventana
            sys.exit()  # Cierra toda la aplicación
    def cerrar_pipeline(self):
        self.grabador.cerrar_pipeline()
        messagebox.showinfo("Pipeline Cerrado", "El pipeline se ha cerrado correctamente.")