import os
from datetime import datetime
import sys
from sensor.exception import SensorException
from sensor.logger import logging


FILE_NAME= "sensor.csv"
TRAIN_FILE_NAME= 'train.csv'
TEST_FILE_NAME= 'test.csv'

class TrainingPipelineConfig:

    def __init__(self):
        # Create a new directory named artifact under which a timestamp folder will be created.
        try:
            self.artifact_dir= os.path.join(os.getcwd(), "artifact", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise SensorException(e, sys)
            
class DataIngestionConfig:

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """This funtion initiates various config requirements such as db name, file paths, split size for
           data ingestion"""
        try:
            self.database_name= "aps"
            self.collection_name= "sensor"

            # Creating data_ingestion directory inside the timestamp folder inside the artifact directory.
            self.data_ingestion_dir= os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
            
            # Initializing feature store, train and test folder paths.
            self.feature_store_dir= os.path.join(self.data_ingestion_dir, "feature_store", FILE_NAME)
            self.train_file_path= os.path.join(self.data_ingestion_dir, "dataset", TRAIN_FILE_NAME)
            self.test_file_path= os.path.join(self.data_ingestion_dir, "dataset", TEST_FILE_NAME)

            # Test split size.
            self.test_size= 0.2
        except Exception as e:
            raise SensorException (e, sys)


    def to_dict(self)->dict:
        """This function returns data in the form of a dictionary."""
        try:
            return self.__dict__
        except Exception  as e:
            raise SensorException(e,sys)

# Data Validation.
class DataValidationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig) :
        # Creating data_ingestion directory inside the timestamp folder inside the artifact directory.
        self.data_validation_dir= os.path.join(training_pipeline_config.artifact_dir, "data_validation")

        # Creating Report file path in artifact folder.
        self.report_file_path= os.path.join(self.data_validation_dir,"report.yaml")

        self.missing_threshold:float= 0.2

        self.base_data_path= os.path.join("aps_failure_training_set1.csv")


class DataTransformationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig) -> None:
        self.data_transformation_dir= os.path.join(training_pipeline_config.artifact_dir, "data_transformation")
        
class ModelTrainerConfig:...
class ModelEvaluationConfig:...
class ModelPusherConfig:...