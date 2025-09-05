qty = int(input("Ingrese cuantos numeros quiere promediar: "))

summ = 0

list_a = []

for i in range(qty):
    list_a.append(int(input("Ingrese uno de los numeros: ")))

for element in list_a:
    summ = summ + element

def average (x, y):
    global summ
    global qty
    return(summ/qty)

print(f"El promedio es {average(summ, qty)}.")