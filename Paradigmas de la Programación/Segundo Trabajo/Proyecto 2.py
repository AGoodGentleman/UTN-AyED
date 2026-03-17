# import matplotlib.pyplot as plt

# --- Boceto --- Etapa 1
# Crear Clase DiarioViajero(texto)
# Añadir métodos para encriptar o desencriptar secciones (sustitución simple o césar)
# Crear Pila para para deshacer cambios
# Hacer Menú: Cargar Diario, Analizar (Leer el texto destacando strings sospechosos), Encriptar, Desencriptar, Deshacer, Salir.

# --- Boceto --- Etapa 2
# Crear Cola para entradas diarias
# Crear Subclase DiarioSecreto(texto)
# Guardar logs y diarios en txt y que estos persistan

# --- Boceto --- Etapa 3
# Ordenar palabras por frecuencia, como método dentro de Analizar(), con algoritmos de ordenamiento
# Gráficos de líneas con matplotlib
# Detectar acrósticos

# Autor: Valentín Blazquez


class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("No hay cambios para deshacer.")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("La pila está vacía.")
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("No hay entradas en la cola.")
        return self.items.pop(0)

    def front(self):
        if self.is_empty():
            raise IndexError("No hay entradas en la cola.")
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)


class DiarioViajero:
    def __init__(self, texto=""):
        self.texto = texto
        self.historial = Stack()

    def cargar_texto(self, texto):
        self.texto = texto
        self.historial = Stack()

    def mostrar_texto(self):
        return self.texto

    def analizar(self):
        if self.texto == "":
            print("No hay diario cargado.")
            return

        letras = {}
        cantidad_letras = 0
        palabras = {}
        palabra_actual = ""

        for caracter in self.texto.lower():
            if caracter.isalpha():
                cantidad_letras += 1

                if caracter in letras:
                    letras[caracter] += 1
                else:
                    letras[caracter] = 1

                palabra_actual += caracter
            else:
                if palabra_actual != "":
                    if palabra_actual in palabras:
                        palabras[palabra_actual] += 1
                    else:
                        palabras[palabra_actual] = 1
                    palabra_actual = ""

        if palabra_actual != "":
            if palabra_actual in palabras:
                palabras[palabra_actual] += 1
            else:
                palabras[palabra_actual] = 1

        print("\n--- Análisis del diario ---")
        print("Texto actual:")
        print(self.texto)
        print(f"\nCantidad total de letras: {cantidad_letras}")

        print("\nFrecuencia de letras:")
        for letra in letras:
            print(f"{letra}: {letras[letra]}")

        sospechosas = ["secreto", "clave", "oculto", "misterio", "conspiracion"]
        encontradas = []

        texto_minuscula = self.texto.lower()
        for palabra in sospechosas:
            if palabra in texto_minuscula:
                encontradas.append(palabra)

        if len(encontradas) > 0:
            print("\nPalabras sospechosas detectadas:")
            for palabra in encontradas:
                print(f"- {palabra}")
        else:
            print("\nNo se detectaron palabras sospechosas.")

        palabras_ordenadas = self._ordenar_frecuencias(palabras)

        print("\nPalabras ordenadas por frecuencia:")
        for palabra, frecuencia in palabras_ordenadas:
            print(f"{palabra}: {frecuencia}")

        acrostico = self.detectar_acrostico()
        if acrostico != "":
            print(f"\nPosible acróstico detectado: {acrostico}")
        else:
            print("\nNo se detectó acróstico.")

    def detectar_acrostico(self):
        if self.texto.strip() == "":
            return ""

        lineas = self.texto.split("\n")
        acrostico = ""

        for linea in lineas:
            linea = linea.strip()
            if linea != "":
                acrostico += linea[0].upper()

        return acrostico

    def _ordenar_frecuencias(self, diccionario):
        lista = []

        for clave in diccionario:
            lista.append((clave, diccionario[clave]))

        n = len(lista)

        for i in range(n):
            for j in range(0, n - i - 1):
                if lista[j][1] < lista[j + 1][1]:
                    aux = lista[j]
                    lista[j] = lista[j + 1]
                    lista[j + 1] = aux

        return lista

    def graficar_frecuencias(self):
        if self.texto == "":
            print("No hay diario cargado.")
            return

        letras = {}

        for caracter in self.texto.lower():
            if caracter.isalpha():
                if caracter in letras:
                    letras[caracter] += 1
                else:
                    letras[caracter] = 1

        letras_ordenadas = []
        frecuencias = []

        for letra in letras:
            letras_ordenadas.append(letra)
            frecuencias.append(letras[letra])

        plt.figure(figsize=(10, 5))
        plt.plot(letras_ordenadas, frecuencias, marker="o")
        plt.title("Frecuencia de letras en el diario")
        plt.xlabel("Letras")
        plt.ylabel("Frecuencia")
        plt.grid(True)
        plt.show()

    def encriptar(self, desplazamiento):
        if self.texto == "":
            print("No hay texto actual cargado.")
            return

        self.historial.push(self.texto)
        self.texto = self._cifrado_cesar(self.texto, desplazamiento)
        print("\nTexto encriptado correctamente.")
        print(self.texto)

    def revelar(self, desplazamiento):
        if self.texto == "":
            print("No hay texto actual cargado.")
            return

        self.historial.push(self.texto)
        self.texto = self._cifrado_cesar(self.texto, -desplazamiento)
        print("\nTexto revelado correctamente.")
        print(self.texto)

    def deshacer(self):
        if self.historial.is_empty():
            print("Error: no hay cambios para deshacer.")
            return

        self.texto = self.historial.pop()
        print("\nSe deshizo el último cambio.")
        print(self.texto)

    def _cifrado_cesar(self, texto, desplazamiento):
        abecedario = "abcdefghijklmnñopqrstuvwxyz"
        resultado = ""

        for caracter in texto:
            if caracter.lower() in abecedario:
                es_mayuscula = caracter.isupper()
                posicion = abecedario.index(caracter.lower())
                nueva_posicion = (posicion + desplazamiento) % len(abecedario)
                nueva_letra = abecedario[nueva_posicion]

                if es_mayuscula:
                    resultado += nueva_letra.upper()
                else:
                    resultado += nueva_letra
            else:
                resultado += caracter

        return resultado


