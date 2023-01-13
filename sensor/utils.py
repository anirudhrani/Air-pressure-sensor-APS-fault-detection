import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongo_client
import sys
import os
import yaml

def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:

    try:
        logging.info(f'Fetching data from {database_name} pertaining to {collection_name}')
        df= pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f'Data frame generated with columns: {df.columns}')

        # Remove 'ID' column from the dataframe.
        logging.info('Checking for the "_id" column in the data frame')
        if '_id' in df.columns:
            logging.info('"_id" column found. Hence removing it.')
            df.drop(columns= '_id')
        return df
    except Exception as e:
        SensorException(e, sys)

def write_yaml_file(file_path, data:dict):
    try:
        file_dir= os.path.dirname(file_path)

        os.makedirs(file_dir, exist_ok= True)

        with open (file_dir, "w") as file_writer:
            yaml.dump(data, file_writer)


    except Exception as e:
        SensorException(e, sys)