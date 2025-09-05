#For loop:

num = int(input("Ingrese el numero desde el cual hacer la cuenta regresiva: "))

for i in range(num):
    print(num - i)
else: print("0")

#While loop:

num = int(input("Ingrese el numero desde el cual hacer la cuenta regresiva: "))

j = 0

while j < num:
    print(num - j)
    j += 1
else: print("0")