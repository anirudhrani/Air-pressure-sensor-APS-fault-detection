# Creates and saves the model in saved_models folder.
import os
import sys
from sensor.logger import logging
from sensor.entity.config_entity import ModelPusherConfig
from sensor.entity.artifact_entity import DataTransformationArtifact, ModelEvaluationArtifact, ModelTrainerArtifact, ModelPusherArtifact
from sensor.predictor import ModelLocator
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
            self.model_locator= ModelLocator(model_registry=self.model_pusher_config.saved_model_dir)
        except Exception as e:
            print(f"\n Error: {e}")
            raise SensorException(e, sys)
    
    def initiate_model_pusher(self):
        try:
            #1 load object
            transformer= deserialize(file_path= self.data_transformation_artifact.transform_object_path)
            model= deserialize(file_path= self.model_trainer_artifact.model_path)
            target_encoder= deserialize(file_path= self.data_transformation_artifact.target_encoder_path)
            logging.info(f"Loaded model, transformer and target encoder.")

            #2
            serialize(file_path= self.model_pusher_config.push_transformer_to_path, obj= transformer)
            serialize(file_path= self.model_pusher_config.push_model_to_path, obj= model)
            serialize(file_path= self.model_pusher_config.push_target_encoder_to_path, obj= target_encoder)

            transformer_path= self.model_locator.get_latest_save_transformer_path()
            model_path= self.model_locator.get_latest_save_model_path()
            target_encoder_path= self.model_locator.get_latest_save_target_encoder_path()
            
            serialize(file_path= transformer_path, obj= transformer)
            serialize(file_path= model_path, obj= model)
            serialize(file_path= target_encoder_path, obj= target_encoder)
            
            model_pusher_artifact= ModelPusherArtifact(pusher_model_dir= self.model_pusher_config.push_model_to_path, 
                                                        saved_model_dir= self.model_pusher_config.saved_model_dir)
            return model_pusher_artifact
        except Exception as e:
            print(f"\nError: {e}")
            raise SensorException(e, sys)