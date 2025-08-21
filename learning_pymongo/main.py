import pymongo
client  = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['school']
users = db.users


while True:
    print("Enter add for adding ")
    answer = input("What do you want to do ?'Add', 'Update' ,'Delete','Getll','GetByName' or  Quit for exit ");
    if(answer.lower()=="add"):
        while True:
            try:
                name = input("Enter student name?: ")
                age = int(input("Enter student age?: "))
                height= int(input("Enter student height: "))
                user = {"Name":name, "Age":age, "Height":height}
                inserted_user = users.insert_one(user)
                print("User inserted successfully")
                answer = input("Do you want to insert again. for yes any key for no")
                if(answer.lower()!="y"):
                    break
            except Exception as e:
                print(e)
                print("Please dont enter non-numerical characters for age or height")
    elif (answer.lower()=="getall"):
        all_users = users.find()
        for user in all_users:
            print(user)
    elif(answer.lower()=="getbyname"):
        name = input("Enter the student name you want to get: ")
        students_by_name = users.find({"Name":name})

        for student in students_by_name:
            print(student)
    elif (answer.lower()=="quit"):
        break
    else:
        print("Enter valid command please")