class DiarioSecreto(DiarioViajero):
    def __init__(self, texto="", archivo="diarios.txt"):
        super().__init__(texto)
        self.archivo = archivo
        self.entradas = Queue()

    def cargar_desde_archivo(self):
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                contenido = f.read().strip()

                if contenido != "":
                    partes = contenido.split(";")
                    for entrada in partes:
                        entrada_limpia = entrada.strip()
                        if entrada_limpia != "":
                            self.entradas.enqueue(entrada_limpia)

            print("Entradas cargadas desde diarios.txt correctamente.")

        except FileNotFoundError:
            print("No existe diarios.txt. Se creará al salir.")

    def guardar_en_archivo(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            textos = []

            if self.texto.strip() != "":
                textos.append(self.texto)

            for entrada in self.entradas.items:
                textos.append(entrada)

            f.write(";".join(textos))

        print("Entradas guardadas en diarios.txt correctamente.")

    def agregar_entrada(self, texto):
        self.entradas.enqueue(texto)
        print("Entrada agregada a la cola correctamente.")

    def procesar_siguiente_entrada(self):
        if self.entradas.is_empty():
            print("No hay entradas pendientes en la cola.")
            return

        self.texto = self.entradas.dequeue()
        self.historial = Stack()
        print("\nSe cargó la siguiente entrada como texto actual:")
        print(self.texto)

    def mostrar_cola(self):
        if self.entradas.is_empty():
            print("La cola de entradas está vacía.")
            return

        print("\n--- Entradas pendientes en la cola ---")
        for i in range(len(self.entradas.items)):
            print(f"{i + 1}. {self.entradas.items[i]}")

diario = DiarioSecreto()
diario.cargar_desde_archivo()

option = -1

while option != 0:
    print("\n==============================")
    print("   DIARIO VIAJERO SECRETO")
    print("   Autor: Valentín Blazquez")
    print("==============================")
    print("1. Agregar entrada a la cola")
    print("2. Procesar siguiente entrada")
    print("3. Analizar texto actual")
    print("4. Encriptar texto actual")
    print("5. Revelar texto actual")
    print("6. Deshacer")
    print("7. Mostrar cola")
    print("8. Graficar frecuencias")
    print("9. Detectar acróstico")
    print("0. Salir")

    try:
        option = int(input("Seleccione una opción: "))
    except ValueError:
        print("Debe ingresar un número válido.")
        continue

    if option == 1:
        texto = input("Ingrese una nueva entrada del diario: ")
        diario.agregar_entrada(texto)

    elif option == 2:
        diario.procesar_siguiente_entrada()

    elif option == 3:
        diario.analizar()

    elif option == 4:
        try:
            clave = int(input("Ingrese una clave de desplazamiento (1 a 26): "))
            if 1 <= clave <= 26:
                diario.encriptar(clave)
            else:
                print("La clave debe estar entre 1 y 26.")
        except ValueError:
            print("Debe ingresar un número entero.")

    elif option == 5:
        try:
            clave = int(input("Ingrese la clave usada para revelar (1 a 26): "))
            if 1 <= clave <= 26:
                diario.revelar(clave)
            else:
                print("La clave debe estar entre 1 y 26.")
        except ValueError:
            print("Debe ingresar un número entero.")

    elif option == 6:
        diario.deshacer()

    elif option == 7:
        diario.mostrar_cola()

    elif option == 8:
        diario.graficar_frecuencias()

    elif option == 9:
        acrostico = diario.detectar_acrostico()
        if acrostico != "":
            print(f"Posible acróstico detectado: {acrostico}")
        else:
            print("No se detectó acróstico.")

    elif option == 0:
        diario.guardar_en_archivo()
        print("Adiós.")

    else:
        print("No ha seleccionado una opción válida.")