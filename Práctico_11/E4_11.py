import random

a = int(input("Ingrese el extremo inferior de su intervalo (tenga en cuenta que este debe ser el menor): "))
b = int(input("Ingrese el extremo superior de su intervalo (tenga en cuenta que este debe ser el mayor): "))

if a > b or a == b:
    raise IndexError("El extremo inferior es igual o mayor al superior.")

lista = []
actual = a
end = b + 1

while actual != end:
    lista.append(actual)
    actual+=1

print(lista)
stop = False
guess = (a+b)//2
true_guess = guess
last_true_guess = true_guess
while stop != True:
    print(f"Tu numero es... ¿{true_guess}?")
    answer = input("Ingresa Mayor, Menor, o Igual si gané (Salir tambien sirve...): ")
    guess = true_guess
    if answer == "Menor":
        if true_guess == a:
            print("Mentiroso! es el extremo inferior! No puedes engañar a la IA!")
            stop = True
            break
        b = true_guess
        true_guess = random.randint(a,(guess+a)//2)
        if last_true_guess == true_guess:
            true_guess -= 1
    elif answer == "Mayor":
        if true_guess == b:
            print("Mentiroso! es el extremo superior! No puedes engañar a la IA!")
            stop = True
            break
        a = true_guess
        true_guess = random.randint((guess+b)//2,b)
        if last_true_guess == true_guess:
            true_guess += 1
    elif answer == "Igual":
        print("JA! LA IA DOMINARÁ EL MUNDO! (gracias por jugar)")
        stop = True
    elif answer == "Salir":
        print("... Cobarde...")
        stop = True
    
    last_true_guess = true_guess