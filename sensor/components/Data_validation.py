import sys
import os
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity import artifact_entity, config_entity
from sensor import utils



class DataValidation:
    def __init__(self, data_validation_config: config_entity.DataValidationConfig,
                       data_ingestion_artifact: artifact_entity.DataIngestionArtifact) -> None:
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact= data_ingestion_artifact

            # Initializing a dictionary for the validation report.
            self.validation_error= dict()
        except Exception as e:
            print('\nError:', e)
            raise SensorException(e, sys)

    def required_columns_check(self, base_df: pd.DataFrame,
                                     present_df: pd.DataFrame,
                                     report_key_name: str)-> bool:

        """Checks if enough data is required for going into the next phase of production."""
        try:
            missing_columns= []
            base_columns =  base_df.columns
            current_columns= present_df.columns

            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f'Column:{base_column} not found.')
                    missing_columns.append(base_column)

            if len(missing_columns)>0:
                self.validation_error[report_key_name]= missing_columns
                return False
            return True

        except Exception as e:
            print('\nError:', e)
            SensorException(e, sys)


    def data_drift(self,base_df:pd.DataFrame, present_df:pd.DataFrame, report_key_name: str):
        """Computes the data drift between the base data and the pre-processed data. Returns a boolean value."""
        try:
            drift_report= dict()
            # Extract column names.
            base_columns =  base_df.columns
            current_columns= present_df.columns

            for base_column in base_columns:
                base_data, present_data= base_df[base_column], present_df[base_column]
                logging.info(f"Hypothesis {base_column}: {base_data.dtype}")
                same_distribution= ks_2samp(base_data, present_data)

                if same_distribution.pvalue>0.05: # Null Hypothesis is accepted
                    logging.info(f"Null hypotheis is true i.e. data drift not detected.")
                    drift_report[base_column]= { "pvalue": same_distribution.pvalue,
                                                 "Data Drift Detected": False}
                else: # Alternate Hypothesis is accepted.
                    logging.info(f"Alternate hypothesis is true as p value {same_distribution.pvalue} is less than 0.05.")
                    drift_report[base_column]= { "pvalue": same_distribution.pvalue,
                                                 "Data Drift Detected": True}


            self.validation_error[report_key_name]= drift_report
        except Exception as e:
            print('\nError:', e)
            SensorException(e, sys)


    def drop_columns_with_missing_vals(self, df: pd.DataFrame, report_key_name: str):

        """Drops columns where 30% of the data is missing.
        df: Dataframe
        threshold: Threshold for the missing data above which the column will be dropped.

        ================================================================================

        Returns a Data Frame."""
        try:
            # Threshold.
            threshold= self.data_validation_config.missing_threshold
            null_report= df.isnull().sum()/df.shape[0]
            logging.info(f'Null report value:{null_report}')
            # Find the columns which have null value percentage greater than threshold.
            dropped_column_names= null_report[null_report> threshold].index

            # Save the names of the columns which will be dropped.
            self.validation_error[report_key_name]= dropped_column_names
            logging.info(f'Dropping columns {dropped_column_names}')

            # Drop the columns.
            df.drop(columns= list(dropped_column_names), inplace= True)


            if len(df.columns)==0:
                logging.info(f'Length of columns is 0.')
                return None

            return df
        except Exception as e:
            print('\nError:', e)
            SensorException(e, sys)

    def initiate_data_validation(self)-> artifact_entity.DataValidationArtifact:
        try:

            logging.info(f'Data Validation Initiated.')
            #1 Read Base data frame.
            base_df= pd.read_csv(self.data_validation_config.base_data_path)

            #2 Replace na with NAN Values.
            base_df.replace({"na": np.NAN}, inplace= True)

            #3 Drop Missing values.
            logging.info(f'Dropped columns with missing values from base data frame.')
            base_df= self.drop_columns_with_missing_vals(df= base_df, report_key_name= "base_dataset")

            #4 Read train and test files.
            train_df= pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df= pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #4 Drop the missing values from both train and test files
            train_df= self.drop_columns_with_missing_vals(df= train_df, report_key_name="missing_data_in_train_dataset")
            test_df= self.drop_columns_with_missing_vals(df= test_df, report_key_name="missing_data_in_test_dataset")

            #4.5 Convert dtype
            
            exclude_columns = ["class"]
            base_df = utils.dtype_converter(df=base_df, exclude_features=exclude_columns)
            train_df = utils.dtype_converter(df=train_df, exclude_features=exclude_columns)
            test_df = utils.dtype_converter(df=test_df, exclude_features=exclude_columns)
            logging.info(f"CONVERTED DATA TYPE OF COLUMNS.")
            #5 Check for REQUIRED COLUMNS.
            train_df_column_status= self.required_columns_check(base_df= base_df,
                                                                present_df= train_df,
                                                                report_key_name="missing_columns_in_train_dataset")
            logging.info(f'Dropped columns with missing values from training data.')
            test_df_column_status= self.required_columns_check(base_df= base_df,
                                                               present_df= test_df,
                                                               report_key_name="missing_columns_in_train_dataset")
            logging.info(f'Dropped columns with missing values from testing data.')

            #6 If required columns are found then check for DATA DRIFT.

            if train_df_column_status:
                self.data_drift(base_df= base_df,
                                present_df= train_df,
                                report_key_name="data_drift_in_train_dataset")
            if test_df_column_status:
                self.data_drift(base_df= base_df,
                                present_df= test_df,
                                report_key_name="data_drift_in_test_dataset")
            logging.info(f"Preparing Data Validation Artifact.")
            
            #7 Write to validation report.
            utils.write_yaml_file(file_path= self.data_validation_config.report_file_path, data= self.validation_error)
            logging.info(f'Report.yaml generated.')

            #8 Prepare the data validation artifact.

            data_validaton_artifact= artifact_entity.DataValidationArtifact(report_file_path= self.data_validation_config.report_file_path)
            return self.validation_error, data_validaton_artifact
        except Exception as e:
            print('\n Error: ',e)
            SensorException(e, sys)