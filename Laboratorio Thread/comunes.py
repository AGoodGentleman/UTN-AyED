"""Funciones comunes para el laboratorio de procesos e hilos.

El objetivo de este archivo es evitar repetir la misma logica en las
tres versiones del programa. Asi, la comparacion mide el mecanismo de
ejecucion (secuencial, hilos o procesos) y no cambios accidentales en
el algoritmo usado para contar primos.
"""

from __future__ import annotations

from time import perf_counter
from typing import Callable


# Rango propuesto por el enunciado del laboratorio.
# La funcion range(inicio, fin) incluye inicio y excluye fin.
RANGO_INICIO = 10_000_000
RANGO_FIN = 10_100_000


def es_primo(n: int) -> bool:
    """Devuelve True si n es primo usando division por tentativa.

    Esta funcion es intencionalmente CPU-bound: trabaja haciendo calculo
    aritmetico puro, sin esperar red, disco ni entrada/salida. Por eso
    sirve para observar el efecto del GIL en threading.
    """
    if n < 2:
        return False

    if n % 2 == 0:
        return n == 2

    # Si n tiene un divisor, alcanza con buscarlo hasta sqrt(n).
    # Probamos solo impares porque los pares ya fueron descartados.
    limite = int(n**0.5) + 1
    for divisor in range(3, limite, 2):
        if n % divisor == 0:
            return False

    return True


def contar_primos_en_rango(inicio: int, fin: int) -> int:
    """Cuenta cuantos primos hay en el intervalo [inicio, fin)."""
    return sum(1 for numero in range(inicio, fin) if es_primo(numero))


def dividir_rango(inicio: int, fin: int, partes: int) -> list[tuple[int, int]]:
    """Divide [inicio, fin) en sub-rangos lo mas parejos posible.

    Si el total no es divisible exacto, los primeros sub-rangos reciben
    un numero extra. Esto evita perder numeros al repartir el trabajo.
    """
    if partes < 1:
        raise ValueError("La cantidad de partes debe ser al menos 1.")

    total = fin - inicio
    if total <= 0:
        raise ValueError("El fin del rango debe ser mayor que el inicio.")

    # En pruebas chicas no tiene sentido crear mas trabajadores que numeros.
    partes_reales = min(partes, total)
    tam_base, sobrante = divmod(total, partes_reales)

    rangos: list[tuple[int, int]] = []
    actual = inicio
    for indice in range(partes_reales):
        extra = 1 if indice < sobrante else 0
        siguiente = actual + tam_base + extra
        rangos.append((actual, siguiente))
        actual = siguiente

    return rangos


def medir(funcion: Callable[[], int]) -> tuple[int, float]:
    """Ejecuta una funcion de conteo y devuelve resultado y segundos."""
    inicio_tiempo = perf_counter()
    cantidad_primos = funcion()
    fin_tiempo = perf_counter()
    return cantidad_primos, fin_tiempo - inicio_tiempo


def imprimir_resultado(nombre: str, primos: int, segundos: float, trabajadores: int) -> None:
    """Muestra una medicion con un formato consistente."""
    print(f"Version: {nombre}")
    print(f"Trabajadores usados: {trabajadores}")
    print(f"Primos encontrados: {primos}")
    print(f"Tiempo: {segundos:.4f} s")
