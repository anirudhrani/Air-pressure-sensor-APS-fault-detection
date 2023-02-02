import pymongo
import pandas as pd
import json
import os

URL= "mongodb+srv://test:test@cluster0.w4eegio.mongodb.net/?retryWrites=true&w=majority"
# client= pymongo.MongoClient(os.getenv('MONGO_DB_URL'))
client= pymongo.MongoClient(URL)
 
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
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)