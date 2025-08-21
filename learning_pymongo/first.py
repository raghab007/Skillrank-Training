from pymongo import MongoClient
from faker import Faker
client =MongoClient('localhost',27017)
db = client['mydb']



# faker = Faker();
# records = []
# for _ in range(1000):
#     record = {
#        "name":faker.name(),
#        "email":faker.email(),
#        "address":faker.address(),
#        "phone":"+1"+faker.phone_number(),
#        "age":faker.random_int(min=1,max=100)
#     }
#     records.append(record)
# db.users.insert_many(records)


# print("running")

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





