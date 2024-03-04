import pyrealsense2 as rs
import json
import time
import datetime

def iniciar_grabacion(config, duracion=15):
    # Generar nombre de archivo basado en la fecha y hora actual
    nombre_archivo = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".bag"
    config.enable_record_to_file(nombre_archivo)
    
    # Iniciar la grabación
    pipeline.start(config)
    print(f"Grabación iniciada, guardando en {nombre_archivo}.")
    
    # Esperar la duración especificada
    time.sleep(duracion)
    
    # Detener la grabación
    pipeline.stop()
    print("Grabación detenida.")
config = rs.config()


# Configurar la grabacion a 848x480
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)


# Configuración básica del pipeline
pipeline = rs.pipeline()

# Asumiendo que el archivo JSON ya no incluye "record_to_file"
# Aplica cualquier otra configuración necesaria aquí, como habilitar streams
# ...



# Repetir la grabación cada 15 segundos
try:
    while True:
        iniciar_grabacion(config)
        # Opcional: añadir un breve descanso entre grabaciones si es necesario
        time.sleep(1)  # Espera 1 segundo antes de iniciar la siguiente grabación
except KeyboardInterrupt:
    print("Finalizado por el usuario.")
