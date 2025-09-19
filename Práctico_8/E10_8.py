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

keep_going = True
Y_N = "Y"
i = 0

while keep_going == True:
    while i < 5:
        client_q.queue(input("Ingrese el nombre y el órden de carta que haya entregado ESTA VEZ (primera, segunda, tercera...).\nTenga en cuenta que no se aceptarán más de 5 por persona: "))
        i += 1
        if i == 5:
            print("")
            print("Su límite ha sido alcanzado, por favor haga de vuelta la cola si desea enviar más cartas.")
            print("")
    
    i = 0
    Y_N = input("Si hay más personas en la cola, ingrese Y, de lo contrario, N: ")
    if Y_N == "Y":
         keep_going = True
    elif Y_N == "N":
         keep_going = False

print(client_q.value)