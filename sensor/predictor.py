import os
import sys
import pickle
from sensor.exception import SensorException

class ModelResolver:

    def __init__(self, model_registry: str = "saved_models",
                 transformer_dir_name= "transformer",
                 target_encoder_dir_name= "target_encoder",
                 model_dir_name= "model"):

        self.model_registry= model_registry

    def get_latest_model_path(self):
        try:
            dir_names= os.listdir(self.model_registry)
            dir_names= list(map(int, dir_names))
            latest_folder_name= max(dir_names)
            return os.path.join(self.model_registry, f"{latest_folder_name}")
        except Exception as e:
            raise SensorException(e, sys)




class Predictor:

    pass
