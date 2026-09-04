"""Genera una imagen PNG con la tabla de resultados del laboratorio."""

from __future__ import annotations

import argparse
import multiprocessing
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from comunes import RANGO_FIN, RANGO_INICIO
from ejecutar_comparacion import calcular_speedup
from multiprocessing_primos import ejecutar as ejecutar_multiprocessing
from secuencial import ejecutar as ejecutar_secuencial
from threading_primos import ejecutar as ejecutar_threading


ANCHO = 1400
ALTO = 820
MARGEN = 70


def fuente(tamano: int, negrita: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Carga una fuente del sistema o usa la fuente basica si no existe."""
    posibles_fuentes = [
        r"C:\Windows\Fonts\segoeuib.ttf" if negrita else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if negrita else r"C:\Windows\Fonts\arial.ttf",
    ]

    for ruta in posibles_fuentes:
        if Path(ruta).exists():
            return ImageFont.truetype(ruta, tamano)

    return ImageFont.load_default()


def texto_centrado(
    dibujo: ImageDraw.ImageDraw,
    caja: tuple[int, int, int, int],
    texto: str,
    font: ImageFont.ImageFont,
    color: tuple[int, int, int],
) -> None:
    """Dibuja texto centrado dentro de una caja."""
    izquierda, arriba, derecha, abajo = caja
    bbox = dibujo.textbbox((0, 0), texto, font=font)
    ancho_texto = bbox[2] - bbox[0]
    alto_texto = bbox[3] - bbox[1]
    x = izquierda + (derecha - izquierda - ancho_texto) / 2
    y = arriba + (abajo - arriba - alto_texto) / 2 - 2
    dibujo.text((x, y), texto, font=font, fill=color)


def dibujar_tabla(
    dibujo: ImageDraw.ImageDraw,
    filas: list[list[str]],
    x: int,
    y: int,
    anchos: list[int],
    alto_fila: int,
) -> None:
    """Dibuja una tabla simple con encabezado destacado."""
    color_borde = (214, 224, 236)
    color_encabezado = (32, 74, 115)
    color_encabezado_texto = (255, 255, 255)
    color_texto = (33, 42, 53)
    color_fila_par = (245, 248, 252)
    color_fila_impar = (255, 255, 255)

    font_header = fuente(28, negrita=True)
    font_body = fuente(27)

    posicion_y = y
    for indice_fila, fila in enumerate(filas):
        posicion_x = x
        fondo = color_encabezado if indice_fila == 0 else color_fila_par if indice_fila % 2 == 0 else color_fila_impar
        texto_color = color_encabezado_texto if indice_fila == 0 else color_texto
        font = font_header if indice_fila == 0 else font_body

        for indice_columna, celda in enumerate(fila):
            caja = (
                posicion_x,
                posicion_y,
                posicion_x + anchos[indice_columna],
                posicion_y + alto_fila,
            )
            dibujo.rounded_rectangle(caja, radius=0, fill=fondo, outline=color_borde, width=1)
            texto_centrado(dibujo, caja, celda, font, texto_color)
            posicion_x += anchos[indice_columna]

        posicion_y += alto_fila


def crear_png(
    salida: Path,
    inicio: int,
    fin: int,
    hilos: int,
    procesos: int,
) -> None:
    """Ejecuta las mediciones y guarda la tabla como PNG."""
    primos_sec, tiempo_sec = ejecutar_secuencial(inicio, fin)
    primos_thr, tiempo_thr, hilos_usados = ejecutar_threading(inicio, fin, hilos)
    primos_mp, tiempo_mp, procesos_usados = ejecutar_multiprocessing(inicio, fin, procesos)

    if len({primos_sec, primos_thr, primos_mp}) != 1:
        raise RuntimeError("Las tres versiones no encontraron la misma cantidad de primos.")

    filas = [
        ["Version", "Trabajadores", "Primos", "Tiempo (s)", "Speedup"],
        ["Secuencial", "1", str(primos_sec), f"{tiempo_sec:.4f}", "1.00x"],
        ["Threading", str(hilos_usados), str(primos_thr), f"{tiempo_thr:.4f}", f"{calcular_speedup(tiempo_sec, tiempo_thr):.2f}x"],
        ["Multiprocessing", str(procesos_usados), str(primos_mp), f"{tiempo_mp:.4f}", f"{calcular_speedup(tiempo_sec, tiempo_mp):.2f}x"],
    ]

    imagen = Image.new("RGB", (ANCHO, ALTO), (239, 244, 249))
    dibujo = ImageDraw.Draw(imagen)

    # Fondo con una banda superior sobria para que la tabla se vea presentable.
    dibujo.rectangle((0, 0, ANCHO, 230), fill=(20, 54, 89))
    dibujo.rounded_rectangle((MARGEN, 150, ANCHO - MARGEN, ALTO - 70), radius=26, fill=(255, 255, 255))

    dibujo.text((MARGEN, 54), "Laboratorio Thread", font=fuente(54, negrita=True), fill=(255, 255, 255))
    dibujo.text(
        (MARGEN, 115),
        "Comparacion de rendimiento: secuencial vs threading vs multiprocessing",
        font=fuente(25),
        fill=(213, 227, 242),
    )

    subtitulo = f"Rango [{inicio:,}, {fin:,})  |  CPU logicos: {multiprocessing.cpu_count()}"
    subtitulo = subtitulo.replace(",", ".")
    dibujo.text((MARGEN + 34, 195), subtitulo, font=fuente(27, negrita=True), fill=(42, 55, 69))

    dibujar_tabla(
        dibujo,
        filas,
        x=MARGEN + 34,
        y=260,
        anchos=[330, 250, 190, 220, 220],
        alto_fila=82,
    )

    nota = (
        "Speedup = T_secuencial / T_version. "
        "En Windows, el costo de crear procesos puede pesar si el rango es pequeno."
    )
    dibujo.text((MARGEN + 34, 640), nota, font=fuente(23), fill=(92, 104, 119))

    salida.parent.mkdir(parents=True, exist_ok=True)
    imagen.save(salida)


def construir_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Genera una tabla PNG con resultados del laboratorio.")
    parser.add_argument("--inicio", type=int, default=RANGO_INICIO, help="Inicio del rango incluido.")
    parser.add_argument("--fin", type=int, default=RANGO_FIN, help="Fin del rango excluido.")
    parser.add_argument("--hilos", type=int, default=4, help="Cantidad de hilos para threading.")
    parser.add_argument("--procesos", type=int, default=multiprocessing.cpu_count(), help="Cantidad de procesos.")
    parser.add_argument("--salida", type=Path, default=Path("tabla_resultados.png"), help="Archivo PNG a crear.")
    return parser


def main() -> None:
    args = construir_parser().parse_args()
    crear_png(args.salida, args.inicio, args.fin, args.hilos, args.procesos)
    print(f"PNG generado: {args.salida.resolve()}")


if __name__ == "__main__":
    main()
