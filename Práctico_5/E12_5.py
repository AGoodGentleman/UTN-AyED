def pyramid_i (char, width):
    i = width

    while i > 0:
        for j in range (i):
            print(char, end=" ")
        print("")
        i-=1

pyramid_i(input("Ingrese el carácter en el que basar su piramide: "), int(input("Ingrese la anchura inicial de su piramide: ")))

def pyramid (char, width):
    
    k = (width-1)
    
    while k >= 0:
        for l in range (width-k):
                print(char, end=" ")
        print("")
        k-=1

pyramid(input("Ingrese el carácter en el que basar su piramide: "), int(input("Ingrese la anchura inicial de su piramide: ")))