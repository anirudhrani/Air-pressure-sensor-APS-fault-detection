import sys
import os
import yaml
import dill
import pandas as pd
import numpy as np
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
            df.drop(columns= ['_id'], inplace= True)
        return df
    except Exception as e:
        print('\nError:', e)
        raise SensorException(e, sys)

def write_yaml_file(file_path, data:dict):
    """Writes data (in dictionary format) to a YAML file."""
    try:
        #1 Just in case if the data_validation folder is not created in artifact directory then this creates one.
        file_dir= os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok= True)
        
        #file_dir ->  D:\aps_fault_detection_main\artifact\01172023__231419\data_validation
        #file_path -> D:\aps_fault_detection_main\artifact\01172023__231419\data_validation\report.yaml

        #2 Dump the data in to the yaml file.
        with open (file_path, "w") as file_writer:
            yaml.dump(data, file_writer)


    except Exception as e:
        print(f'\nError: {e}')
        raise SensorException(e, sys)

def serialize(file_path:str, obj: object)->None:
    """Saves object to a file."""
    try:
        logging.info(f'Entered the searialize method of the main utils class.')
        # make a directory if it doesn't exist.
        os.makedirs(os.path.dirname(file_path), exist_ok= True)

        with open (file_path, "wb") as file_obj:
            return dill.dump(obj, file_obj)
        logging.info(f'Exited the searialize method of the main utils class.')

    except Exception as e:
        print(f'\nError: {e}')
        raise SensorException(e, sys)


def deserialize(file_path:str)->None:
    """Loads object from a file."""
    try:
        logging.info(f'Entered the searialize method of the main utils class.')
        # make a directory if it doesn't exist.
        if not os.path.exists(file_path):
            raise Exception(f"The file at location {file_path} does'nt exist.")

        with open (file_path, "rb") as file_obj:
            return dill.load(file_obj)
        logging.info(f'Exited the searialize method of the main utils class.')

    except Exception as e:
        print(f'\nError: {e}')
        raise SensorException(e, sys)


def save_numpy_array_data(file_path: str, np_array: np.array):
    """SAVES AN ARRAY TO A (.npy) NUMPY BINARY FILE. """
    try:
        dir_path= os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok= True)
        with open(file_path, "wb") as file_obj:
            # np.save -> SAVES AN ARRAY TO A NUMPY BINARY FILE (.npy).
            np.save(file_obj, np_array)
    except Exception as e:
        print(f'\nError: {e}')
        raise SensorException(e, sys)\

def load_numpy_array_data(file_path: str)-> np.array:
    """LOADS A (.npy) NUMPY BINARY FILE. """
    try:

        with open(file_path, "rb") as file_obj:
            # np.save -> SAVES AN ARRAY TO A NUMPY BINARY FILE (.npy).
            return np.load(file_obj)

    except Exception as e:
        print(f'\nError: {e}')
        raise SensorException(e, sys)\

def dtype_converter(df: pd.DataFrame, except_columns: list)-> pd.DataFrame:
    """Converts the data type of a column to float."""
    try:
        for column_name in df.columns:
            if column_name not in except_columns:
                # df[column_name] = df[column_name].astype('float')
                df[column_name]= pd.to_numeric(df[column_name], downcast="float", errors='coerce')
        return df

    except Exception as e:
        print(f"\nError: {e}")
        raise SensorException(e, sys)