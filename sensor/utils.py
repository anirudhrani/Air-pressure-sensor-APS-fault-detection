import sys
import os
import yaml
import dill
import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorException
from sensor.config import mongo_client


def get_collection_as_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    """Gets the data from a MongoDb collection as a pandas DataFrame."""

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
        print('\nError:', e)
        raise SensorException(e, sys)

def write_yaml_file(file_path, data:dict):
    """Writes data (in dictionary format) to a YAML file."""
    try:
        file_dir= os.path.dirname(file_path)

        os.makedirs(file_dir, exist_ok= True)

        with open (file_dir, "w") as file_writer:
            yaml.dump(data, file_writer)


    except Exception as e:
        print(f'\nError: {e}')
        raise SensorException(e, sys)

def serialize(file_path:str, obj: object)->None:
    """Saves object to a file."""
    try:
        pass


    except Exception as e:
        print(f'\nError: {e}')
        SensorException(e, sys)
