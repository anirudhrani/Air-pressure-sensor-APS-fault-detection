import pandas as pd
import pymongo 
from dataclasses import dataclass
import os

@dataclass
class EnvironmentVariable:
    # os.getenv -> Used to access the contents in .env file.
    mongodb_url:str= os.getenv("MONGO_DB_URL")

    #
    aws_access_key= os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key= os.getenv("AWS_SECRET_KEY")

env_var= EnvironmentVariable()
mongo_client= pymongo.MongoClient(env_var.mongodb_url)
TARGET_COLUMN= "class"
TARGET_COLUMN_MAPPING= {"pos":1,
                         "neg":0}
