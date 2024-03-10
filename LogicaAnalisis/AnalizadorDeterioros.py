from LogicaAnalisis.AdministradorDeArchivos import AdministradorArchivos
from LogicaAnalisis.ModeloSegmentacion import ModeloSegmentacion
from LogicaAnalisis.CargarModelo import CargarModelo
from LogicaAnalisis.Bache import Bache
import concurrent.futures
import os
import torch

class AnalizadorDeterioros:
    def __init__(self):
        self.modelo_entrenado = None
        self.lista_baches = []
        self.baches_filtrados = [] 

    def cargar_modelo(self):
        modelo = CargarModelo()
        self.modelo_entrenado = modelo.cargar_modelo("LogicaAnalisis\RutaModelo\model_state_dictV5.pth")
        #Si cuda esta activado mover el modelo a cuda
        if torch.cuda.is_available():
            self.modelo_entrenado.to('cuda')
        else:
            print("CUDA no está disponible, el modelo se ejecutará en CPU.")
        return self.modelo_entrenado




    def procesar_imagenes(self,carpeta_base):
    
        segmentador = ModeloSegmentacion(self.modelo_entrenado)
        administrador_archivos = AdministradorArchivos(carpeta_base)
    
        archivos_bags = administrador_archivos.generar_lista_de_archivosBags()
        for ruta_carpeta_bag in archivos_bags:
            imagenes = administrador_archivos.generar_lista_de_imagenes(ruta_carpeta_bag)
            for ruta_imagen in imagenes:
                coordenadas_baches = segmentador.obtener_coordenadas_baches(ruta_imagen)
                for i, coord in enumerate(coordenadas_baches):
                    # Generar un ID único para cada bache
                    id_bache = f"{os.path.splitext(os.path.basename(ruta_imagen))[0]}_{i}"
                    bache = Bache(ruta_carpeta_bag, ruta_imagen, id_bache, coord)
                    # Procesar el bache (calcular contorno, radio máximo, etc.)
                    bache.calcular_contorno()
                    bache.calcular_radio_maximo()
                    print(f"El radio máximo del bache {bache.id_bache} es {bache.diametro_bache} mm procedente del bag {bache.bag_de_origen}.")
                    # Asumiendo que existe una lista para almacenar baches detectados
                    self.lista_baches.append(bache)
        return self.lista_baches
    
    def filtrar_baches_por_radio(self,baches, diametro_minimo, diamtro_maximo):
        baches_filtrados = [bache for bache in baches if diametro_minimo <= bache.diametro_bache <= diamtro_maximo]
        #Checar que la nube de puntos de los baches no este vacia
        #for bache in baches_filtrados:
        #    tiene_puntos = bache.revisar_nube_puntos_no_este_vacia()
        #    if not tiene_puntos:
        #        print(f"La nube de puntos del bache {bache.id_bache} está vacía.")
        #        #borrar bache de la lista
        #        baches_filtrados.remove(bache) 
        return baches_filtrados
    
    
    def filtrar_y_procesar_baches(self, diametro_minimo, diametro_maximo):
        self.lista_baches = self.filtrar_baches_por_radio(self.lista_baches, diametro_minimo, diametro_maximo)
        print(f"Se encontraron {len(self.lista_baches)} baches con un diámetro entre {diametro_minimo} y {diametro_maximo} unidades.")
        #Eliminar de la lista de baches los que no cumplan con el radio
        self.procesar_nubes_de_puntos()
        for bache in self.lista_baches:
            bache.estimar_profundidad()
            print(f"La profundidad estimada del bache {bache.id_bache} es {bache.profundidad_del_bache} m.")
    
    #Con la lista de baches filtrados por radio se puede hacer el procesamiento de nubes de puntos
    #Se puede hacer el procesamiento de nubes de puntos en paralelo
    def procesar_nubes_de_puntos(self):
        baches_validos = []
        for bache in self.lista_baches:
            if bache.set_altura_captura(bache.nube_puntos):  # Asumiendo que `nube_puntos` es accesible
                bache.procesar_nube_puntos()  # Asumiendo que este método hace algo con la nube de puntos válida
                print(f"Se procesó la nube de puntos del bache {bache.id_bache} procedente del bag {bache.bag_de_origen}.")
                baches_validos.append(bache)
        return baches_validos  # Devuelve solo los baches con nubes de puntos no vacías

    def guardar_informacion_baches(self,lista_baches, nombre_archivo):
        with open(nombre_archivo, 'w') as archivo:
            for bache in lista_baches:
                # Compilando la información del bache en una cadena de texto
                informacion_bache = f"ID: {bache.id_bache}, Profundidad: {bache.profundidad_del_bache} m, Diámetro: {bache.diametro_bache} mm, Origen: {bache.bag_de_origen}\n, Altura de captura: {bache.altura_captura} m\n"
                # Escribir la información compilada en el archivo
                archivo.write(informacion_bache)
        print(f"La información de los baches ha sido guardada en {nombre_archivo}.")
       #Funcion a llamar desde el boton de analizar.
    def analizar_deterioros(self, carpeta_base):
        ruta_carpeta_archivos = carpeta_base #Variable que se debe obtener del boton de seleccionar carpeta.
        self.cargar_modelo()
        self.lista_baches = self.procesar_imagenes(ruta_carpeta_archivos)
        diametro_minimo = 150
        diametro_maximo = 1000
        self.filtrar_y_procesar_baches( diametro_minimo, diametro_maximo)
        self.guardar_informacion_baches(self.lista_baches, "informacion_Resultados_baches.txt")
    