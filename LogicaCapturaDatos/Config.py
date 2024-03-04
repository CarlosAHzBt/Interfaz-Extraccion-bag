#Clase para cargar la configuracion del D435if para la grabacion de datos apartir del json

import json
import os
import pyrealsense2 as rs
import time

class Config:
    def __init__(self,config_file_path):
        self.config_file_path = config_file_path
        
    def load_config(self):
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, "r") as file:
                return json.load(file)
        else:
            return self.create_default_config()
    
    def create_default_config(self):
        config = {
            "color": {
                "width": 640,
                "height": 480,
                "fps": 30
            },
            "depth": {
                "width": 640,
                "height": 480,
                "fps": 30
            }
        }
        with open(self.config_file, "w") as file:
            json.dump(config, file, indent=4)
        return config
