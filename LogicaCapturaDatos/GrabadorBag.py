import pyrealsense2 as rs
import time
import datetime
import os

class GrabadorBag:
    def __init__(self, duracion=15):
        self.config = rs.config()
        self.duracion = duracion
        self.configurar_streams()

    def configurar_streams(self):
        """Configura los streams de profundidad y color."""
        self.config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)

    def generar_nombre_archivo_en_carpeta_seleccionada(self,):
        """Genera un nombre de archivo basado en la fecha y hora actual."""
        #guardar el archivo en la carpeta seleccionada
        return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".bag"
         

    def iniciar_pipeline(self,carpeta_destino):
        """Inicia el pipeline de grabación con la configuración dada."""
        self.nombre_archivo = self.generar_nombre_archivo_en_carpeta_seleccionada()
        # guardar el archivo en la carpeta destino con el nombre asignado
        self.nombre_archivo = carpeta_destino + self.nombre_archivo
        self.config.enable_record_to_file(self.nombre_archivo)
        self.pipeline = rs.pipeline()
        self.pipeline.start(self.config)


    def grabar(self):
        """Realiza la grabación durante un tiempo especificado."""
        print(f"Grabación iniciada, guardando en {self.nombre_archivo}.")
        time.sleep(self.duracion)
        print("Grabación detenida.")

    def detener_pipeline(self):
        """Detiene el pipeline."""
        self.pipeline.stop()

    def guardar_bag(self, carpeta_destino):
        """Guarda el archivo .bag en la carpeta de destino."""
        self.nombre_archivo = os.path.join(carpeta_destino, self.nombre_archivo)
        os.rename(self.nombre_archivo, self.nombre_archivo)

    def ejecutar_grabacion(self, carpeta_destino):
        """Método principal para ejecutar la grabación."""
        self.carpeta_destino=carpeta_destino
        self.iniciar_pipeline(carpeta_destino)
        self.grabar()
        self.detener_pipeline()