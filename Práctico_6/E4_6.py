import random

file_name = "archivo_4.txt"

file = open(file_name, "a")

counter = 0

for i in range(10):
    file.write(f"{random.randint(1,10)}\n")

file.close

file = open(file_name, "r")

for line in file:
    line = line.strip()
    print(line)
    if line == "5":
        counter += 1

print(f"Hay {counter} cincos.")

file.close