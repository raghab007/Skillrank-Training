from markupsafe import escape
from flask import Flask, request,render_template,jsonify,Response
from pymongo import MongoClient
from bson import json_util, ObjectId   
import json
mongo_client = MongoClient('mongodb://localhost:27017');
db = mongo_client['mydb']
app =  Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

# get users
@app.route('/users',methods=['GET'])
def users():
   # return render_template("users.html")
   users = db.users.find()

   return Response(
        json.dumps(list(users), default=json_util.default),
        mimetype="application/json"
    )
   
#add users
@app.route('/users',methods=['POST'])
def add_user():
   try:
      data = request.get_json()
      print(data['name'])
      if(not 'name' in data or not 'email' in data or not 'address' in data or not 'phone' in data or not 'age' in data):
         return {
            "message":"incomplete data provided"
         }
      users = db['users']
      print(data)
      users.insert_one(data)
      return {
         "message":"data inserted successfully"
      }
   except Exception as e:
      print(e)
      return {
         "message":"internal server occurred"
      }

#get user by id
@app.route('/users/<userid>')
def get_user_by_id(userid):
   try:
      users = db['users']
      user = users.find_one({'_id':ObjectId(f"{userid}")})
      user['_id'] = str(user['_id'])
      return user
   except Exception as e:
      print(e)
      return {
         "message":"internal server occured"
      }



# delete user by id
@app.route('/users/<userid>',methods= ['DELETE'])
def delete_user(userid):
   try:
      users = db['users']
      user = users.find_one_and_delete({'_id':ObjectId(f"{userid}")})
      print('user deleted', user)
      return {
         "message":"user deleted successfully"
      }
   except Exception as e:
      print(e)
      return {
         "message":"internal server occured"
      }



# @app.route('/user/<username>',methods=['POST'])
# def show_user_profile(username):
#     return f'User {username}'


# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     return f'Post {post_id}'

# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#   return f'Subpath {subpath}'

@app.route('/health')
def health_check():
   return 'ok'



