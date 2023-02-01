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
            self.model_locator= ModelLocator()
        except Exception as e:
            print(f"\nError : {e}")
            raise SensorException(e, sys)


    def initiate_model_evaluation(self):
        try:
            #1 
            logging.info(f"Initiated model evaluation class.")

            latest_dir_path= self.model_locator.get_latest_dir_path()
            if latest_dir_path==None:
                model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(model_accepted= True, improved_accuracy= None)
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact
            
            #2 Find locations of PREVIOSULY TRAINED data transformer, model and target encoder. 
            logging.info(f"Locating PREVIOUSLY TRAINED MODEL, TRANSFORMER AND ENCODER paths.")
            transformer_path= self.model_locator.get_latest_transformer_path()
            model_path= self.model_locator.get_latest_model_path()
            target_encoder_path= self.model_locator.get_latest_target_encoder_path()

            #3 De-serialize the binaries of PREVIOSULY TRAINED transformer, model and target encoder. 
            logging.info(f"De-serializing the binaries of transformer, model and encoder for the PREVIOUSLY TRAINED MODEL.")
            transformer = utils.deserialize(file_path= transformer_path)
            model= utils.deserialize(file_path= model_path)
            target_encoder=  utils.deserialize(file_path= target_encoder_path)

            #4 De-serialize the binaries of RECENTLY TRAINED transformer, model and target encoder.
            logging.info(f"De-serializing the binaries of transformer, model and encoder for the RECENTLY TRAINED MODEL.")
            latest_transformer= utils.deserialize(file_path= self.data_transformation_artifact.transform_object_path)
            latest_model= utils.deserialize(file_path= self.model_trainer_artifact.model_path)
            latest_target_encoder= utils.deserialize(file_path= self.data_transformation_artifact.target_encoder_path)

# PREVIOUSLY TRAINED MODEL
            #5 Load test data
            logging.info(f"Loading test data and computing the f1 score of the previously trained model.")
            test_df= pd.read_csv(self.data_ingestion_artifact.test_file_path)
            target_df= test_df[TARGET_COLUMN]
            y_true= target_encoder.transform(target_df)

            #6 Compute the accuraccy using previously trained model.

            # Take input feature names from the transformer input.
            input_feature_name = list(transformer.feature_names_in_)
            # Transform those columns by the old transfromer on test_df.
            input_arr= transformer.transform(test_df[input_feature_name])
            # Make predictions on the input array.
            y_pred= model.predict(input_arr)
            print(f"Predictions made by the previous model: {target_encoder.inverse_transform(y_pred[:5])}")

                # F1 score
            previous_model_score= f1_score(y_true= y_true, y_pred= y_pred)
            logging.info(f"PREVIOUS MODEL score : {previous_model_score}")
# RECENTLY TRAINED MODEL
            # Get the names of the features to be transformed.

            # Get the input feature names from the latest transformer.
            input_feature_name = list(latest_transformer.feature_names_in_)
            
            # Transform those columns using the latest tranformer on the input test_df.
            input_arr= latest_transformer.transform(test_df[input_feature_name])
            
            # Make predictions on the inpit array
            y_pred= latest_model.predict(input_arr)

            # Prepare y_true using target encoder.
            y_true= latest_target_encoder.transform(target_df)
            print(f"Predictions made by the previous model: {latest_target_encoder.inverse_transform(y_pred[:5])}")
            
            # Compute f1-score for the latest model.
            latest_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"CURRENT MODEL score : {latest_model_score}")
            

            #7 Compare the models
            if latest_model_score<previous_model_score:
                logging.info(f"Recently trained model is not better than previous model")
                raise Exception("Recently trained model is not better than previous model")

            model_evaluation_artifact= artifact_entity.ModelEvaluationArtifact(model_accepted=True,
                                                                                improved_accuracy= latest_model_score - previous_model_score)
            return model_evaluation_artifact
        except Exception as e:
            print(f"\nError : {e}")
            raise SensorException(e, sys)