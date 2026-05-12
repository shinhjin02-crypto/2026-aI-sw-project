from employee import Employee
from person import Person

employee1 = Employee("James", 25, "Samsung")
employee2 = Employee("Jhon", 27, "LG")
employee3 = Person("Bob", 35, "Samsung")

employee1.greet()
employee2.greet()
employee3.greet()

employee3.set_age(40)
employee3.greet()
print(employee3.get_name())