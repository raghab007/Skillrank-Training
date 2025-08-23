from markupsafe import escape
from flask import Flask, request,render_template,jsonify,Response
from pymongo import MongoClient
from bson import json_util, ObjectId  
from utils import utils 
import json
mongo_client = MongoClient('mongodb://localhost:27017');
db = mongo_client['mydb']
app =  Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/users')
def users_page():
   return render_template('users.html')

# get users
@app.route('/api/users/<int:pagenumber>/<int:pagesize>',methods=['GET'])
def users(pagenumber=1, pagesize=10):
    print('pagenumber', pagenumber)
    print('pagesize', pagesize)

    users = utils.skip_limit(page_num=pagenumber, page_size=pagesize)

    if not users:
        print("zero")  # no users found


    return Response(
        json.dumps(users, default=json_util.default),
        mimetype="application/json"
    )

#add users
@app.route('/api/users',methods=['POST'])
def add_user():
   try:
      data = request.get_json()

      if(not 'name' in data or not 'email' in data or not 'address' in data or not 'phone' in data or not 'age' in data):
         return {
            "message":"incomplete data provided"
         }
      users = db['users']
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
@app.route('/api/users/<userid>')
def get_user_by_id(userid):
   try:
      users = db['users']
      user = users.find_one({'_id':ObjectId(userid)})
      if(user):
         user['_id'] = str(user['_id'])
         return user
      return {
         "message":"user not found"
      }
   except Exception as e:
      print(e)
      return {
         "message":"internal server occured"
      }



# delete user by id
@app.route('/api/users/<userid>',methods= ['DELETE'])
def delete_user(userid):
   try:
      users = db['users']
      user = users.find_one_and_delete({'_id':ObjectId(userid)})
      if(user):
         return {
            "message":"user deleted successfully"
         }
      return {
         "message":"user with that id doesnot exists"
      }
   except Exception as e:
      print(e)
      return {
         "message":"internal server occured"
      }


#update user by id
@app.route('/api/users/<userid>',methods =['PUT'])
def update_user(userid):
   try:
      data= request.get_json();
   
      users = db['users']
      database_user  =users.find_one({"_id":ObjectId(userid)})
      if(database_user):
         database_user['_id'] = str(database_user['_id'])
         for key in database_user.keys():
            database_user[key] = data[key] if key in data else database_user[key]
         
         del database_user["_id"]
         users.update_one({"_id":ObjectId(userid)},{"$set":database_user})
         return {
            "message":"user updated successfully"
         }
      else :
         print("user doesnot exists")

      return {
         "message":"user does not exists"
      }
   except Exception as e:
      print('exception')
      print(e)
      return {
         "message":"internal server occured"
      }



# @app.route('/post/<int:post_id>')
# def show_post(post_id):
#     return f'Post {post_id}'

# @app.route('/path/<path:subpath>')
# def show_subpath(subpath):
#   return f'Subpath {subpath}'

@app.route('/health')
def health_check():
   return 'ok'





