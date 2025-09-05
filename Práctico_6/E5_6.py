import random

file_name = "archivo_5.txt"

file = open(file_name, "a")

summ = 0

average = 0

for i in range(10):
    file.write(f"{random.randint(1,100)}\n")

file.close

file = open(file_name, "r")

for line in file:
    line = line.strip()
    print(line)
    summ = summ + int(line)

average = summ/10

print(f"La suma de todos ellos es {summ}.")

print(f"El promedio de todos ellos es {average}.")

file.close