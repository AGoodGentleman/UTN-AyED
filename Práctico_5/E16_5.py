def equal (num):
    
    counter_0 = 0
    counter_1 = 0
    
    for element in num:
        if element == "0":
            counter_0 += 1 
        elif element == "1":
            counter_1 += 1
        else:
            pass
    return(counter_0, counter_1)

print(equal(str(input("Ingrese un numero completo y sin espacios, el primer dígito serán los 0 y el segundo dígito serán los 1: "))))