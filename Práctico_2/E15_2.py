my_list = [56, 7, 34, 19, 3, 1, 76, 2, 81, 4, 2, 8]

for index in range(0, len(my_list), 2):
    print(my_list[index])

print("")

for index in range(len(my_list)):
    if index%2 == 0:
        print(my_list[index])

#Es aconsejable hacer un loop con step 2 o un loop con mod 2 == 0 por temas de eficiencia.