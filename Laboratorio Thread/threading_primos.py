"""Version multihilo del laboratorio usando threading.Thread.

Para este problema CPU-bound no se espera una mejora importante porque
los hilos comparten el mismo interprete CPython y el mismo GIL. Aun asi,
el programa sirve para medirlo empiricamente.
"""

from __future__ import annotations

import argparse
import threading

from comunes import (
    RANGO_FIN,
    RANGO_INICIO,
    contar_primos_en_rango,
    dividir_rango,
    imprimir_resultado,
    medir,
)


def contar_primos_hilo(inicio: int, fin: int, resultados: list[int], indice: int) -> None:
    """Cuenta primos en un sub-rango y guarda el parcial.

    Cada hilo escribe en una posicion distinta de la lista. Por eso, en
    este ejercicio, no necesitamos un Lock para proteger una suma global.
    """
    resultados[indice] = contar_primos_en_rango(inicio, fin)


def ejecutar(
    inicio: int = RANGO_INICIO,
    fin: int = RANGO_FIN,
    cantidad_hilos: int = 4,
) -> tuple[int, float, int]:
    """Ejecuta el conteo con hilos y devuelve (cantidad, segundos, hilos)."""
    rangos = dividir_rango(inicio, fin, cantidad_hilos)
    resultados = [0] * len(rangos)
    hilos: list[threading.Thread] = []

    def trabajo_completo() -> int:
        for indice, (sub_inicio, sub_fin) in enumerate(rangos):
            hilo = threading.Thread(
                target=contar_primos_hilo,
                args=(sub_inicio, sub_fin, resultados, indice),
                name=f"ContadorPrimos-{indice + 1}",
            )
            hilos.append(hilo)
            hilo.start()

        # Primero se lanzan todos los hilos; despues se esperan todos.
        # Si hicieramos start() y join() dentro del mismo bucle, quedaria
        # una ejecucion practicamente secuencial.
        for hilo in hilos:
            hilo.join()

        return sum(resultados)

    primos, segundos = medir(trabajo_completo)
    return primos, segundos, len(rangos)


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cuenta primos usando threading.Thread.")
    parser.add_argument("--inicio", type=int, default=RANGO_INICIO, help="Inicio del rango incluido.")
    parser.add_argument("--fin", type=int, default=RANGO_FIN, help="Fin del rango excluido.")
    parser.add_argument("--hilos", type=int, default=4, help="Cantidad de hilos a crear.")
    return parser


def main() -> None:
    args = construir_parser().parse_args()
    primos, segundos, hilos_usados = ejecutar(args.inicio, args.fin, args.hilos)

    print(f"Rango evaluado: [{args.inicio}, {args.fin})")
    imprimir_resultado("threading", primos, segundos, trabajadores=hilos_usados)


if __name__ == "__main__":
    main()
