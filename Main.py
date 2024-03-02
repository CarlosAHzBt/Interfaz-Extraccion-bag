import tkinter as tk
from tkinter import filedialog, messagebox
import os
from LogicaExtraccionBag.BagFile import BagFile  # Asegúrate de tener el path correcto
from LogicaExtraccionBag.ProcesadorBags import ProcesadorBags  # Asegúrate de tener el path correcto

def extraer_informacion():
    messagebox.showinfo("Extraer Información", "Selecciona archivos .bag o una carpeta que los contenga.")
    files = filedialog.askopenfilenames(filetypes=[("Bag files", "*.bag")])
    if not files:
        # Si no se seleccionaron archivos, intenta seleccionar una carpeta
        folder = filedialog.askdirectory()
        if folder:
            # Procesar todos los archivos .bag en la carpeta seleccionada
            procesador = ProcesadorBags(folder)
            procesador.process_bag_files()
            messagebox.showinfo("Proceso Completado", "Todos los archivos .bag han sido procesados.")
    else:
        # Procesar archivos .bag seleccionados individualmente
        for file_path in files:
            # Aquí, necesitas extraer el directorio y el nombre del archivo para usar tu clase correctamente
            directory, bag_file = os.path.split(file_path)
            procesador = ProcesadorBags(directory)
            procesador.process_bag_file(bag_file)
        messagebox.showinfo("Proceso Completado", "Todos los archivos .bag seleccionados han sido procesados.")

def capturar_datos():
    messagebox.showinfo("Capturar Datos", "Esta funcionalidad aún no está implementada.")

root = tk.Tk()
root.title("Herramienta de Procesamiento")

boton_extraer = tk.Button(root, text="Extraer información de Captura", command=extraer_informacion)
boton_extraer.pack(pady=10)

boton_capturar = tk.Button(root, text="Capturar Datos", command=capturar_datos)
boton_capturar.pack(pady=10)

root.mainloop()
