import sys
import os
import pandas as pd
import numpy as np 
from scipy.stats import ks_2samp
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity import artifact_entity, config_entity



class DataValidation:
    def __init__(self, data_validation_config: config_entity.DataValidationConfig) -> None:
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.initiate_data_validation= data_validation_config
        except Exception as e:
            raise SensorException(e, sys)
    
    def required_columns_check(self, df)-> bool:
        """Checks if enough data is required for going into the next phase of poduction."""
        try:
            pass
        except Exception as e:
            SensorException(e, sys)


    def drop_columns_with_missing_vals(self, df: pd.DataFrame, threshold:float= 0.30):
        
        """Drops columns where 30% of the data is missing.
        df: Dataframe
        threshold: Threshold for the missing data above which the column will be dropped.
        
        ================================================================================
        
        Returns a Data Frame."""
        try:
            null_repot= df.isnull().sum()/df.shape[0]

            # Find the columns which have null value percentage greater than threshold.
            drop_column_names= null_repot[null_repot> threshold].index
            logging.info(f'Dropping columns {drop_column_names}')
            df.drop(columns= list(drop_column_names), inplace= True)
            
            if len(df.columns)==0:
                logging.info(f'Length of columns is 0.')
                return None
            
            return df
        except Exception as e:
            SensorException(e, sys)

    def initiate_data_validation(self)-> artifact_entity.DataValidationArtifact:
        try:
            pass
        except Exception as e:
            SensorException(e, sys)