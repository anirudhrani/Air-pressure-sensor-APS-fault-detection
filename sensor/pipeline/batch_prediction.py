import os
import sys
import numpy as np
import pandas as pd
from sensor.exception import SensorException
from sensor.predictor import ModelLocator
from sensor.logger import logging
from sensor.pipeline import training_pipeline
from sensor.utils import serialize
from datetime import datetime


PREDICTION_DIR= "prediction"
PREDICTION_FILE_NAME= f"{datetime.now().strftime('%m%d%Y__%H%M%S')}"

def start_batch_prediction(input_file_path:str):
    try:
        #1 Create prediction directory.
        logging.info(f"Create prediction directory.")
        os.makedirs(PREDICTION_DIR, exist_ok= True)

        logging.info(f"Initiate model locator so that we will able to track down model, transformer and encoder binaries.")
        model_locator= ModelLocator(model_registry="saved_models")
        #1.5 Load and replace "na" with np.NAN
        df= pd.read_csv(input_file_path)
        df.replace(to_replace= "na", value= np.NAN, inplace= True)

        #2 Read the latest transformer file.
        transformer= serialize(file_path= model_locator.get_latest_transformer_path())
        logging.info(f"Loaded Transformer.")

        #3 Create the input array for the model and transformer. 
        input_feature_name= list(transformer.feature_names_in_)
        input_arr= df[input_feature_name]
        logging.info(f"Input array created.")

        #4 Serialize the model and make predcitions on the input array.
        model= serialize(file_path= model_locator.get_latest_model_path())
        y_pred= model.predict(input_arr)
        logging.info(f"Model loaded and prediction made.")

        #5 Serialize the target encoder and inverse transform the obtained prediction.
        target_encoder= serialize(file_path= model_locator.get_latest_target_encoder_path())
        final_predicted_value= target_encoder.inverse_transform(y_pred)
        logging.info(f"Performed inverse transformation on the predicted output.")

        #6 Save the numerical and categorical predictions to the existing dataframe.
        df['Numerical_predictions']= y_pred
        df['Categorical_predictions']= final_predicted_value
        logging.info(f"Created prediction columns to the existing model.")

        #7 Create proper file name and folder to save the data frame.
        prediction_file_name= os.path.basename(input_file_path).replace(".csv", f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path= os.path.join(PREDICTION_DIR, prediction_file_name)
        logging.info(f"Created prediction file path at: {prediction_file_path}")

        #8 Save the data frame in the designated path.
        df.to_csv(prediction_file_path, header= True, index= False)

        return prediction_file_path
    except Exception as e:
        raise SensorException(e, sys)