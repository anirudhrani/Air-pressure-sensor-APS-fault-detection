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
            self.data_validation_config = data_validation_config
            self.validation_error= dict()
        except Exception as e:
            raise SensorException(e, sys)
    
    def required_columns_check(self, base_df: pd.DataFrame
                                   , present_df: pd.DataFrame)-> bool:
        """Checks if enough data is required for going into the next phase of poduction."""
        try:
            missing_columns= []
            base_columns =  base_df.columns
            current_columns= present_df.columns

            for base_column in base_columns:
                if base_column not in current_columns:
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error['missing_columns']= missing_columns
                return False
            return True

        except Exception as e:
            SensorException(e, sys)


    def drop_columns_with_missing_vals(self, df: pd.DataFrame):
        
        """Drops columns where 30% of the data is missing.
        df: Dataframe
        threshold: Threshold for the missing data above which the column will be dropped.
        
        ================================================================================
        
        Returns a Data Frame."""
        try:
            # Threshold.
            threshold= self.data_validation_config.missing_threshold
            null_repot= df.isnull().sum()/df.shape[0]

            # Find the columns which have null value percentage greater than threshold.
            dropped_column_names= null_repot[null_repot> threshold].index

            # Save the names of the columns which will be dropped.
            self.validation_error['dropped_columns']= dropped_column_names
            logging.info(f'Dropping columns {dropped_column_names}')
            
            # Drop the columns.
            df.drop(columns= list(dropped_column_names), inplace= True)
            
            
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