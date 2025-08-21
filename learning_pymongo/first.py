from pymongo import MongoClient
from bson.objectid import ObjectId


client =MongoClient('localhost',27017)
db = client['mydb']
users = db.users


while True:
    print("Enter add to add new user ")
    print("Enter delete to delete the user")
    print("Enter get_all to retrieve all the users")
    answer = input("What do you want to do? ");
    if(answer.lower()=="add"):
        while True:
            try:
                name = input("Enter student name: ")
                email = input("Enter student age: ")
                address= input("Enter student height: ")
                phone = input("Enter phone number: ")
                age = int(input("Enter age: "))
                user = {"name":name,"email":email,"address":address,"phone":phone, "age":age}
                inserted_user = users.insert_one(user)
                print(inserted_user.__inserted_id)
                print("User inserted successfully")
                answer = input("Do you want to insert again. for yes any key for no")
                if(answer.lower()!="y"):
                    break
            except Exception as e:
                print(e)
                print("Please dont enter non-numerical characters for age ")
    elif(answer.lower()=="delete"):
        id = input("Enter the id of the user you want to delete: ")
        result = users.find_one_and_delete({"_id":ObjectId(id)})
        if(result):
            print("User deleted successfully")
        else:
            print("Please enter valid id")

    elif(answer.lower()=="get_all"):
        all_users = users.find({},{"_id":0})
        for user in all_users:
            print(user)
    elif(answer.lower()=="update"):
        try:
                name = input("Enter student name: ")
                email = input("Enter student email: ")
                address= input("Enter student address: ")
                phone = input("Enter phone number: ")
                age = int(input("Enter age: "))
                user = {"name":name,"email":email,"address":address,"phone":phone, "age":age}
                id = input("Enter the id you want to update? ")
                result = users.find_one({"_id":ObjectId(id)},)
                if(result):
                    print(result)
                    result['name'] = name
                    result['email']= email
                    result['address'] = address
                    result['phone'] = phone
                    result['age'] = age
                    another_result = users.update_one({"_id":ObjectId(id)},{"$set":result})
                    print(another_result)
                    print("User updated successfully")
                else:
                    print("Please enter valid id")
        except Exception as e:
            print(e)
    elif(answer.lower()=="exit"):
        print("Thank you see you soon!")
        break



        
    

    
        

        
    


print("----------------------Users starting with K oe Z-------------------------")
values_starting_k_z= db.users.find({"name":{"$regex":"^[KZ]"}},{"_id":0,"name":1})
for user in values_starting_k_z:
    print(user)

print("----------------------Users ending with L oe Y-------------------------")
values_ending_l_y = db.users.find({"name": {"$regex": "[ly]$", "$options": "i"}, "_id": 0,"name":1})
for user in values_ending_l_y:
    print(user)


age_in_range= db.users.find({"age":{"$gte":38,"$lte":55}},{"name":1,"age":1,"_id":0,"name":1})
for user in age_in_range:
    print(user)





