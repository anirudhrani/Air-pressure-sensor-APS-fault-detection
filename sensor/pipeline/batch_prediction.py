import os
import sys
import pandas as pd
from sensor.exception import SensorException
from sensor.predictor import ModelLocator
from sensor.logger import logging
from sensor.utils import serialize
from datetime import datetime


PREDICTION_DIR= "prediction"
PREDICTION_FILE_NAME= f"{datetime.now().strftime('%m%d%Y__%H%M%S')}"

def batch_prediction(input_file_path:str):
    try:
        model_locator= ModelLocator(model_registry="saved_models")
        df= pd.read_csv(input_file_path)
        transformer= serialize(file_path= model_locator.get_latest_transformer_path())
        
        input_feature_name= transformer.f

        prediction_file_name= os.path.base(input_file_path).replace(".csv", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
    except Exception as e:
        raise SensorException(e, sys)