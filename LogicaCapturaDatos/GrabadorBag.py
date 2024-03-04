# GrabadorBag.py
from LogicaCapturaDatos.Config import Config
import pyrealsense2 as rs
import numpy as np
import cv2
import time
import os

class GrabadorBag:
    def __init__(self, archivo_config=None):
        self.carpeta_destino = carpeta_destino
        # Iniciar el pipeline
        self.pipeline = rs.pipeline()
        # Cargar el archivo de configuración
        self.config = Config(archivo_config) if archivo_config else None
        self.config_data = self.config.load_config() if self.config else {}
        # Configuración para la grabación
        self.config_bag = rs.config()
        self.num_archivo = 0
        self.grabando = False

    def iniciar_grabacion(self, carpeta_destino):
        # Define el nombre del archivo .bag donde se guardarán los datos
        nombre_archivo = os.path.join(carpeta_destino, f"grabacion_{self.num_archivo}.bag")
        self.guardar_archivo(nombre_archivo)

        # Inicia la grabación con la configuración especificada
        try:
            self.pipeline.start(self.config_bag)
            self.grabando = True
            print(f"Iniciando grabación en {nombre_archivo}...")

            # Grabar en intervalos de 30 segundos
            inicio = time.time()
            while self.grabando and time.time() - inicio < 30:
                time.sleep(1)  # Espera activa para simplificar el ejemplo

            if self.grabando:
                self.detener_grabacion()

            self.num_archivo += 1
        except Exception as e:
            print(f"Error al iniciar la grabación: {e}")
            self.detener_grabacion()

    def detener_grabacion(self):
        if self.grabando:
            self.pipeline.stop()
            self.grabando = False
            print("Grabación detenida.")

    def guardar_archivo(self, archivo):
        if not os.path.exists(os.path.dirname(archivo)):
            os.makedirs(os.path.dirname(archivo))
        self.config_bag.enable_record_to_file(archivo)
        print(f"Configuración para guardar archivo establecida: {archivo}")

    def mostrar_ventana(self):
        if not self.grabando:
            print("La grabación no está activa.")
            return

        try:
            while self.grabando:
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                if not color_frame:
                    continue

                color_image = np.asanyarray(color_frame.get_data())
                cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('RealSense', color_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cv2.destroyAllWindows()
