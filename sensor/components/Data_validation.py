import sys
import os
from scipy.stats import ks_2samp
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity import artifact_entity, config_entity



class DataValidation:
    def __init__(self, data_validation_config: config_entity.DataValidationConfig) -> None:
        try:
            logging.info()
            self.initiate_data_validation= data_validation_config
        except Exception as e:
            raise SensorException(e, sys)
    
    

    def initiate_data_validation(self)-> artifact_entity.DataValidationArtifact:
        pass