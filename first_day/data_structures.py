

names = ['salman','sharukh','alia','ranvir','deepika']
# using for each loop
print("using for each loop")
for name in names:
    print(name)

print('-----------------------------')
print('using for loop')
# using for loop
for i in range(len(names)):
    print(names[i])

key_value = {"name":"raghab","age":21,"height":6.1}
print('name:',key_value['name'], 'age:', key_value.get('age'), 'height:',key_value.get('height'))
