import pymongo
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()
client_atlas= pymongo.MongoClient(os.getenv('MONGO_DB_ATLAS_URL'))
client_local= pymongo.MongoClient(os.getenv('MONGO_DB_LOCAL_HOST_URL'))
 
DATAPATH= "aps_failure_training_set1.csv"
DATABASE_NAME= 'aps'
COLLECTION_NAME= 'sensor'

if __name__== '__main__':
    #client.
    df= pd.read_csv('aps_failure_training_set1.csv')
    print(f'Data {df.shape}')

# Converting a dataframe to json format for inserting into mongodb.
    df.reset_index(inplace= True, drop = True)

    # json.loads converts any python object to json object.
    json_records= list(json.loads(df.T.to_json()).values())
    
    # Bulk insert data to mongo db
    client_atlas[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)
    client_local[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)