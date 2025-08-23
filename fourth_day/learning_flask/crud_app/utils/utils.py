from pymongo import MongoClient
mongo_client = MongoClient('mongodb://localhost:27017');
db = mongo_client['mydb']
def skip_limit(page_size, page_num):
    # Calculate number of documents to skip
    print(type(page_size), page_num)
    skips = page_size * (page_num - 1)
  # Skip and liit
    cursor = db['users'].find().skip(skips).limit(page_size)
    print(cursor)
       
    return [x for x in cursor]