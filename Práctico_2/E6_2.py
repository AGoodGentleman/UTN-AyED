name = input("Ingrese su nombre: ")
surname = input("Ingrese su apellido: ")

u_name = (name[0]).upper()
u_surname = (surname[0]).upper()

l_name = (name[1:]).lower()
l_surname = (surname[1:]).lower()

print(u_name + l_name)
print(u_surname + l_surname)