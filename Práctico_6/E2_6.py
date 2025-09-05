import random

file_name = "números.txt"

file = open(file_name, "a")

for i in range(10):
    file.write(f"{random.randint(0,100)}\n")

file = open(file_name, "r")

print(file.read())

file.close()