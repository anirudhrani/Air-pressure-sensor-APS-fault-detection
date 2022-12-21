import pandas as pd
import pymongo 
import json
from dataclasses import dataclass
import os

@dataclass
class EnvironmentVariable:
    # os.getenv -> Used to access the contents in .env file.
    mongodb_url:str= os.getenv("MONGO_DB_URL")

env_var= EnvironmentVariable()
mongo_client= pymongo.MongoClient(env_var.mongodb_url)
