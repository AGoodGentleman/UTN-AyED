import random

my_list = []

for i in range(10):
    a = input("Escriba una de sus diez marcas favoritas: ")
    my_list.append(a)

print(random.choice(my_list))