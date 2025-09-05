counter_0 = 0

counter_1 = 0

counter_2 = 0

counter_3 = 0

counter_4 = 0

counter_5 = 0

counter_6 = 0

counter_7 = 0

counter_8 = 0

counter_9 = 0

numbers = input("Ingrese una cadena de numeros: ")

original_list = []

for index in range(len(numbers)):
    original_list.append(numbers[index])

for element in original_list:
    if element == "0":
        counter_0 +=1
    elif element == "1":
        counter_1 +=1
    elif element == "2":
        counter_2 +=1
    elif element == "3":
        counter_3 +=1
    elif element == "4":
        counter_4 +=1
    elif element == "5":
        counter_5 +=1
    elif element == "6":
        counter_6 +=1
    elif element == "7":
        counter_7 +=1
    elif element == "8":
        counter_8 +=1
    elif element == "9":
        counter_9 +=1

new_list = [counter_0, counter_1, counter_2, counter_3, counter_4, counter_5, counter_6, counter_7, counter_8, counter_9]

print(new_list)