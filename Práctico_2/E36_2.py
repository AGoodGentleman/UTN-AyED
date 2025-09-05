import random

print("Para más dificultad, se recomienda que haya al menos 20 numeros de separacion entre a y b.")

a = int(input("Seleccione su numero positivo a (a debe ser menor a b): "))

b = int(input("Seleccione su numero positivo b (a debe ser menor a b): "))

my_list = []

life = 10

if a >= b:
    print("Lo siento, pero a debe ser menor a b.")
elif a <= 0 or b <= 0:
    print("Lo siento, pero ambos deben ser positivos.")
else:
    for i in range(a,b+1):
        print(i)
        my_list.append(i)
    answer = random.choice(my_list)

    while life > 0:
        choice = int(input("Que numero crees que elegí? "))
        if choice == answer:
            print (f"Ganaste! Mi numero era {answer}! Te quedaron {life} vidas.")
            break
        elif choice != answer and life > 0:
            life -=1
            if life > 0:
                print(f"Lo siento! Ese no era! Prueba otra vez! Te quedan {life} vidas.")
            else:
                print(f"Oh no! Lo lamento! Te has quedado sin vidas y mi numero era {answer}.")