"""Ejecuta las tres versiones y arma la tabla comparativa del laboratorio."""

from __future__ import annotations

import argparse
import multiprocessing

from comunes import RANGO_FIN, RANGO_INICIO
from multiprocessing_primos import ejecutar as ejecutar_multiprocessing
from secuencial import ejecutar as ejecutar_secuencial
from threading_primos import ejecutar as ejecutar_threading


def calcular_speedup(tiempo_base: float, tiempo_version: float) -> float:
    """Speedup = tiempo secuencial / tiempo de la version comparada."""
    return tiempo_base / tiempo_version


def imprimir_tabla(filas: list[tuple[str, int, int, float, float]]) -> None:
    """Imprime una tabla en formato Markdown para copiar al informe."""
    print("| Version | Trabajadores | Primos encontrados | Tiempo (s) | Speedup |")
    print("|---|---:|---:|---:|---:|")
    for nombre, trabajadores, primos, segundos, speedup in filas:
        print(f"| {nombre} | {trabajadores} | {primos} | {segundos:.4f} | {speedup:.2f}x |")


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Compara secuencial, threading y multiprocessing.")
    parser.add_argument("--inicio", type=int, default=RANGO_INICIO, help="Inicio del rango incluido.")
    parser.add_argument("--fin", type=int, default=RANGO_FIN, help="Fin del rango excluido.")
    parser.add_argument("--hilos", type=int, default=4, help="Cantidad de hilos para threading.")
    parser.add_argument(
        "--procesos",
        type=int,
        default=multiprocessing.cpu_count(),
        help="Cantidad de procesos para multiprocessing.",
    )
    return parser


def main() -> None:
    args = construir_parser().parse_args()

    print(f"Rango evaluado: [{args.inicio}, {args.fin})")
    print(f"CPU logicos detectados: {multiprocessing.cpu_count()}")
    print()

    primos_sec, tiempo_sec = ejecutar_secuencial(args.inicio, args.fin)
    primos_thr, tiempo_thr, hilos_usados = ejecutar_threading(args.inicio, args.fin, args.hilos)
    primos_mp, tiempo_mp, procesos_usados = ejecutar_multiprocessing(args.inicio, args.fin, args.procesos)

    if len({primos_sec, primos_thr, primos_mp}) != 1:
        raise RuntimeError(
            "Las versiones no encontraron la misma cantidad de primos. "
            "Revisar la division de rangos."
        )

    filas = [
        ("Secuencial", 1, primos_sec, tiempo_sec, 1.0),
        ("Threading", hilos_usados, primos_thr, tiempo_thr, calcular_speedup(tiempo_sec, tiempo_thr)),
        (
            "Multiprocessing",
            procesos_usados,
            primos_mp,
            tiempo_mp,
            calcular_speedup(tiempo_sec, tiempo_mp),
        ),
    ]

    imprimir_tabla(filas)
    print()
    print("Conclusion sugerida:")
    print(
        "En una tarea CPU-bound, threading no mejora mucho porque los hilos comparten el GIL "
        "y solo uno ejecuta bytecode Python a la vez. Multiprocessing crea procesos separados, "
        "cada uno con su propio interprete y su propio GIL, por eso puede repartir el calculo "
        "entre nucleos. Si el rango es chico o se crean demasiados procesos, el costo de spawn "
        "y comunicacion puede reducir o incluso ocultar esa mejora."
    )


if __name__ == "__main__":
    main()
