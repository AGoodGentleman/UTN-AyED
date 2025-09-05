user_list = ["Agustín", "Ariel", "Gustavo", "Matías", "Valentín"]

user = input("Ingrese su nombre con mayúsculas y tildes: ")

counter = 0

for index in range(len(user_list)):
    if user_list[index] == user:
        print(f"Bienvenido {user}")
        break
else: counter = 1

if counter == 1 and user != index:
    print("Usted no es un usuario válido.")