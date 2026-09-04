"""Version secuencial del laboratorio.

Esta es la linea base: un unico flujo de ejecucion recorre todo el rango
y cuenta primos. Los tiempos de threading y multiprocessing se comparan
contra esta medicion.
"""

from __future__ import annotations

import argparse

from comunes import RANGO_FIN, RANGO_INICIO, contar_primos_en_rango, imprimir_resultado, medir


def ejecutar(inicio: int = RANGO_INICIO, fin: int = RANGO_FIN) -> tuple[int, float]:
    """Cuenta primos en un solo hilo y devuelve (cantidad, segundos)."""
    return medir(lambda: contar_primos_en_rango(inicio, fin))


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cuenta primos de forma secuencial.")
    parser.add_argument("--inicio", type=int, default=RANGO_INICIO, help="Inicio del rango incluido.")
    parser.add_argument("--fin", type=int, default=RANGO_FIN, help="Fin del rango excluido.")
    return parser


def main() -> None:
    args = construir_parser().parse_args()
    primos, segundos = ejecutar(args.inicio, args.fin)

    print(f"Rango evaluado: [{args.inicio}, {args.fin})")
    imprimir_resultado("secuencial", primos, segundos, trabajadores=1)


if __name__ == "__main__":
    main()
