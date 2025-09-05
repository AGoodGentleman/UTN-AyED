import random

counter = 0

average = 0

for i in range(2500):
    throw = random.randint(1,6)
    average = average + throw
    print(throw)
    counter += 1

print(counter) #Para asegurar que haya 2500 tiradas

print(average/2500)

#Por pura matemática estadística, 2500 tiradas son mucho más precisas en su media, es decir, mas cercanas al 3, que solo 20.