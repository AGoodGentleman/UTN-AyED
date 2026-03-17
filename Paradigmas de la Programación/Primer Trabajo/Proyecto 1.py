# import matplotlib.pyplot as plt

# ACLARACIÓN
# En este trabajo, se consultó a IA's (específicamente a ChatGPT) para su llevada a cabo.

# --- RESUMEN --- ETAPA 1
#Necesitamos que el usuario ingrese de 5 a 10 títulos de canciones como tal para luego ingresar sus letras.
#Se limitará las letras a 200 palabras para evitar usar almacenamiento de sobra.
#Luego usaremos bucles para contabilizar las palabras positivas y las palabras negativas para poder puntuar las canciones.
#Esta puntuación se dará en base a criterios predeterminados.
#Uno podría ser definir una lista de las 50 palabras positivas y negativas más frecuentes.
#Esta puntuación será del 1 al 10, donde 1 es negativa y 10 positiva. Empezamos en 5 y sumamos o restamos 0,25.

# --- BOCETO --- ETAPA 1
#Definir la lista de palabras negativas y positivas, y los demás criterios de puntuación.
#Pedir el input del usuario para anotar las canciones y sus letras recordandole la limitacion de 200 palabras.
#Crear un bucle identificando las palabras y sumando o restando puntos.
#Una vez terminado, pasarle al usuario la lista de canciones, solo sus títulos, y su respectiva puntuación.

# --- CÓDIGO ---

lista_positivas = [
    "amor", "amar", "feliz", "felicidad", "alegria", "sonreir", "sonrisa", "luz",
    "brillar", "brillo", "esperanza", "sueño", "sueños", "vivir", "vida", "libre",
    "libertad", "paz", "calma", "dulce", "dulzura", "abrazo", "besar", "beso",
    "cielo", "estrella", "sol", "bailar", "cantar", "magia", "milagro", "belleza",
    "hermoso", "hermosa", "eterno", "eternidad", "confianza", "fuerza",
    "victoria", "ganar", "triunfo", "celebrar", "placer", "gozo", "encantar",
    "ilusion", "volar", "flotar", "brisa"
]

lista_negativas = [
    "odio", "odiar", "triste", "tristeza", "llorar", "llanto", "dolor", "sufrir",
    "sufrimiento", "miedo", "temor", "oscuridad", "sombra", "perder", "perdido",
    "caer", "caida", "romper", "roto", "soledad", "solo", "abandono", "abandonar",
    "mentira", "mentir", "engaño", "herida", "herir", "culpa", "culpar", "pena",
    "destruir", "destruido", "fracaso", "fallar", "derrota", "morir", "muerte",
    "vacío", "vacio", "gritar", "grito", "duda", "perdicion", "tormenta",
    "infierno", "frio", "lagrima", "lagrimas"
]

lista_canciones = []
lista_puntajes = []
lista_longitudes = []
vocales = ["a", "e", "i", "o", "u"]


def contar_palabras_manual(texto):
    contador = 0
    en_palabra = False

    for caracter in texto:
        if caracter != " " and caracter != "," and caracter != "." and caracter != ":" and caracter != ";" and caracter != "\n" and caracter != "\t":
            if en_palabra is False:
                contador += 1
                en_palabra = True
        else:
            en_palabra = False

    return contador


def analizar_letra(letra_original):
    c_v = 0
    c_c = 0
    puntaje = 5.0
    palabra = ""
    longitud = 0

    letra = letra_original.lower() + " "

    for caracter in letra:
        if caracter == " " or caracter == "," or caracter == "." or caracter == ":" or caracter == ";" or caracter == "\n" or caracter == "\t":
            for elemento in lista_positivas:
                if palabra == elemento:
                    puntaje += 0.25

            for elemento in lista_negativas:
                if palabra == elemento:
                    puntaje -= 0.25

            for caracter_palabra in palabra:
                if caracter_palabra.isalpha():
                    longitud += 1
                    es_vocal = False

                    for element in vocales:
                        if caracter_palabra == element:
                            c_v += 1
                            es_vocal = True
                            break

                    if es_vocal is False:
                        c_c += 1

            palabra = ""
        else:
            palabra += caracter

    if c_v > c_c:
        puntaje += 0.1

    if puntaje < 1:
        puntaje = 1
    elif puntaje > 10:
        puntaje = 10

    return puntaje, longitud


cantidad_canciones = int(input("Ingrese la cantidad de canciones: "))

if cantidad_canciones < 5 or cantidad_canciones > 10:
    raise ValueError("El límite de canciones es entre 5 y 10, intente nuevamente.")

n = 0

