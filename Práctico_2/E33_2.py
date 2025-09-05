num_list = []

q_num = 0

odd = False

num = 0

even_sum = 0

while num != 99:
    q_num = int(input("Ingrese la cantidad de numeros que quiera ingresar: "))
    for i in range(q_num):
        num = float(input("Ingrese el siguiente numero: "))
        if num == 99:
            break
        else: 
            if num%2 == 1 or num%-2 == 1:
                odd = True
            else:
                if num%2 == 0 or num%-2 == 0:
                    even_sum = even_sum + num
    num = 99

if odd == True:
    print("Se ingresaron impares.")
else:
    print("No se ingresaron impares.")

print(f"La suma de los numeros pares es {even_sum}.")