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

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, LabelEncoder
from imblearn.combine import SMOTETomek


class DataTransformation:

    def __init__(self,
                data_transformation_config: config_entity.DataTransformationConfig,
                data_ingestion_artifact: artifact_entity.DataIngestionArtifact) -> None:
        try:
            logging.info(f"{'>>>'*20} Data Transformation.{'<<<'*20}")
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact= data_ingestion_artifact


        except Exception as e:
            print(f'\nError : {e}')
            raise SensorException(e, sys)



    @classmethod
    def get_transformer_object(cls)->Pipeline:

        try:
            logging.info(f"Entered get_transformer_object.")
            simple_imputer= SimpleImputer(strategy= "constant", fill_value= 0)
            robust_scaler= RobustScaler()
            pipeline= Pipeline(steps= [('Imputer', simple_imputer), ('RobustScaler', robust_scaler)])
            logging.info(f'Pipeline created.')
            return pipeline

        except Exception as e:
            print(f'\nError: {e}')
            raise SensorException(e, sys)



    def initiate_data_transformation(self)-> artifact_entity.DataTransformationArtifact:
        try:
            logging.info(f"Entered initiate date transformation class.")
        #1 Read train data and test data.
            
            train_df= pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df= pd.read_csv(self.data_ingestion_artifact.test_file_path)

        #2 Declare Target Column.
            
            target_feature_train_df= train_df[TARGET_COLUMN]
            target_feature_test_df= test_df[TARGET_COLUMN]
            logging.info(f"Declared target columns in train and test data.")


        #3 Input feature for train and test data
            input_feature_train_df= train_df.drop(TARGET_COLUMN, axis=1)
            input_feature_test_df= test_df.drop(TARGET_COLUMN, axis=1)
            logging.info(f"Prepared input for train and test sets.")

        #4 LABEL ENCODING on the target variable.
            label_encoder= LabelEncoder()
                # Fit
            label_encoder.fit(target_feature_train_df)
            logging.info(f"Fitting the label encoder.")

                # Tranform.
            target_feature_train_array= label_encoder.transform(target_feature_train_df)
            target_feature_test_array= label_encoder.transform(target_feature_test_df)
            logging.info(f"Label encoded the target features in both train and test sets.")

        #5  Prepare input feature data. [x_train and x_test]
            logging.info(f"Sending input data into the data transformation pipeline.")
            transformation_pipeline= DataTransformation.get_transformer_object()
            
            transformation_pipeline.fit(input_feature_train_df)

            input_feature_train_array= transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_array= transformation_pipeline.transform(input_feature_test_df)

        #6 Dealing with imbalanced data.
            logging.info(f"Performing SMOTE to deal with the imbalanced data.")
            smt= SMOTETomek(sampling_strategy= 'minority')
            logging.info(f'Before resampling, training set input shape:{input_feature_train_array.shape} Target shape: {target_feature_train_array.shape}')
            input_feature_train_array, target_feature_train_array= smt.fit_resample(input_feature_train_array,
                                                                                     target_feature_train_array)
            logging.info(f'After resampling, training set input shape:{input_feature_train_array.shape} Target shape: {target_feature_train_array.shape}')

            logging.info(f'Before resampling, testing set input shape:{input_feature_test_array.shape} Target shape: {target_feature_test_array.shape}')
            input_feature_test_array, target_feature_test_array= smt.fit_resample(input_feature_test_array,
                                                                                  target_feature_test_array)
            logging.info(f'After resampling, testing set input shape:{input_feature_test_array.shape} Target shape: {target_feature_test_array.shape}')

        #7 Concatenate train and test array data.
            train_arr= np.c_[input_feature_train_array, target_feature_train_array]
            test_arr= np.c_[input_feature_test_array, target_feature_test_array]

        #8 Save train and test numpy array  in train and test paths.
            utils.save_numpy_array_data(file_path= self.data_transformation_config.transformed_train_path, np_array= train_arr)
            utils.save_numpy_array_data(file_path= self.data_transformation_config.transformed_test_path, np_array= test_arr)

        #9 Serializing the transformation_pipeline.
            utils.serialize(file_path= self.data_transformation_config.transform_object_path, obj= transformation_pipeline)

        #10 Serializing the label encoder object.
            utils.serialize(file_path= self.data_transformation_config.target_encoder, obj= label_encoder)

        #11 Data Transformation artifact
            data_transformation_artifact= artifact_entity.DataTransformationArtifact(transform_object_path= self.data_transformation_config.transform_object_path,
                                                                                     transformed_train_path= self.data_transformation_config.transformed_train_path,
                                                                                     transformed_test_path= self.data_transformation_config.transformed_test_path,
                                                                                     target_encoder_path= self.data_transformation_config.target_encoder)
            logging.info(f'Data transformation artifact: {data_transformation_artifact}')
            return data_transformation_artifact


        except Exception as e:
            logging.info(f'Error: {e}')
            print(f'\nError : {e}')
            raise SensorException(e, sys)