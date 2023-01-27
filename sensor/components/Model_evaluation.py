import os
import sys
import pandas as pd
import numpy as np
from typing import Optional

from sensor.exception import SensorException
from sensor.predictor import ModelLocator
from sensor.logger import logging
from sensor.entity import config_entity, artifact_entity
from sensor import utils 
from sensor.config import TARGET_COLUMN




class ModelEvaluation:
    def __init__(self,
                 model_evaluation_config: config_entity.ModelEvaluationConfig,
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
                 data_transformation_artifact: artifact_entity.DataTransformationArtifact,
                 model_trainer_artifact: artifact_entity.ModelTrainerArtifact) -> None:
        try:
            self.model_evaluation_config= model_evaluation_config
            self.data_ingestion_artifact= data_ingestion_artifact
            self.data_transformation_artifact= data_transformation_artifact
            self.model_trainer_artifact= model_trainer_artifact

            self.model_locator= ModelLocator
        except Exception as e:
            print(f"\nError : {e}")
            raise SensorException(e, sys)


    def initiate_model_evaluation(self):
        try:
            latest_dir_path= self.model_locator.get_latest_dir_path()
            
        except Exception as e:
            print(f"\nError : {e}")
            raise SensorException(e, sys)