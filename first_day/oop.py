
class Person:
    # function for initializing object values
    def __init__(self,name, age, height):
        self.name= name
        self.age = age
        self.height= height

    def walk(self):
        print(self.name, ' is walking')

    def sleep(self):
        print(self.name, ' is sleeping' )

    def info(self):
        print('name: ',self.name, 'age:',self.age, 'height: ',self.height )


person =  Person('raghab', 12,6.1)
person.walk();
person.sleep();
person.info()



        