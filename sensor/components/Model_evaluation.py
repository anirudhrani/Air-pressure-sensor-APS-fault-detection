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

from sklearn.metrics import f1_score




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
            #1 

            latest_dir_path= self.model_locator.get_latest_dir_path()
            if latest_dir_path==None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(accepted_the_model=True,
                improved_accuracy=None)
                logging.info(f"Model evaluation artifact: {model_eval_artifact}")
                return model_eval_artifact
            
            #2 Find locations of PREVIOSULY TRAINED data transformer, model and target encoder. 
            transformer_path= self.model_locator.get_latest_transformer_path()
            model_path= self.model_locator.get_latest_model_path()
            target_encoder_path= self.model_locator.get_latest_target_encoder_path

            #3 De-serialize the binaries of PREVIOSULY TRAINED transformer, model and target encoder.
            transformer = utils.deserialize(file_path= transformer_path)
            model= utils.deserialize(file_path= model_path)
            target_encoder=  utils.deserialize(file_path= target_encoder_path)

            #4 De-serialize the binaries of RECENTLY TRAINED transformer, model and target encoder.
            latest_transformer= utils.deserialize(file_path= self.data_transformation_artifact.transform_object_path)
            latest_model= utils.deserialize(file_path= self.model_trainer_artifact.model_path)
            latest_target_encoder= utils.deserialize(file_path= self.data_transformation_artifact.target_encoder_path)

            #5 Load test data
            test_df= pd.read_csv(self.data_ingestion_artifact.test_file_path)
            #6 Transform the data and perform train test split
            #7 Compare the models
            

        except Exception as e:
            print(f"\nError : {e}")
            raise SensorException(e, sys)