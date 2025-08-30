from flask import Flask, request, jsonify, Response, render_template
from bson import json_util, ObjectId
import json
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=os.getenv("AZURE_ENPOINT"),
    api_key=os.getenv("API_KEY")
)

uri = os.getenv("MONGO_URL")

# Create a new client and connect to the server
mongo_client = MongoClient(uri, tlsAllowInvalidCertificates=True, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    mongo_client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = mongo_client['mydb']

app = Flask(__name__)
CORS(app)

def serialize_user(user_doc):
    if not user_doc:
        return None
    user_doc["_id"] = str(user_doc["_id"])
    return user_doc

@app.route('/')
def home():
    return jsonify({"message": "Hello from Lambda Flask MongoDB app!"})



def  ai_response(content):
    system_prompt = """
    You are a JSON API generator. 
    Convert user requests into CRUD operations for MongoDB.
    Response format ONLY:
    {
      "operation": "create|read|update|delete",
      "collection": "users",
      "filter": {...},     # for read, update, delete
      "data": {...}        # for create, update
    }
    """
    response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": content,
        }
    ],
    max_completion_tokens=16384,
    model="gpt-5-mini"
    )
    print(json.loads(response.choices[0].message.content))
    return (json.loads(response.choices[0].message.content))


@app.route("/chat/<content>",methods=['GET'])
def chat(content):
    try:
        genereted= ai_response(content)
        print(genereted)
        print(genereted['operation'])
        if(genereted['operation']=="create"):
           res =  db['users'].insert_one(genereted['data'])
           print(res)
           return jsonify({"message":"user inserted"})
        elif(genereted['operation']=='update'):
            res = db['users'].update_one(genereted['filter'],genereted['data'])
            return jsonify({"message":"user updated"})
        elif(genereted['operation']=='delete'):
            filter = genereted['filter']
            data= genereted['data']
            res = db['users'].delete_many(filter,data)
            return jsonify({"message":"users deleted"})
        elif(genereted['operation']=='read'):
            filter = genereted['filter']
            users = db['users'].find(filter)
            all_users = []
            for user in users:
                all_users.append(serialize_user(user))
            return jsonify({"message":"all users ","users":all_users})

    except Exception as e:
        print(e)
        return jsonify("Internal server error occured")
  


@app.route('/users')
def users_page():
    return jsonify({"message": "Hello from Raghab Flask MongoDB app!"})

@app.route('/api/users/<int:pagenumber>/<int:pagesize>', methods=['GET'])
def get_users(pagenumber=1, pagesize=10):
    if(pagenumber<1):
        return  {}

    users_cursor = db.users.find().skip((pagenumber - 1) * pagesize).limit(pagesize)
    users_list = [serialize_user(u) for u in users_cursor]
    data  = {"users":users_list, "count":db.users.count_documents({})}
    return Response(json.dumps(data, default=json_util.default), mimetype="application/json")

@app.route('/api/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json(force=True)
        required_fields = ["name", "email", "address", "phone", "age"]
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Incomplete data provided"}), 400
        db.users.insert_one(data)
        return jsonify({"message": "Data inserted successfully"}), 201
    except Exception as e:
        print("Add user error:", e)
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

@app.route('/api/users/<userid>', methods=['GET'])
def get_user_by_id(userid):
    try:
        user = db.users.find_one({"_id": ObjectId(userid)})
        user = serialize_user(user)
        if user:
            return jsonify(user)
        return jsonify({"message": "User not found"}), 404
    except Exception as e:
        print("Get user error:", e)
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

@app.route('/api/users/<userid>', methods=['PUT'])
def update_user(userid):
    try:
        data = request.get_json(force=True)
        user = db.users.find_one({"_id": ObjectId(userid)})
        if not user:
            return jsonify({"message": "User does not exist"}), 404
        update_fields = {k: v for k, v in data.items() if k in user}
        db.users.update_one({"_id": ObjectId(userid)}, {"$set": update_fields})
        return jsonify({"message": "User updated successfully"})
    except Exception as e:
        print("Update user error:", e)
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

@app.route('/api/users/<userid>', methods=['DELETE'])
def delete_user(userid):
    try:
        result = db.users.find_one_and_delete({"_id": ObjectId(userid)})
        if result:
            return jsonify({"message": "User deleted successfully"})
        return jsonify({"message": "User with that ID does not exist"}), 404
    except Exception as e:
        print("Delete user error:", e)
        return jsonify({"message": "Internal server error", "error": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return "ok"

# # ===================== Lambda Handler =====================
# def lambda_handler(event, context):
#     import awsgi
#     return awsgi.response(app, event, context)

if __name__ == "__main__":
    app.run(debug=True)
