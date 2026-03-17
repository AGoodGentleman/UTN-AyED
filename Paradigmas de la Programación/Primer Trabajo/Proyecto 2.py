# import matplotlib.pyplot as plt

# ACLARACIÓN
# En este trabajo, se consultó a IA's (específicamente a ChatGPT) para su llevada a cabo.

# --- RESUMEN --- ETAPA 1
# Leer un archivo txt con 10 posts de redes sociales.
# Cada línea tendrá un usuario y un post.
# Limitar cada post a 140 caracteres.
# Recorrer cada post letra por letra para contar mayúsculas y minúsculas.
# Si más del 50% de las letras son mayúsculas, invertir el post manualmente.
# Mostrar una alerta si aparece una palabra clave como "secreto" o "conspiracion".

# --- BOCETO --- ETAPA 1
# Abrir el archivo en modo lectura.
# Leer línea por línea.
# Recorrer cada línea carácter por carácter para separar manualmente usuario y post.
# Recortar el post a 140 caracteres usando un contador o un bucle.
# Usar un for para contar mayúsculas y minúsculas con comparaciones simples.
# Calcular si las mayúsculas superan el 50%.
# Si eso pasa, invertir el texto construyendo otro string letra por letra.
# Buscar manualmente las palabras clave en el post.
# Mostrar los resultados de cada post.

# --- RESUMEN --- ETAPA 2
# Usar pila para almacenar palabras decodificadas, ya sea por inversion o cosas como cifrado cesar de 1 a 5.
# Popear las que no sean validas para probar otras.
# Guardar logs en otro txt.

# --- BOCETO --- ETAPA 2
# Crear una pila para palabras ya decodificadas siempre y cuando sean validas como alertas.
# Crear el criterio de palabra decodificada y la forma cesar de decodificacion.
# Guardar logs en otro txt.

# --- RESUMEN --- ETAPA 3
# Crear una cola para procesar los posteos.
# Ordenar los posteos por puntaje de nivel de sospecha (cant. de alertas).
# Graficar linea de puntaje de nivel de sospecha con MatPlotLib.
# Filtrar ruido como emojis para darle coherencia al mensaje.

# --- BOCETO --- ETAPA 3
# Cola de procesamiento.
# Ordenar mediante linear sort por cantidad de alertas.
# Grafica de linea de puntaje de nivel de sospecha.
# Filtrar los emojis con condicionales.


def invertir_texto(texto):
    inverso = ""
    i = len(texto) - 1
    while i >= 0:
        inverso += texto[i]
        i -= 1
    return inverso


def separar_usuario_post(linea):
    usuario = ""
    post = ""
    i = 0
    encontrado_puntoycoma = False

    while i < len(linea):
        if linea[i] == ";" and encontrado_puntoycoma == False:
            encontrado_puntoycoma = True
        else:
            if encontrado_puntoycoma == False:
                usuario += linea[i]
            else:
                post += linea[i]
        i += 1

    return usuario, post


def limitar_140(texto):
    resultado = ""
    contador = 0

    for caracter in texto:
        if caracter != "\n":
            if contador < 140:
                resultado += caracter
                contador += 1

    return resultado


def contar_mayus_minus(texto):
    mayus = 0
    minus = 0

    for caracter in texto:
        if ("A" <= caracter <= "Z") or caracter == "Á" or caracter == "É" or caracter == "Í" or caracter == "Ó" or caracter == "Ú" or caracter == "Ñ":
            mayus += 1
        elif ("a" <= caracter <= "z") or caracter == "á" or caracter == "é" or caracter == "í" or caracter == "ó" or caracter == "ú" or caracter == "ñ":
            minus += 1

    return mayus, minus


def contiene_palabra_clave(texto):
    texto_minus = ""

    for caracter in texto:
        texto_minus += caracter.lower()

    if "secreto" in texto_minus or "conspiracion" in texto_minus or "conspiración" in texto_minus:
        return True
    return False


# ETAPA 2

class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if len(self.items) > 0:
            return self.items.pop()
        return None

    def is_empty(self):
        return len(self.items) == 0


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
            raise IndexError("Queue vacía")
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)


processing_queue = Queue()


def decodificar_cesar(texto, desplazamiento):
    alfabeto = "abcdefghijklmnopqrstuvwxyz"
    resultado = ""

    for caracter in texto:
        letra = caracter.lower()

        if letra in alfabeto:
            posicion = alfabeto.index(letra)
            nueva_pos = posicion - desplazamiento

            if nueva_pos < 0:
                nueva_pos = nueva_pos + 26

            nueva_letra = alfabeto[nueva_pos]

            if "A" <= caracter <= "Z":
                resultado += nueva_letra.upper()
            else:
                resultado += nueva_letra
        else:
            resultado += caracter

    return resultado


