def prime(num):
    if num < 2 and num > -2:
        print("No es primo.")
        return
    
    if num > 0:
        for i in range(2, num):
            if num % i == 0:
                print("No es primo.")
                return
    else:
        for i in range(-2, num, -1):
            if num % i == 0:
                print("No es primo.")
                return

    print("Es primo.")

prime(int(input("Ingrese un número. A continuación, se verificará si es o no primo: ")))