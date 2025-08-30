from pymongo import MongoClient
from urllib.parse import quote_plus
password = quote_plus("Praghab@123##")
username = "pokhrelraghab60"

mongo_client = MongoClient(f'mongodb+srv://{username}:{password}@cluster0.q4dyd0y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0');
db = mongo_client['mydb']
def skip_limit(page_size, page_num):
    # Calculate number of documents to skip
    print(type(page_size), page_num)
    skips = page_size * (page_num - 1)
  # Skip and liit
    cursor = db['users'].find().skip(skips).limit(page_size)
    print(cursor)
       
    return [x for x in cursor]




import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps({"message":"Hello from Lambda!"})
    }

# from pymongo import MongoClient
# import json

# def lambda_handler(event, context):
#     username = "pokhrelraghab60"
#     password = "Raghab"
#     client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.q4dyd0y.mongodb.net/?retryWrites=true&w=majority")
#     db = client['mydb']
#     try:
#         count = db['users'].count_documents({})
#         return {
#         'statusCode': 200,
#         'body': json.dumps({"message":"Hello from Lambda!"})
#     }
#     except Exception as e:
#         return {
#         'statusCode': 500,
#         'body': json.dumps('Error!')
#     }