def contar_vocales(texto):
    contador = 0

    for caracter in texto.lower():
        if caracter == "a" or caracter == "e" or caracter == "i" or caracter == "o" or caracter == "u":
            contador += 1

    return contador


def probar_desplazamientos(post):
    historial = Stack()
    mejor_texto = ""
    mejor_shift = 0
    max_vocales = -1

    for desplazamiento in range(1, 6):
        decodificado = decodificar_cesar(post, desplazamiento)
        historial.push(decodificado)

        vocales = contar_vocales(decodificado)

        print("Shift:", desplazamiento)
        print("Decodificado:", decodificado)
        print("Vocales:", vocales)
        print("--------------------")

        if vocales > max_vocales:
            max_vocales = vocales
            mejor_texto = decodificado
            mejor_shift = desplazamiento

    return mejor_texto, mejor_shift, historial


def filtrar_ruido(texto):
    limpio = ""

    for caracter in texto:
        if (
            ("A" <= caracter <= "Z")
            or ("a" <= caracter <= "z")
            or ("0" <= caracter <= "9")
            or caracter == " "
            or caracter == ","
            or caracter == "."
            or caracter == ";"
            or caracter == ":"
            or caracter == "á"
            or caracter == "é"
            or caracter == "í"
            or caracter == "ó"
            or caracter == "ú"
            or caracter == "ñ"
            or caracter == "Á"
            or caracter == "É"
            or caracter == "Í"
            or caracter == "Ó"
            or caracter == "Ú"
            or caracter == "Ñ"
        ):
            limpio += caracter

    return limpio


def ordenar_por_sospecha(lista):
    n = len(lista)

    for i in range(n - 1):
        pos_max = i

        for j in range(i + 1, n):
            if lista[j][2] > lista[pos_max][2]:
                pos_max = j

        aux = lista[i]
        lista[i] = lista[pos_max]
        lista[pos_max] = aux


def graficar_scores(lista):
    x = []
    y = []

    i = 1
    for elemento in lista:
        x.append(i)
        y.append(elemento[2])
        i += 1

    plt.plot(x, y, marker="o")
    plt.title("Nivel de sospecha de los posts")
    plt.xlabel("Post")
    plt.ylabel("Score")
    plt.grid(True)
    plt.show()


with open("logs_decodificados.txt", "w", encoding="utf-8") as log:
    pass


with open("posteos.txt", "r", encoding="utf-8") as archivo:
    for linea in archivo:
        usuario, post = separar_usuario_post(linea)
        post = limitar_140(post)
        post = filtrar_ruido(post)
        processing_queue.enqueue([usuario, post])

alerta = 0
posts_con_score = []

while processing_queue.is_empty() == False:
    dato = processing_queue.dequeue()
    usuario = dato[0]
    post = dato[1]
    score = 0

    mayusculas, minusculas = contar_mayus_minus(post)

    print("Usuario:", usuario)
    print("Post original:", post)
    print("Mayúsculas:", mayusculas)
    print("Minúsculas:", minusculas)

    total_letras = mayusculas + minusculas

    if contiene_palabra_clave(post):
        print("ALERTA: palabra clave detectada en el post original")
        alerta += 1
        score += 1

    if total_letras > 0 and mayusculas > total_letras // 2:
        post_invertido = invertir_texto(post)
        print("Post sospechoso. Invertido:", post_invertido)
        score += 2

        if contiene_palabra_clave(post_invertido):
            print("ALERTA: palabra clave detectada en el post invertido")
            alerta += 1
            score += 1

        mejor_texto, mejor_shift, historial = probar_desplazamientos(post_invertido)

        print("Mejor decodificación:", mejor_texto)
        print("Shift usado:", mejor_shift)

        deshecho = historial.pop()
        print("Última decodificación quitada con pop():", deshecho)

        with open("logs_decodificados.txt", "a", encoding="utf-8") as log:
            log.write(post + "," + mejor_texto + "\n")

    posts_con_score.append([usuario, post, score])

    print("-" * 40)

print(f"Se detectaron {alerta} alertas.")

ordenar_por_sospecha(posts_con_score)

print("POSTS ORDENADOS POR NIVEL DE SOSPECHA:")
for elemento in posts_con_score:
    print("Usuario:", elemento[0], "- Score:", elemento[2], "- Post:", elemento[1])

graficar_scores(posts_con_score)