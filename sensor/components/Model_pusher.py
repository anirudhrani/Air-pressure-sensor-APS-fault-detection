# Creates and saves the model in saved_models folder.
import os
import sys

from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelEvaluationArtifact, ModelTrainerArtifact
from sensor.exception import SensorException
from sensor.utils import serialize, deserialize


class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig,
                       data_transformation_artifact: DataTransformationArtifact,
                       model_evaluation_artifact: ModelEvaluationArtifact,
                       model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_pusher_config= model_pusher_config
            self.data_transformation_artifact= data_transformation_artifact
            self.model_evaluation_artifact= model_evaluation_artifact
            self.model_trainer_artifact= model_trainer_artifact

        except Exception as e:
            print(f"\n Error: {e}")
            raise SensorException(e, sys)
    
    def initite_model_pusher(self):
        try:
            pass
        except Exception as e:
            print(f"\nError: {e}")
            raise SensorException(e, sys)