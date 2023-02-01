import sys
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity import config_entity, artifact_entity
from sensor.components import Data_Ingestion, Data_validation, Data_Transformation, Model_trainer, Model_pusher, Model_evaluation

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
        print('\nData Ingestion completed.\n')


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
        #print(data_transformation_artifact)
        print('\nData Transformation Completed.\n')
    # Testing Model Trainer.
        print('\nInitiating Model Training.\n')
        model_trainer_config= config_entity.ModelTrainerConfig(training_pipeline_config= training_pipeline_config)
        model_trainer= Model_trainer.ModelTrainer(model_trainer_config= model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact= model_trainer.initiate_model_trainer()
        print(model_trainer_artifact)
        print('\nModel Training Completed.\n')
    
    # Evaluating the model
        print('\nInitiating Model Evaluation.\n')
        model_evaluation_config= config_entity.ModelEvaluationConfig(training_pipeline_config= training_pipeline_config)
        model_eval= Model_evaluation.ModelEvaluation(model_evaluation_config= model_evaluation_config,
                                                    data_ingestion_artifact= data_ingestion_artifact,
                                                    data_transformation_artifact= data_transformation_artifact,
                                                    model_trainer_artifact= model_trainer_artifact)
        model_eval_artifact= model_eval.initiate_model_evaluation()
        print(model_eval_artifact)
        print('\nModel Evaluation Completed.\n')
    # Model Pushing.
        print('\nInitiating Model Pusher.\n')
        model_pusher_config= config_entity.ModelPusherConfig(training_pipeline_config= training_pipeline_config)
        model_pusher= Model_pusher.ModelPusher(model_pusher_config= model_pusher_config,
                                               data_transformation_artifact= data_transformation_artifact,
                                               model_evaluation_artifact= model_eval_artifact,
                                               model_trainer_artifact= model_trainer_artifact)
        model_pusher_artifact= model_pusher.initiate_model_pusher()
        print(model_pusher_artifact)
        print('\nModel Pushing Completed.\n')


    except Exception as e:
        print('Error: ',e)
        SensorException(e, sys)