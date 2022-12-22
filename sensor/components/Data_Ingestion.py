import sys
import numpy as np
import pandas as pd

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
            3. Creates a feature store folder."""


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
        
        # 3.

        
        except Exception as e:
            raise SensorException(e, sys)