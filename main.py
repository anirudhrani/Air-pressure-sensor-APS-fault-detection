import sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity import config_entity, artifact_entity
from sensor.components import Data_Ingestion, Data_validation, Data_Transformation, Model_trainer

if __name__== '__main__':
    try:
    # Testing Data Ingestion.
        print('\nInitiating Data Ingestion.\n')
        training_pipeline_config= config_entity.TrainingPipelineConfig()
        data_ingestion_config= config_entity.DataIngestionConfig(training_pipeline_config= training_pipeline_config)

        # print(data_ingestion_config.to_dict())

        data_ingestion= Data_Ingestion.DataIngestion(data_ingestion_config= data_ingestion_config)
        # print(data_ingestion.initiate_data_ingestion())

        data_ingestion_artifact= data_ingestion.initiate_data_ingestion()
        print('Data Ingestion completed.')


    # Testing Data Validation
        print('\nInitiating Data Validation.\n')
        data_validation_config= config_entity.DataValidationConfig(training_pipeline_config= training_pipeline_config)
        data_validation= Data_validation.DataValidation(data_validation_config=data_validation_config, data_ingestion_artifact= data_ingestion_artifact)
        data_validation_artifact=  data_validation.initiate_data_validation()
        print('\nData Validation Completed.\n')
        # print(data_validation_artifact)

    # Testing Data Transformation.
        print('\nInitiating Data Transformation.\n')
        data_transformation_config= config_entity.DataTransformationConfig(training_pipeline_config= training_pipeline_config)
        data_transformation= Data_Transformation.DataTransformation(data_transformation_config=data_transformation_config, data_ingestion_artifact= data_ingestion_artifact)
        data_transformation_artifact=  data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
    # Testing Model Trainer.

    except Exception as e:
        print('Error: ',e)
        SensorException(e, sys)