while n < cantidad_canciones:
    titulo = input("Ingrese el nombre de la siguiente canción: ")
    letra = input("Ingrese la letra de la canción, recuerde que hay un límite de 200 palabras: ")

    while contar_palabras_manual(letra) > 200:
        print("La letra supera las 200 palabras.")
        letra = input("Reingrese la letra de la canción: ")

    puntaje, longitud = analizar_letra(letra)

    lista_canciones.append(titulo)
    lista_puntajes.append(puntaje)
    lista_longitudes.append(longitud)

    n += 1

print("El proceso ha terminado:")
print("")

for i in range(len(lista_canciones)):
    print(f"{lista_canciones[i]}")
    print(f"Se ha puntuado con {lista_puntajes[i]}.")
    print(f"Longitud de letra: {lista_longitudes[i]} caracteres alfabéticos.")

    if lista_puntajes[i] < 5:
        print("La canción se considera triste o con emociones negativas.")
    elif lista_puntajes[i] > 5:
        print("La canción se considera alegre o con emociones positivas.")
    else:
        print("La canción se considera neutral.")
    print("")

# --- RESUMEN --- ETAPA 2
# Debemos crear una cola, encolar las canciones teniendo en cuenta la transición de las emociones y guardarla en un txt.
# Debemos leer un archivo inicial si existe.
# Debemos agregar una función que le permita al usuario encolar canciones adicionales.

# --- BOCETO --- ETAPA 2
# Tengo una estructura de cola ya desarrollada, solo la pegaré y modificaré.
# Además, creo que debería hacer un diccionario con las canciones y su puntaje para poder ordenarlas de manera eficiente.
# Para dicho ordenamiento, creo que con un algoritmo de ordenado lineal, que ya tengo también, estaría bien

# PREGUNTAR: Cuando pide leer el archivo si es que existe y sinó crearlo, que se espera que se haga? (Try/Except ?)

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue vacía")
        return self.items.pop(0)

    def front(self):
        if self.is_empty():
            raise IndexError("Cola vacía")
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)


cola_canciones = Queue()

try:
    with open("canciones.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if linea != "":
                partes = linea.split(",")
                if len(partes) >= 3:
                    titulo_arch = partes[0]
                    score_arch = float(partes[1])
                    longitud_arch = int(partes[2])
                    cola_canciones.enqueue((titulo_arch, score_arch, longitud_arch))
except FileNotFoundError:
    pass

i = 0
while i < len(lista_canciones):
    cola_canciones.enqueue((lista_canciones[i], lista_puntajes[i], lista_longitudes[i]))
    i += 1

choice = input("¿Desea encolar más canciones? ")

while choice.lower() == "si":
    song = input("Ingrese el nombre de la canción a encolar: ")
    score = float(input("Ingrese el puntaje de la canción: "))
    longitud = int(input("Ingrese la longitud de la letra de la canción: "))
    cola_canciones.enqueue((song, score, longitud))
    choice = input("¿Desea encolar más canciones? ")

playlist_procesada = []
anterior_score = None

while cola_canciones.is_empty() == False:
    cancion = cola_canciones.dequeue()
    titulo = cancion[0]
    score = cancion[1]
    longitud = cancion[2]

    print(f"Reproduciendo: {titulo} - Score: {score} - Longitud: {longitud}")

    if anterior_score is not None:
        if anterior_score < 5 and score > 5:
            print("Transición emocional: de triste a feliz")
        elif anterior_score > 5 and score < 5:
            print("Transición emocional: de feliz a triste")
        else:
            print("Transición emocional: sin cambio fuerte")

    playlist_procesada.append((titulo, score, longitud))
    anterior_score = score

with open("canciones.txt", "w", encoding="utf-8") as archivo:
    i = 0
    while i < len(playlist_procesada):
        archivo.write(
            f"{playlist_procesada[i][0]},{playlist_procesada[i][1]},{playlist_procesada[i][2]}\n"
        )
        i += 1

# --- RESUMEN --- ETAPA 3
# Se nos pide ordenar las canciones manualmente usando inserción manual.
# Debemos ademas crear una pila como historial de skips que se pueda deshacer dichos skips y reordenarla.
# Hay que usar "MatPlotLib" para hacer un grafico de barras con los puntajes.
# Finalmente, hay que manejar empates emocionales y listas repetitivas o loopeadas con criterios como la longitud de letras.

# --- BOCETO --- ETAPA 3
# Bien, entonces, ordenar usando inserción manual como algoritmo.
# Crear una pila y dar la capacidad de deshacer y reordenar.
# Crear un grafico de barras.
# Manejar empates emocionales y listas repetitivas o loopeadas con criterios.

def debe_ir_antes(cancion_a, cancion_b):
    # Formato: (titulo, score, longitud)
    # Regla principal: ordenar por score ascendente
    # Desempate emocional: si los scores difieren en 0.5 o menos, va primero la de menor longitud
    if abs(cancion_a[1] - cancion_b[1]) <= 0.5:
        if cancion_a[2] != cancion_b[2]:
            return cancion_a[2] < cancion_b[2]
        return cancion_a[0].lower() < cancion_b[0].lower()

    return cancion_a[1] < cancion_b[1]


def insertion_sort_canciones(lista):
    copia = lista[:]

    for i in range(1, len(copia)):
        actual = copia[i]
        j = i - 1

        while j >= 0 and debe_ir_antes(actual, copia[j]):
            copia[j + 1] = copia[j]
            j -= 1

        copia[j + 1] = actual

    return copia


def detectar_empates(lista):
    empates = []
    i = 0

    while i < len(lista):
        j = i + 1
        while j < len(lista):
            if abs(lista[i][1] - lista[j][1]) <= 0.5:
                empates.append((lista[i], lista[j]))
            j += 1
        i += 1

    return empates


def detectar_loops(lista):
    loops = []

    i = 0
    while i < len(lista):
        j = i + 1
        while j < len(lista):
            if lista[i][0].lower() == lista[j][0].lower() and (j - i) <= 3:
                loops.append(("titulo_repetido", i, j))
            j += 1
        i += 1

    i = 0
    while i < len(lista) - 2:
        if abs(lista[i][1] - lista[i + 1][1]) <= 0.5 and abs(lista[i + 1][1] - lista[i + 2][1]) <= 0.5:
            loops.append(("bloque_emocional", i, i + 2))
        i += 1

    return loops


def resolver_loops_por_longitud(lista):
    # Propone y aplica una variante:
    # Si hay 3 canciones seguidas con emoción muy similar, intercambia la del medio con una más diferente en longitud.
    copia = lista[:]
    i = 0

    while i < len(copia) - 2:
        if abs(copia[i][1] - copia[i + 1][1]) <= 0.5 and abs(copia[i + 1][1] - copia[i + 2][1]) <= 0.5:
            indice_mejor = -1
            diferencia_mejor = -1
            j = i + 3

            while j < len(copia):
                diferencia_actual = abs(copia[i + 1][2] - copia[j][2])
                if diferencia_actual > diferencia_mejor:
                    diferencia_mejor = diferencia_actual
                    indice_mejor = j
                j += 1

            if indice_mejor != -1:
                temp = copia[i + 1]
                copia[i + 1] = copia[indice_mejor]
                copia[indice_mejor] = temp

        i += 1

    return copia


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack vacío")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack vacío")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)

