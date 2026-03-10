from typing import Iterable, List, Tuple, Optional
import random

def write_lines(nombre_archivo: str, lineas: Iterable[str], overwrite: bool = True) -> None:
    """Escribe una lista de líneas. Si overwrite=False, agrega al final."""
    modo = "w" if overwrite else "a"
    with open(nombre_archivo, modo, encoding="utf-8") as f:
        for linea in lineas:
            f.write(f"{linea}\n")

def read_lines(nombre_archivo: str) -> List[str]:
    """Lee todas las líneas (sin salto de línea final). Si no existe, levanta error del open."""
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        return [linea.rstrip("\n") for linea in f]

def append_line(nombre_archivo: str, linea: str) -> None:
    """Agrega UNA línea al final del archivo."""
    write_lines(nombre_archivo, [linea], overwrite=False)

def count_lines(nombre_archivo: str) -> int:
    return len(read_lines(nombre_archivo))

def search_text(nombre_archivo: str, query: str, case_sensitive: bool = False) -> List[Tuple[int, str]]:
    """Devuelve lista de (nro_linea, contenido) donde aparece query."""
    resultados: List[Tuple[int, str]] = []
    lineas = read_lines(nombre_archivo)
    if case_sensitive:
        for i, linea in enumerate(lineas, start=1):
            if query in linea:
                resultados.append((i, linea))
    else:
        q = query.lower()
        for i, linea in enumerate(lineas, start=1):
            if q in linea.lower():
                resultados.append((i, linea))
    return resultados

def leer_lineas(nombre_archivo):
    with open(nombre_archivo, "r") as f:
        return f.readlines()

def escribir_linea(nombre_archivo, texto):
    with open(nombre_archivo, "a") as f:
        f.write(texto + "\n")

# Guardar lista de objetos en texto
def guardar_lista(nombre_archivo, lista):
    with open(nombre_archivo, "w") as f:
        for alumno in lista:
            f.write(str(alumno) + "\n")

# Cargar lista de objetos desde texto
def cargar_lista(nombre_archivo):
    lista = []
    with open(nombre_archivo, "r") as f:
        for linea in f:
            leg, nom, nota = linea.strip().split(",")
            #alumno = clase_alumno(leg, nom, nota)
            #lista.append(alumno)
    return lista

# Leer todo junto
# with open("datos.txt", "r") as f:
  #  contenido = f.read()
  #  print("LECTURA COMPLETA:")
  #  print(contenido)

# Leer línea por línea (muy usado para procesar datos)
# with open("datos.txt", "r") as f:
  #  for linea in f:
  #      print("LINEA:", linea.strip())

def write_numbers(nombre_archivo: str, numeros: Iterable[float], overwrite: bool = True) -> None:
    write_lines(nombre_archivo, (str(n) for n in numeros), overwrite=overwrite)

def read_numbers(nombre_archivo: str) -> List[float]:
    """Lee números (float) desde un .txt con un número por línea. Ignora líneas no numéricas."""
    numeros: List[float] = []
    for linea in read_lines(nombre_archivo):
        s = linea.strip()
        if not s:
            continue
        try:
            numeros.append(float(s))
        except ValueError:
            # Ignora líneas no válidas para ser tolerante
            pass
    return numeros

def sum_and_avg_numbers(nombre_archivo: str) -> Tuple[float, Optional[float]]:
    nums = read_numbers(nombre_archivo)
    if not nums:
        return 0.0, None
    total = sum(nums)
    return total, total / len(nums)

def count_value_in_file(nombre_archivo: str, valor: float) -> int:
    """Cuenta cuántas veces aparece EXACTAMENTE "valor" en el archivo de números."""
    return sum(1 for n in read_numbers(nombre_archivo) if n == valor)

def generate_random_numbers_file(nombre_archivo: str, n: int, low: int = 1, high: int = 100, overwrite: bool = True) -> None:
    rng = random.Random()
    numeros = (rng.randint(low, high) for _ in range(n))
    write_numbers(nombre_archivo, numeros, overwrite=overwrite)

def archivo_palabras_demo(nombre_archivo: str) -> None:
    write_lines(nombre_archivo, ["manzana", "pera", "uva", "banana"], overwrite=True)
    print("Palabras:", read_lines(nombre_archivo))
    print("Total de líneas:", count_lines(nombre_archivo))
    print("Buscar 'na':", search_text(nombre_archivo, "na"))

def archivo_numeros_demo(nombre_archivo: str) -> None:
    generate_random_numbers_file(nombre_archivo, n=10, low=1, high=10, overwrite=True)
    total, promedio = sum_and_avg_numbers(nombre_archivo)
    print("Suma y promedio:", total, promedio)
    print("Cantidad de 5:", count_value_in_file(nombre_archivo, 5))

if __name__ == "__main__":
    # 1) Texto
    archivo_palabras_demo("palabras.txt")

    # 2) Números
    archivo_numeros_demo("numeros.txt")

    # 3) Operaciones sencillas extra
    write_lines("colores.txt", ["rojo", "verde", "azul"], overwrite=True)
    append_line("colores.txt", "amarillo")
    print("Colores:", read_lines("colores.txt"))
    print("Buscar 'ver':", search_text("colores.txt", "ver"))