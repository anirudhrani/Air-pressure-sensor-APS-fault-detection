import pymongo
import pandas as pd
import json


client= pymongo.MongoClient('')
 
DATAPATH= 'D:\aps_fault_detection_main\aps_failure_training_set1.csv'
DATABASE_NAME= 'aps'
COLLECTION_NAME= 'sensor'

if __name__== '__main__':

    df= pd.read_csv('aps_failure_training_set1.csv')
    print(f'Data {df.shape}')

# Converting a dataframe to json format for inserting into mongodb.
    df.reset_index(inplace= True, drop = True)

    # json.loads converts any python object to json object.
    json_records= list(json.loads(df.T.to_json()).values())
    test= df.T.to_json()
    print(f'test {test}')
    print(f'Final {json_records[0]}')
    
    # Bulk insert data to mongo db
    client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_records)