class Pila:
    def __init__(self):
        self.value = []
    def push(self, element):
        self.value.insert(0, element)
    def pop(self):
        self.value.pop(0)
    def __str__(self):
        chain = ""
        for element in self.value:
            chain += element
        return chain
    def empty(self):
        if len(self.value) == 0:
            return True
        else:
            return False

file_name1 = "texto.txt"

file_name2 = "invertido.txt"

file1 = open(file_name1, "w")

file2 = open(file_name2, "w")

word = ""

pile = Pila()

stop = False

while stop == False:

    line = input("Ingrese una línea de texto, si quiere parar, ingrese 0: ")
    if line != "0":
        file1.write(f"{line}\n")
    else:
        stop = True

file1 = open(file_name1,"r")

for char in file1.read():
    if char != " " and char != "\n":
        word += char
    else:
        pile.push(word)
        word = ""

print(pile.value)

for element in pile.value:
    file2.write(f"{element}\n")

file2 = open(file_name2,"r")

print(file2.read())