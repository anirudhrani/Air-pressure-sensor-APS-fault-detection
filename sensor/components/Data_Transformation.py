import os
import sys
import pandas as pd
import numpy as np
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.entity import config_entity, artifact_entity
from sensor import utils

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from imblearn.combine import SMOTETomek


class DataTransformation:

    def __init__(self,
                data_transformation_config: config_entity.DataTransformationConfig,
                data_ingestion_artifact: artifact_entity.DataIngestionArtifact) -> None:
        try:
            self.data_transformation_config= data_transformation_config
            self.data_ingestion_artifact= data_ingestion_artifact


        except Exception as e:
            print(f'Error : {e}')
            raise SensorException(e, sys)

    @classmethod
    def get_transformer_object(cls)->Pipeline:

        try:

            simple_imputer= SimpleImputer(strategy= "constant", fill_value= 0)
            robust_scaler= RobustScaler()
            pipeline= Pipeline(steps= [('Imputer', simple_imputer), ('RobustScaler', robust_scaler)])
            
            return pipeline
        except Exception as e:
            print(f'Error: {e}')
            raise SensorException(e, sys)