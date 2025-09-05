q_num = int(input("Ingrese la cantidad de numeros a evaluar (Tenga en cuenta que el centro sera 0, por lo tanto elija conscientemente valores menores y mayores): ")) 

inf = 0
sup = 0

for i in range(q_num):

    num = float(input("Ingrese su siguiente numero: "))

    if num <= inf and num < sup:
        inf = num
    elif num >= sup and num > inf:
        sup = num

if num <= inf and num < sup:
        inf = num
elif num >= sup and num > inf:
        sup = num

print(inf, sup)