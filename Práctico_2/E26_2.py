import random

counter = 0

average = 0

for i in range(20):
    throw = random.randint(1,6)
    average = average + throw
    print(throw)
    counter += 1

print(counter) #Para asegurar que haya 20 tiradas

print(average/20)