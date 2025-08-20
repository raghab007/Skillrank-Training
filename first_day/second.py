import os
a = "Some content inside the file"


file =  open("file.txt","r")

# Creating new file
newFile = open('new_file.txt','w');
content = file.read()
newFile.write(content)

file.close();
if(os.path.exists('file.txt')):
    os.remove('file.txt')
    print("File deleted")

print(content)



























# # creating another file object with read permission
# readFile =  open("file.txt",'r');

# # reading the entire content of the file and saving
# fileValue = readFile.read();

# # if value exists remove the file
# if(fileValue and os.path.exists('file.txt')):
#     os.remove('file.txt')
#     print("File deleted")
# else:
#     print("Path does not exists")


    