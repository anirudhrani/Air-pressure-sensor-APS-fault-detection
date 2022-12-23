import pandas as pd
from logger import logging
from exception import SensorException
from config import mongo_client
import sys

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