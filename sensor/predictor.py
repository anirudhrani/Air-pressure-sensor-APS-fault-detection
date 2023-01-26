import os
import sys
import pickle
from glob import glob
from sensor.exception import SensorException
from sensor.entity.config_entity import MODEL_FILE_NAME, TRANSFORMER_OBJECT_FILE_NAME, TARGET_ENCODER_OBJECT

class ModelResolver:

    def __init__(self, model_registry: str = "saved_models",
                 transformer_dir_name= "transformer",
                 target_encoder_dir_name= "target_encoder",
                 model_dir_name= "model"):

        self.model_registry= model_registry
        self.transformer_dir_name= transformer_dir_name
        self.target_encoder_dir_name= target_encoder_dir_name
        self.model_dir_name= model_dir_name


    def get_latest_dir_path(self):
        try:
            dir_names= os.listdir(self.model_registry)
            dir_names= list(map(int, dir_names))
            latest_folder_name= max(dir_names)
            return os.path.join(self.model_registry, f"{latest_folder_name}")
        except Exception as e:
            raise SensorException(e, sys)

    def get_latest_model_path(self):
        try:
            latest_dir= self.get_latest_dir_path()
            return os.path.join(latest_dir, self.model_dir_name, MODEL_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)
    
    def get_latest_transformer_path(self):
        try:
            latest_dir= self.get_latest_dir_path()
            return  os.path.join(latest_dir, TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise SensorException(e, sys)
    
    def get_latest_target_encoder_path(self):
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Target encoder is not available")
            return os.path.join(latest_dir,self.target_encoder_dir_name,TARGET_ENCODER_OBJECT)
        except Exception as e:
            raise SensorException(e, sys)

    def get_latest_saved_dir_path(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)

    def get_latest_target_encoder_path(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e, sys)    





