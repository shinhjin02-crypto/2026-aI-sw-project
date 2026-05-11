import math

print(math.pi)
print(math.e)
print(math.sqrt(16))
print(math.sin(0))
print(math.sin(math.pi))

import datetime as dt

#print(dt.datetime.now())
#print(dt.datetime.now().strftimeI('%Y-%m-%d'))
#print(dt.datetime.now().strftime('%H:%M:%S'))

a_day = dt.datetime(2025, 1, 1, 10, 00, 00)

import random

print(random.random())
print(math.floor(random.random( )* 100))
print(random.randint(1, 100))

def roll_dice():
    my_number = random.randint(1, 6)
    return my_number

print("내 주사위의 숫자는: ", roll_dice())
print("내 주사위의 숫자는: ", roll_dice())
print("내 주사위의 숫자는: ", roll_dice())
print("내 주사위의 숫자는: ", roll_dice())
print("내 주사위의 숫자는: ", roll_dice())
print("내 주사위의 숫자는: ", roll_dice())

fruits = ['apple', 'banana', 'cherry', 'grape', 'orange', 'pineapple']

def pick_fruit():
    my_number = random.radint(0, len(fruits) - 1)
    my_pick = fruits[my_number]
    return my_pick

def pick_fruit2():
    return random.choice(fruits)

print("내 과일은: ", pick_fruit())
print("내 과일은: ", pick_fruit())
print("내 과일은: ", pick_fruit())
print("내 과일은: ", pick_fruit())
print("내 과일은: ", pick_fruit())
print("내 과일은: ", pick_fruit())

print("내 과일은2: ", pick_fruit2())
print("내 과일은2: ", pick_fruit2())
print("내 과일은2: ", pick_fruit2())
print("내 과일은2: ", pick_fruit2())
print("내 과일은2: ", pick_fruit2())
print("내 과일은2: ", pick_fruit2())

