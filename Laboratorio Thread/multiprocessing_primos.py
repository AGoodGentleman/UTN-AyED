"""Version multiproceso del laboratorio usando multiprocessing.Process.

Cada proceso tiene su propio interprete de Python y su propio GIL. Por
eso, para un problema CPU-bound como este, multiprocessing si puede
aprovechar varios nucleos de CPU.
"""

from __future__ import annotations

import argparse
import multiprocessing

from comunes import (
    RANGO_FIN,
    RANGO_INICIO,
    contar_primos_en_rango,
    dividir_rango,
    imprimir_resultado,
    medir,
)


def contar_primos_proceso(inicio: int, fin: int, cola: multiprocessing.Queue) -> None:
    """Cuenta primos en un sub-rango y envia el parcial por una Queue.

    Los procesos no comparten memoria como los hilos. La cola es un
    mecanismo de IPC: permite que un proceso hijo le mande datos al padre.
    """
    total = contar_primos_en_rango(inicio, fin)
    cola.put(total)


def ejecutar(
    inicio: int = RANGO_INICIO,
    fin: int = RANGO_FIN,
    cantidad_procesos: int | None = None,
) -> tuple[int, float, int]:
    """Ejecuta el conteo con procesos y devuelve (cantidad, segundos, procesos)."""
    if cantidad_procesos is None:
        cantidad_procesos = multiprocessing.cpu_count()

    rangos = dividir_rango(inicio, fin, cantidad_procesos)
    cola: multiprocessing.Queue = multiprocessing.Queue()
    procesos: list[multiprocessing.Process] = []

    def trabajo_completo() -> int:
        for indice, (sub_inicio, sub_fin) in enumerate(rangos):
            proceso = multiprocessing.Process(
                target=contar_primos_proceso,
                args=(sub_inicio, sub_fin, cola),
                name=f"ContadorPrimos-{indice + 1}",
            )
            procesos.append(proceso)
            proceso.start()

        # El enunciado recomienda leer la Queue antes de join().
        # Con datos grandes, un hijo podria bloquearse si la cola se llena
        # y el padre todavia no esta consumiendo resultados.
        resultados = [cola.get() for _ in procesos]

        for proceso in procesos:
            proceso.join()
            if proceso.exitcode != 0:
                raise RuntimeError(f"El proceso {proceso.name} termino con exitcode {proceso.exitcode}.")

        return sum(resultados)

    primos, segundos = medir(trabajo_completo)
    return primos, segundos, len(rangos)


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Cuenta primos usando multiprocessing.Process.")
    parser.add_argument("--inicio", type=int, default=RANGO_INICIO, help="Inicio del rango incluido.")
    parser.add_argument("--fin", type=int, default=RANGO_FIN, help="Fin del rango excluido.")
    parser.add_argument(
        "--procesos",
        type=int,
        default=multiprocessing.cpu_count(),
        help="Cantidad de procesos a crear. Por defecto usa todos los CPU logicos.",
    )
    return parser


def main() -> None:
    args = construir_parser().parse_args()
    primos, segundos, procesos_usados = ejecutar(args.inicio, args.fin, args.procesos)

    print(f"Rango evaluado: [{args.inicio}, {args.fin})")
    print(f"CPU logicos detectados: {multiprocessing.cpu_count()}")
    imprimir_resultado("multiprocessing", primos, segundos, trabajadores=procesos_usados)


if __name__ == "__main__":
    # Necesario en Windows porque multiprocessing usa spawn: el proceso hijo
    # vuelve a importar este archivo y no debe crear procesos recursivamente.
    main()
