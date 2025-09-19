class Cola():
    def __init__(self):
            self.value = []
    def queue(self, element):
            self.value.append(element)
    def dequeue(self):
            self.value.pop()
    def __str__(self):
        chain = ""
        for element in self.value:
            chain = chain + element + " "
        return chain 
    def empty(self):
        if len(self.value) == 0:
            return True
        else:
            return False

client_q = Cola()
obra_list = []

client = ""
obra_social = ""
c_counter = 0
o_counter = 0

while client != "0":
    client = input("Ingrese el nombre de su cliente, para parar ingrese 0: ")
    print("")
    if client != "0":
        c_counter += 1
        client_q.queue(client)
        obra_social = input("Ingrese la obra social del cliente, si no tiene ingrese 0: ")
        print("")
        if obra_social != "0":
            obra_list.append(obra_social)
        else: obra_list.append("No tiene")

for element in obra_list:
    if element == "No tiene":
        o_counter += 1

print("Usted tiene los siguientes clientes: ")
print(client_q)
print(f"Y de esos, tiene {o_counter} sin obra social y {c_counter-o_counter} con obra social.")