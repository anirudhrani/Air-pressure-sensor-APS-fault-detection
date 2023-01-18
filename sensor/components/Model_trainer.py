import os
import sys
import pandas as pd
import numpy as np
from typing import Optional

from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity import config_entity, artifact_entity
from sensor import utils
from sensor.config import TARGET_COLUMN

from sklearn.metrics import f1_score
from xgboost import XGBClassifier

class ModelTrainer:


    def __init__(self,
                model_trainer_config: config_entity.ModelTrainerConfig,
                data_transformation_artifact: artifact_entity.DataTransformationArtifact):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config= model_trainer_config
            self.data_transformation_artifact= data_transformation_artifact
        except Exception as e:
            print(f'\nError: {e}')
            raise SensorException(e, sys)

    # property
    def train_model(self, x, y):
        try:
            logging.info(f"Training the XG Boost Classifier.")
            xgb_clf= XGBClassifier()
            xgb_clf.fit(x, y)
            
            return xgb_clf

        except Exception as e:
            print(f'\nError: {e}')
            raise SensorException(e, sys)



    def initiate_model_trainer(self)-> artifact_entity.ModelTrainerArtifact:
        """ Initiating the model trainer."""
        try:
            logging.info(f"Model trainer initiated.")
            
            #1 Load train and test data from the arrays.
            train_arr= utils.load_numpy_array_data(file_path= self.data_transformation_artifact.transformed_train_path)
            test_arr= utils.load_numpy_array_data(file_path= self.data_transformation_artifact.transformed_test_path)

            logging.info(f"Loaded training and testing arrays.")
            #2 x_train, y_train, x_test, y_test
            x_train, y_train= train_arr[:,:-1], train_arr[:, -1]
            x_test, y_test= test_arr[:,:-1], test_arr[:, -1]
            logging.info(f"Acquired x_train, x_test, y_train, y_test.")
            #3 Train model.

            model= self.train_model(x= x_train, y=y_train)

            logging.info(f"Trained the model")
            #4 Compute f1 score for train and test sets.
            y_pred_train= model.predict(x= x_train, y= y_train)
            y_pred_test= model.predict(x= x_test, y= y_test)
            logging.info(f"Predictions made and saved.")

            f1_train_score= f1_score(y_true= y_train, y_pred= y_pred_train)
            f1_test_score= f1_score(y_true= y_test, y_pred= y_pred_test)
            logging.info(f"F1 score for train set: {f1_train_score} \nF1 score for test set: {f1_test_score}")

            #5 Check if the model score is equal to requirements.
            if f1_test_score< self.model_trainer_config.expected_score:
                logging.info(f"Model accuracy was {f1_test_score} which does not meet the required accuracy which is {self.model_trainer_config.expected_score}.")
                raise Exception(f"Model accuracy was {f1_test_score} which does not meet the required accuracy which is {self.model_trainer_config.expected_score}.")

            #6 Check if the model is  overfitting.

            diff= abs(f1_train_score- f1_test_score)
            if diff > self.model_trainer_config.overfitting_threshold:
                logging.info(f"Model is overfitting. \nObtained test accuracy: {f1_test_score}")
                raise Exception(f"Model is overfitting. \nObtained test accuracy: {f1_test_score}")

            
            #7 Serialize the model.
            utils.serialize(file_path= self.model_trainer_config.model_path, obj= model)

            #8 Prepare Artifact.
            
            
            model_trainer_artifact= artifact_entity.ModelTrainerArtifact(model_path= self.model_trainer_config.model_path,
                                                                        f1_train_score= f1_train_score, 
                                                                         f1_test_score= f1_test_score)
            return model_trainer_artifact

        except Exception as e:
            print(f'\nError: {e}')
            raise SensorException(e, sys)