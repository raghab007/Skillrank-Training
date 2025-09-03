
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, Response, render_template
from bson import json_util, ObjectId
import json
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from utils import utils

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



# creating app instance
app = Flask(__name__)
CORS(app)






@app.route('/')
def home():
    return jsonify({"message": "Hello from Lambda Flask MongoDB app!"})



@app.route('/web/<query>',methods=["POST"])
def web(query):
    try:
        utils.scrape(query)
        files = os.listdir("data")
        # collection = {"title":[],"price":[],"link":[]}
        data= utils.collect(files)
        web_data = db["web_data"]
        web_data.insert_many(data)
        return jsonify({
            "message":"successfully collected and inserted into the database",
            "total collected":len(data)
        })
    except Exception as e:
        print(e)
        return jsonify({"message":"internal error occurred"})





@app.route("/chat/<content>", methods=['GET'])
def chat(content):
    try:
        generated = utils.ai_response(content)
        print(generated)

        # If the response is a message (not a CRUD operation)
        if "response" in generated:
            return jsonify({"message": generated["response"]})

        # Handle CRUD operations
        if generated['operation'] == "create":
            res = db['users'].insert_one(generated['data'])
            print(res)
            return jsonify({"message": "User created successfully", "operation": "create"})
        elif generated['operation'] == 'update':
            res = db['users'].update_many(generated['filter'], generated['data'])
            return jsonify({"message": "User updated successfully", "operation": "update"})
        elif generated['operation'] == 'delete':
            res = db['users'].delete_many(generated['filter'])
            return jsonify({"message": f"{res.deleted_count} user(s) deleted successfully", "operation": "delete"})
        elif generated['operation'] == 'read':
            filter = generated['filter']
            users = db['users'].find(filter)
            all_users = []
            for user in users:
                all_users.append(utils.serialize_user(user))
            return jsonify({"message": f"Found {len(all_users)} user(s)", "users": all_users, "operation": "read"})

    except Exception as e:
        print(e)
        return jsonify({"message": "Internal server error occurred"})


@app.route('/users')
def users_page():
    return jsonify({"message": "Hello from Raghab Flask MongoDB app!"})


@app.route('/api/users/<int:pagenumber>/<int:pagesize>', methods=['GET'])
def get_users(pagenumber=1, pagesize=10):
    if (pagenumber < 1):
        return {}

    users_cursor = db.users.find().skip((pagenumber - 1) * pagesize).limit(pagesize)
    users_list = [utils.serialize_user(u) for u in users_cursor]
    data = {"users": users_list, "count": db.users.count_documents({})}
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
        user = utils.serialize_user(user)
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


if __name__ == "__main__":
    app.run(debug=True)