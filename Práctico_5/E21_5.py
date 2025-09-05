p1_c = 0
p2_c = 0
tie = 0
option = ""

def winner (x, y):
    global p1_c
    global p2_c
    global tie

    if x == "R":
        if y == "P":
            p2_c +=1
        elif y == "S":
            p1_c +=1
    elif x == "P":
        if y == "R":
            p1_c +=1
        elif y == "S":
            p2_c +=1
    elif x == "S":
        if y == "R":
            p2_c +=1
        elif y == "P":
            p1_c +=1
    
    if x == y:
        tie +=1

while option != "Parar":
    print("Ingrese la opcion de cada jugador (R, P, S). X es P1 y Y es P2: ")
    winner(input("x: "),input("y: "))
    option = input("Si desea Parar ingrese 'Parar', sino, presione enter: ")
print(f"El jugador 1 ganó {p1_c} veces, el jugador 2 ganó {p2_c} veces. Empataron {tie} veces...")

if p1_c > p2_c:
    print("Por lo tanto, Player 1 Wins!")
elif p2_c > p1_c:
    print("Por lo tanto, Player 2 Wins!")
elif p1_c == p2_c:
    print("Por lo tanto, es un empate!")