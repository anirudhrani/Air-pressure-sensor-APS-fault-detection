import os
from datetime import datetime
import sys
from sensor.exception import SensorException
from sensor.logger import logging

# Constants. (Includes file name conventions and fixed values.)
FILE_NAME= "sensor.csv"
TRAIN_FILE_NAME= 'train.csv'
TEST_FILE_NAME= 'test.csv'
TRANSFORMER_OBJECT_FILE_NAME= "transformer.pkl"
TARGET_ENCODER_OBJECT= "target_encoder.pkl"
MODEL_FILE_NAME= 'model.pkl'
EXPECTED_SCORE= 0.7
MODEL_OVERFITTING_THRESHOLD= 0.1
TARGET_COLUMN_NAME= 'class'

class TrainingPipelineConfig:
    """Create a new directory named artifact under which a timestamp folder will be created."""
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
    """This funtion initiates various config requirements such as directory path for data validation, report file path, missing value threshold, base data path
       as a part of data validation."""
    def __init__(self, training_pipeline_config: TrainingPipelineConfig) :
        #1 Creating data_ingestion directory inside the timestamp folder inside the artifact directory.
        self.data_validation_dir= os.path.join(training_pipeline_config.artifact_dir, "data_validation")

        #2 Creating Report file path in artifact folder.
        self.report_file_path= os.path.join(self.data_validation_dir,"report.yaml")

        self.missing_threshold:float= 0.2

        self.base_data_path= os.path.join("aps_failure_training_set1.csv")


# Data Transformation.
class DataTransformationConfig:
    """This funtion initiates various config requirements such as db name, file paths, split size for
       data transformation."""
    def __init__(self, training_pipeline_config: TrainingPipelineConfig) -> None:

        #1 Create a folder for data transformation in the artifact directory.
        self.data_transformation_dir= os.path.join(training_pipeline_config.artifact_dir, "data_transformation")
        #2 Create a transform pickle file.
        self.transform_object_path= os.path.join(self.data_transformation_dir,"transformer", TRANSFORMER_OBJECT_FILE_NAME)
        #3 Create the transformed training file name.
        self.transformed_train_path= os.path.join(self.data_transformation_dir, "transformed", TRAIN_FILE_NAME.replace('csv', 'npz'))
        #4 Create the transformed testing file name.
        self.transformed_test_path= os.path.join(self.data_transformation_dir, "transformed", TEST_FILE_NAME.replace('csv', 'npz'))
        #5
        self.target_encoder= os.path.join(self.data_transformation_dir,"target_encoder", TARGET_ENCODER_OBJECT )

class ModelTrainerConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig) -> None:
        """This funtion initiates various config requirements such as db name, file paths, split size for
       data transformation."""
        self.model_trainer_dir= os.path.join(training_pipeline_config.artifact_dir, "model_trainer")
        self.model_path= os.path.join(self.model_trainer_dir, "model", MODEL_FILE_NAME)
        self.expected_score= EXPECTED_SCORE
        self.overfitting_threshold= MODEL_OVERFITTING_THRESHOLD

class ModelEvaluationConfig:
    def __init__(self, training_pipeline_config: TrainingPipelineConfig)-> None:
        self.model_evaluation_dir= os.path.join(training_pipeline_config.artifact_dir, "model_evaluation")
class ModelPusherConfig:...