copia_playlist = playlist_procesada[:]

playlist_ordenada = insertion_sort_canciones(copia_playlist)

empates = detectar_empates(playlist_ordenada)

print("Empates emocionales detectados:")
if len(empates) == 0:
    print("No se detectaron empates.")
else:
    for par in empates:
        print(
            f"{par[0][0]} ({par[0][1]}, longitud {par[0][2]}) y "
            f"{par[1][0]} ({par[1][1]}, longitud {par[1][2]})"
        )
        if par[0][2] < par[1][2]:
            print(f"Desempate: se prioriza {par[0][0]} por menor longitud.")
        elif par[1][2] < par[0][2]:
            print(f"Desempate: se prioriza {par[1][0]} por menor longitud.")
        else:
            print("Desempate: misma longitud, se mantiene orden alfabético.")

print("")

loops_detectados = detectar_loops(playlist_ordenada)

print("Loops detectados:")
if len(loops_detectados) == 0:
    print("No se detectaron loops.")
else:
    for loop in loops_detectados:
        print(loop)

print("")

playlist_final = resolver_loops_por_longitud(playlist_ordenada)
print("Playlist final reordenada:")
for cancion in playlist_final:
    print(f"{cancion[0]} - Score: {cancion[1]} - Longitud: {cancion[2]}")

print("")

historial_skips = Stack()
cola_reproduccion_final = Queue()

for cancion in playlist_final:
    cola_reproduccion_final.enqueue(cancion)

choice_skip = input("¿Desea simular skips? ")

while choice_skip.lower() == "si" and not cola_reproduccion_final.is_empty():
    cancion_actual = cola_reproduccion_final.dequeue()
    print(f"Skip de: {cancion_actual[0]}")
    historial_skips.push(cancion_actual)

    otra = input("¿Desea deshacer el último skip? ")
    if otra.lower() == "si" and not historial_skips.is_empty():
        restaurada = historial_skips.pop()
        cola_reproduccion_final.items.insert(0, restaurada)
        print(f"Se restauró: {restaurada[0]}")

    choice_skip = input("¿Desea simular otro skip? ")

x_graf = []
y_graf = []

for cancion in playlist_final:
    x_graf.append(cancion[0])
    y_graf.append(cancion[1])


plt.bar(x_graf, y_graf)