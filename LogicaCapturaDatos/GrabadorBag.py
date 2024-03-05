import pyrealsense2 as rs
import time
import datetime
import os
import threading

class GrabadorBag:
    def __init__(self, duracion=15):
        self.config = rs.config()
        self.duracion = duracion
        self.configurar_streams()
        self.grabando = False
        self.finalizado = threading.Event()  # Para sincronizar la finalización de la grabación
        self.pipeline_activa = False  # Añadir esta línea


    def configurar_streams(self):
        self.config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
        self.config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)

    def generar_nombre_archivo_en_carpeta_seleccionada(self, carpeta_destino):
        nombre_archivo = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".bag"
        return os.path.join(carpeta_destino, nombre_archivo)

    def grabar_segmento(self, carpeta_destino):
        nombre_archivo = self.generar_nombre_archivo_en_carpeta_seleccionada(carpeta_destino)
        self.config.enable_record_to_file(nombre_archivo)
        self.pipeline = rs.pipeline()
        self.pipeline.start(self.config)
        self.pipeline_activa = True  # Establecer a True después de llamar a start()
        print(f"Grabación iniciada, guardando en {nombre_archivo}.")

        inicio = time.time()
        while time.time() - inicio < self.duracion and self.grabando:
            time.sleep(0.01)

        if self.pipeline_activa:  # Verificar antes de llamar a stop()
            self.pipeline.stop()
            self.pipeline_activa = False  # Establecer a False después de detener la pipeline
        print("Grabación detenida.")

    def ejecutar_grabacion(self, carpeta_destino):
        self.grabando = True
        self.finalizado.clear()  # Prepara el evento para una nueva sesión de grabación
        while self.grabando:
            self.grabar_segmento(carpeta_destino)
        self.finalizado.set()  # Indica que la grabación ha finalizado

    def detener_grabacion(self):
        self.grabando = False
        # Asumiendo que self.pipeline puede haber sido inicializado pero no necesariamente empezado
        try:
            if self.pipeline_activa:
                self.pipeline.stop()
                print("Pipeline detenido correctamente.")
        except Exception as e:
            print(f"Error al detener el pipeline: {e}")
        finally:
            self.pipeline_activa = False  # Asegura que el estado refleje que el pipeline ya no está activo
    
        self.finalizado.set()  # Indica la finalización para cualquier espera pendiente
    def cerrar_pipeline(self):
        if self.pipeline_activa:
            self.pipeline.stop()
            self.pipeline_activa = False
            print("Pipeline cerrado correctamente.")