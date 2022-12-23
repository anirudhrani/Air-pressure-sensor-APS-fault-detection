import sys
import numpy as np
import pandas as pd
import os
from dataclasses import dataclass
from sensor import utils
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.entity import artifact_entity
from sensor.entity import config_entity
from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self, data_ingestion_config: config_entity.DataIngestionConfig) -> None:
        try:
            self.data_ingestion_config= data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)

    
    def initiate_data_ingestion_config(self)->artifact_entity.DataIngestionArtifact:

        """ This functiion:
            1. Imports data from db as a data frame.
            2. Replaces null values with numpy nan values.
            3. Creates a feature store folder.
            4. Save data frame as a csv file.
            5. Perform train-test split."""


        try:
        # 1. Importing data from db as a data frame.
            logging.info('Fetching data from db and converting it to a dataframe.')
            # Get the data. Convert it to a data frame from csv using functions in utils
            # get_collection_as_dataframe takes db name and collection name.
            df= utils.get_collection_as_dataframe(database_name= self.data_ingestion_config.database_name , 
                                                 collection_name= self.data_ingestion_config.collection_name)
        # 2. Replacing null values with numpy NaN's.
            logging.info("Replacing null values with numpy NaN's. ")
            df.replace(to_replace= "na", value= np.NAN, inplace= True)
        
        # 3. Creating a feature store.
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_dir)
            os.makedirs(feature_store_dir, exist_ok=True)
            logging.info("Created feature store folder.")
        
        # 4. Saving the data frame to a csv file.
            df.to_csv(path_or_buf= self.data_ingestion_config.feature_store_dir, index=False, header= True)
            logging.info(f'Csv file created at location{self.data_ingestion_config.feature_store_dir}')

        # 5. Train test split.
            train_df, test_df= train_test_split(df, test_size= self.data_ingestion_config.test_size , random_state=42)
            logging.info('Finished train test split.')

            # Creating the directory if it doesnot exist.
            dataset_dir= os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok= True)
        
        # 6. Save df to feature store.
            train_df.to_csv(path_or_buf= self.data_ingestion_config.train_file_path, random_state=42)
            test_df.to_csv(path_or_buf= self.data_ingestion_config.test_file_path, random_state=42)
            logging.info('Train and test csv files generated in feature store.')


            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path= self.data_ingestion_config.feature_store_dir,
                train_file_path= self.data_ingestion_config.train_file_path, 
                test_file_path= self.data_ingestion_config.test_file_path)
            logging.info(f'Data ingestion artifact. {data_ingestion_artifact}')

            return data_ingestion_artifact
            
        except Exception as e:
            raise SensorException(e, sys)