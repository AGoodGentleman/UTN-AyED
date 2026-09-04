"""Graficos del Taller 04 - Introduccion a campos escalares.

El script genera los graficos pedidos en los ejercicios obligatorios
del 1 al 17. Los ejercicios que no piden grafico directo se omiten,
salvo algunos conjuntos geometricos incluidos como apoyo visual.

Uso rapido:
    py taller_04_graficos_obligatorios.py --guardar
    py taller_04_graficos_obligatorios.py --ejercicio 4 12 16 --guardar
    py taller_04_graficos_obligatorios.py --listar
"""

from __future__ import annotations

import argparse
import importlib
import math
import subprocess
import sys
from pathlib import Path

np = None
plt = None


DEFAULT_OUTPUT_DIR = Path(__file__).with_name("graficos_taller_04")
VISTA_ELEV = 24
VISTA_AZIM = -60
COLOR_EJE = "#ff1493"
MOSTRAR_TICKS_EJES_3D = True
MAX_TICKS_EJES_3D = 7
COLOR_PISO = "tab:green"
COLOR_PARED = "tab:blue"
COLOR_PARED_2 = "tab:orange"
COLOR_BORDE = "tab:green"
COLOR_CURVA = "navy"
COLOR_PUNTO = "crimson"
COLOR_SUPERFICIE = "tab:blue"


def importar_o_instalar(modulo, paquete=None):
    paquete = paquete or modulo

    try:
        return importlib.import_module(modulo)
    except ModuleNotFoundError:
        print(f"No se encontro {modulo}. Instalando {paquete}...")

    comando = [sys.executable, "-m", "pip", "install", paquete]
    resultado = subprocess.run(comando, check=False)
    if resultado.returncode != 0:
        print(
            f"No se pudo instalar {paquete}. "
            f"Proba manualmente con: {sys.executable} -m pip install {paquete}"
        )
        raise SystemExit(resultado.returncode)

    try:
        return importlib.import_module(modulo)
    except ModuleNotFoundError:
        print(f"{paquete} se instalo, pero Python no pudo importar {modulo}.")
        raise SystemExit(1)


def cargar_dependencias(modo_guardar=False) -> None:
    global np, plt

    numpy_mod = importar_o_instalar("numpy")
    matplotlib = importar_o_instalar("matplotlib")

    if modo_guardar:
        matplotlib.use("Agg")

    pyplot_mod = importar_o_instalar("matplotlib.pyplot", "matplotlib")

    np = numpy_mod
    plt = pyplot_mod


def configurar_estilo() -> None:
    plt.rcParams.update(
        {
            "figure.constrained_layout.use": True,
            "axes.grid": True,
            "grid.alpha": 0.25,
            "axes.titlesize": 10,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
        }
    )


def configurar_2d(ax, titulo, xlim=(-5, 5), ylim=(-5, 5), igual=True):
    ax.set_title(titulo)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axhline(0, color="0.25", linewidth=0.8)
    ax.axvline(0, color="0.25", linewidth=0.8)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    if igual:
        ax.set_aspect("equal", adjustable="box")


def centrar_limite_en_origen(limite):
    extremo = max(abs(limite[0]), abs(limite[1]))
    if extremo == 0:
        extremo = 1
    return (-extremo, extremo)


def ajustar_limite_z(limite):
    inferior, superior = limite
    if inferior >= 0:
        return (0, superior if superior > 0 else 1)
    if superior <= 0:
        return (inferior if inferior < 0 else -1, 0)
    extremo = max(abs(inferior), abs(superior))
    return (-extremo, extremo)


def limites_con_origen_central(xlim, ylim, zlim):
    return (
        centrar_limite_en_origen(xlim),
        centrar_limite_en_origen(ylim),
        ajustar_limite_z(zlim),
    )


def paso_lindo(valor):
    if valor <= 0:
        return 1
    potencia = 10 ** math.floor(math.log10(valor))
    base = valor / potencia
    if base <= 1:
        factor = 1
    elif base <= 2:
        factor = 2
    elif base <= 5:
        factor = 5
    else:
        factor = 10
    return factor * potencia


def generar_ticks(limite, max_ticks=MAX_TICKS_EJES_3D):
    minimo, maximo = limite
    paso = paso_lindo((maximo - minimo) / max(max_ticks - 1, 1))
    inicio = math.ceil(minimo / paso) * paso
    fin = math.floor(maximo / paso) * paso
    ticks = []
    valor = inicio
    while valor <= fin + paso * 0.5:
        if minimo <= valor <= maximo:
            ticks.append(0 if abs(valor) < 1e-9 else valor)
        valor += paso
    if minimo <= 0 <= maximo and 0 not in ticks:
        ticks.append(0)
    return sorted(set(ticks))


def formato_tick(valor):
    if abs(valor) < 1e-9:
        return "0"
    if abs(valor - round(valor)) < 1e-9:
        return str(int(round(valor)))
    return f"{valor:g}"


def configurar_3d(
    ax,
    titulo,
    xlim=(-5, 5),
    ylim=(-5, 5),
    zlim=(-5, 5),
    elev=VISTA_ELEV,
    azim=VISTA_AZIM,
):
    xlim, ylim, zlim = limites_con_origen_central(xlim, ylim, zlim)
    ax.set_title(titulo)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_zlabel("")
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_zlim(*zlim)
    ax.set_xticks(generar_ticks(xlim))
    ax.set_yticks(generar_ticks(ylim))
    ax.set_zticks(generar_ticks(zlim))
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_zticklabels([])
    ax.view_init(elev=elev, azim=azim)
    ax.grid(True)
    try:
        ax.set_proj_type("ortho")
    except Exception:
        pass
    try:
        ax.set_box_aspect(
            (xlim[1] - xlim[0], ylim[1] - ylim[0], zlim[1] - zlim[0])
        )
    except Exception:
        pass
    for eje in (ax.xaxis, ax.yaxis, ax.zaxis):
        try:
            eje.line.set_color((1, 1, 1, 0))
            eje.set_tick_params(length=0, width=0)
        except Exception:
            pass


def agregar_ejes_3d(ax, xlim=(-5, 5), ylim=(-5, 5), zlim=(-5, 5)):
    xlim, ylim, zlim = limites_con_origen_central(xlim, ylim, zlim)
    lw = 1.15
    rango_x = xlim[1] - xlim[0]
    rango_y = ylim[1] - ylim[0]
    rango_z = zlim[1] - zlim[0]
    tick = min(rango_x, rango_y, rango_z) * 0.025
    despl = tick * 2.3

    if xlim[0] < 0:
        ax.plot([xlim[0], 0], [0, 0], [0, 0], color=COLOR_EJE, linewidth=lw)
    if xlim[1] > 0:
        ax.quiver(0, 0, 0, xlim[1], 0, 0, color=COLOR_EJE, linewidth=lw, arrow_length_ratio=0.06)
        ax.text(xlim[1] + despl, 0, 0, "x", color=COLOR_EJE, fontsize=9, style="italic")
    elif xlim[0] < 0:
        ax.quiver(0, 0, 0, xlim[0], 0, 0, color=COLOR_EJE, linewidth=lw, arrow_length_ratio=0.06)
        ax.text(xlim[0] - despl, 0, 0, "x", color=COLOR_EJE, fontsize=9, style="italic")

    if ylim[0] < 0:
        ax.plot([0, 0], [ylim[0], 0], [0, 0], color=COLOR_EJE, linewidth=lw)
    if ylim[1] > 0:
        ax.quiver(0, 0, 0, 0, ylim[1], 0, color=COLOR_EJE, linewidth=lw, arrow_length_ratio=0.06)
        ax.text(0, ylim[1] + despl, 0, "y", color=COLOR_EJE, fontsize=9, style="italic")
    elif ylim[0] < 0:
        ax.quiver(0, 0, 0, 0, ylim[0], 0, color=COLOR_EJE, linewidth=lw, arrow_length_ratio=0.06)
        ax.text(0, ylim[0] - despl, 0, "y", color=COLOR_EJE, fontsize=9, style="italic")

    if zlim[0] < 0:
        ax.plot([0, 0], [0, 0], [zlim[0], 0], color=COLOR_EJE, linewidth=lw)
    if zlim[1] > 0:
        ax.quiver(0, 0, 0, 0, 0, zlim[1], color=COLOR_EJE, linewidth=lw, arrow_length_ratio=0.06)
        ax.text(0, 0, zlim[1] + despl, "z", color=COLOR_EJE, fontsize=9, style="italic")
    elif zlim[0] < 0:
        ax.quiver(0, 0, 0, 0, 0, zlim[0], color=COLOR_EJE, linewidth=lw, arrow_length_ratio=0.06)
        ax.text(0, 0, zlim[0] - despl, "z", color=COLOR_EJE, fontsize=9, style="italic")

    ax.text(-despl, 0, despl * 0.45, "O", color=COLOR_EJE, fontsize=9, style="italic")

    if not MOSTRAR_TICKS_EJES_3D:
        return

    for valor in generar_ticks(xlim):
        if valor == 0:
            continue
        ax.plot([valor, valor], [-tick, tick], [0, 0], color=COLOR_EJE, linewidth=0.8)
        ax.text(valor, -despl, 0, formato_tick(valor), color=COLOR_EJE, fontsize=7)

    for valor in generar_ticks(ylim):
        if valor == 0:
            continue
        ax.plot([-tick, tick], [valor, valor], [0, 0], color=COLOR_EJE, linewidth=0.8)
        ax.text(-despl, valor, 0, formato_tick(valor), color=COLOR_EJE, fontsize=7)

    for valor in generar_ticks(zlim):
        if valor == 0:
            continue
        ax.plot([-tick, tick], [0, 0], [valor, valor], color=COLOR_EJE, linewidth=0.8)
        ax.text(despl, 0, valor, formato_tick(valor), color=COLOR_EJE, fontsize=7)


def borde_plano_x(ax, x0, ylim, zlim, color=COLOR_BORDE):
    y0, y1 = ylim
    z0, z1 = zlim
    ax.plot([x0, x0], [y0, y1], [z0, z0], color=color, linewidth=1.0)
    ax.plot([x0, x0], [y0, y1], [z1, z1], color=color, linewidth=1.0)
    ax.plot([x0, x0], [y0, y0], [z0, z1], color=color, linewidth=1.0)
    ax.plot([x0, x0], [y1, y1], [z0, z1], color=color, linewidth=1.0)


def borde_plano_y(ax, y0, xlim, zlim, color=COLOR_BORDE):
    x0, x1 = xlim
    z0, z1 = zlim
    ax.plot([x0, x1], [y0, y0], [z0, z0], color=color, linewidth=1.0)
    ax.plot([x0, x1], [y0, y0], [z1, z1], color=color, linewidth=1.0)
    ax.plot([x0, x0], [y0, y0], [z0, z1], color=color, linewidth=1.0)
    ax.plot([x1, x1], [y0, y0], [z0, z1], color=color, linewidth=1.0)


def borde_plano_z(ax, z0, xlim, ylim, color=COLOR_BORDE):
    x0, x1 = xlim
    y0, y1 = ylim
    ax.plot([x0, x1], [y0, y0], [z0, z0], color=color, linewidth=1.0)
    ax.plot([x0, x1], [y1, y1], [z0, z0], color=color, linewidth=1.0)
    ax.plot([x0, x0], [y0, y1], [z0, z0], color=color, linewidth=1.0)
    ax.plot([x1, x1], [y0, y1], [z0, z0], color=color, linewidth=1.0)


def etiqueta_3d(ax, x, y, z, texto, fontsize=10):
    ax.text(x, y, z, texto, color=COLOR_EJE, fontsize=fontsize, style="italic", zorder=20)


def plano_x(ax, x0, ylim=(-4, 4), zlim=(-4, 4), color=COLOR_PARED, alpha=0.35):
    y = np.linspace(*ylim, 35)
    z = np.linspace(*zlim, 35)
    yy, zz = np.meshgrid(y, z)
    xx = np.full_like(yy, x0)
    ax.plot_surface(xx, yy, zz, color=color, alpha=alpha, linewidth=0, shade=False)
    borde_plano_x(ax, x0, ylim, zlim)


def plano_y(ax, y0, xlim=(-4, 4), zlim=(-4, 4), color=COLOR_PARED_2, alpha=0.35):
    x = np.linspace(*xlim, 35)
    z = np.linspace(*zlim, 35)
    xx, zz = np.meshgrid(x, z)
    yy = np.full_like(xx, y0)
    ax.plot_surface(xx, yy, zz, color=color, alpha=alpha, linewidth=0, shade=False)
    borde_plano_y(ax, y0, xlim, zlim)


def plano_z(ax, z0, xlim=(-4, 4), ylim=(-4, 4), color=COLOR_PISO, alpha=0.35):
    x = np.linspace(*xlim, 35)
    y = np.linspace(*ylim, 35)
    xx, yy = np.meshgrid(x, y)
    zz = np.full_like(xx, z0)
    ax.plot_surface(xx, yy, zz, color=color, alpha=alpha, linewidth=0, shade=False)
    borde_plano_z(ax, z0, xlim, ylim)


def esfera(ax, radio, color=COLOR_SUPERFICIE, alpha=0.22, mitad_superior=False):
    theta = np.linspace(0, 2 * math.pi, 70)
    phi_max = math.pi / 2 if mitad_superior else math.pi
    phi = np.linspace(0, phi_max, 35)
    theta, phi = np.meshgrid(theta, phi)
    x = radio * np.sin(phi) * np.cos(theta)
    y = radio * np.sin(phi) * np.sin(theta)
    z = radio * np.cos(phi)
    ax.plot_surface(x, y, z, color=color, alpha=alpha, linewidth=0, shade=False)


def cilindro_vertical(ax, radio, zlim=(-4, 4), color=COLOR_SUPERFICIE, alpha=0.32):
    theta = np.linspace(0, 2 * math.pi, 80)
    z = np.linspace(*zlim, 35)
    theta, z = np.meshgrid(theta, z)
    x = radio * np.cos(theta)
    y = radio * np.sin(theta)
    ax.plot_surface(x, y, z, color=color, alpha=alpha, linewidth=0, shade=False)


def guardar_o_mostrar(fig, nombre, carpeta_salida=None):
    if carpeta_salida is None:
        fig.canvas.manager.set_window_title(nombre)
        plt.show()
        return

    carpeta_salida.mkdir(parents=True, exist_ok=True)
    ruta = carpeta_salida / f"{nombre}.png"
    fig.savefig(ruta, dpi=170)
    plt.close(fig)
    print(f"Guardado: {ruta}")


def ejercicio_01():
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")
    configurar_3d(
        ax,
        "E1 - Planos coordenados: xy (z=0), xz (y=0), yz (x=0)",
        (-4, 4),
        (-4, 4),
        (-4, 4),
    )
    plano_z(ax, 0, color="tab:green", alpha=0.28)
    plano_y(ax, 0, color="tab:orange", alpha=0.28)
    plano_x(ax, 0, color="tab:blue", alpha=0.28)
    agregar_ejes_3d(ax, (-4, 4), (-4, 4), (-4, 4))
    etiqueta_3d(ax, 1.2, 2.4, 0.15, "plano xy")
    etiqueta_3d(ax, 1.4, 0.08, 2.2, "plano xz")
    etiqueta_3d(ax, 0.08, 2.2, 2.2, "plano yz")
    return fig


def ejercicio_02():
    fig = plt.figure(figsize=(13, 8))
    titulos = [
        "a) x = 3",
        "b) y = 6",
        "c) z = 2",
        "d) x + y = 3",
        "e) x + y + z = 1",
    ]

    ax = fig.add_subplot(231, projection="3d")
    configurar_3d(ax, titulos[0], (0, 5), (-3, 3), (-3, 3))
    plano_x(ax, 3, (-3, 3), (-3, 3), COLOR_PARED)
    agregar_ejes_3d(ax, (0, 5), (-3, 3), (-3, 3))
    etiqueta_3d(ax, 3, 0.8, 1.0, "x = 3")

    ax = fig.add_subplot(232, projection="3d")
    configurar_3d(ax, titulos[1], (-3, 3), (3, 8), (-3, 3))
    plano_y(ax, 6, (-3, 3), (-3, 3), COLOR_PARED_2)
    agregar_ejes_3d(ax, (-3, 3), (3, 8), (-3, 3))
    etiqueta_3d(ax, 0.8, 6, 1.0, "y = 6")

    ax = fig.add_subplot(233, projection="3d")
    configurar_3d(ax, titulos[2], (-3, 3), (-3, 3), (0, 4))
    plano_z(ax, 2, (-3, 3), (-3, 3), COLOR_PISO)
    agregar_ejes_3d(ax, (-3, 3), (-3, 3), (0, 4))
    etiqueta_3d(ax, 1.0, 1.2, 2.08, "z = 2")

    ax = fig.add_subplot(234, projection="3d")
    configurar_3d(ax, titulos[3], (-1, 4), (-1, 4), (-3, 3))
    x = np.linspace(-1, 4, 35)
    z = np.linspace(-3, 3, 35)
    xx, zz = np.meshgrid(x, z)
    yy = 3 - xx
    ax.plot_surface(xx, yy, zz, color="tab:red", alpha=0.35, linewidth=0)
    agregar_ejes_3d(ax, (-1, 4), (-1, 4), (-3, 3))
    etiqueta_3d(ax, 1.0, 2.0, 1.0, "x + y = 3")

    ax = fig.add_subplot(235, projection="3d")
    configurar_3d(ax, titulos[4], (-2, 3), (-2, 3), (-4, 4))
    x = np.linspace(-2, 3, 40)
    y = np.linspace(-2, 3, 40)
    xx, yy = np.meshgrid(x, y)
    zz = 1 - xx - yy
    ax.plot_surface(xx, yy, zz, color="tab:purple", alpha=0.35, linewidth=0)
    agregar_ejes_3d(ax, (-2, 3), (-2, 3), (-4, 4))
    etiqueta_3d(ax, 0.6, 0.6, -0.2, "x + y + z = 1")

    return fig


def ejercicio_03():
    fig = plt.figure(figsize=(12, 5.5))

    ax = fig.add_subplot(121, projection="3d")
    configurar_3d(
        ax,
        "E3.a - Plano normal a v=(5,2,-1): 5x + 2y - z + 22 = 0",
        (-6, 1),
        (-4, 4),
        (-12, 25),
    )
    x = np.linspace(-6, 1, 45)
    y = np.linspace(-4, 4, 45)
    xx, yy = np.meshgrid(x, y)
    zz = 5 * xx + 2 * yy + 22
    ax.plot_surface(xx, yy, zz, color="tab:blue", alpha=0.35, linewidth=0)
    ax.quiver(-3, 0, 7, 5, 2, -1, length=2.2, color="crimson", normalize=True)
    ax.scatter([-3], [0], [7], color=COLOR_PUNTO, s=35)
    etiqueta_3d(ax, -3, 0, 8.5, "P0(-3,0,7)", fontsize=9)
    agregar_ejes_3d(ax, (-6, 1), (-4, 4), (-12, 25))
    etiqueta_3d(ax, -2.6, 1.0, 8.0, "5x + 2y - z + 22 = 0", fontsize=8)

    ax = fig.add_subplot(122, projection="3d")
    configurar_3d(
        ax,
        "E3.b - Paralelo a Oz: x/2 + y/3 = 1",
        (-1, 3.5),
        (-1, 4),
        (-3, 3),
    )
    x = np.linspace(-1, 3.5, 35)
    z = np.linspace(-3, 3, 35)
    xx, zz = np.meshgrid(x, z)
    yy = 3 - 1.5 * xx
    ax.plot_surface(xx, yy, zz, color="tab:orange", alpha=0.35, linewidth=0)
    ax.scatter([2, 0], [0, 3], [0, 0], color=COLOR_PUNTO, s=35)
    etiqueta_3d(ax, 2, 0, 0.35, "(2,0,0)", fontsize=8)
    etiqueta_3d(ax, 0, 3, 0.35, "(0,3,0)", fontsize=8)
    agregar_ejes_3d(ax, (-1, 3.5), (-1, 4), (-3, 3))
    etiqueta_3d(ax, 1.0, 1.5, 1.1, "x/2 + y/3 = 1", fontsize=8)

    return fig


def ejercicio_04():
    fig = plt.figure(figsize=(12, 9))

    ax = fig.add_subplot(221, projection="3d")
    configurar_3d(ax, "E4.a - x = 1 - y^2 (cilindro parabolico)", (-4, 2), (-2.2, 2.2), (-3, 3))
    y = np.linspace(-2.2, 2.2, 55)
    z = np.linspace(-3, 3, 35)
    yy, zz = np.meshgrid(y, z)
    xx = 1 - yy**2
    ax.plot_surface(xx, yy, zz, color="tab:blue", alpha=0.45, linewidth=0)
    agregar_ejes_3d(ax, (-4, 2), (-2.2, 2.2), (-3, 3))
    etiqueta_3d(ax, 0.4, 1.0, 1.5, "x = 1 - y^2", fontsize=8)

    ax = fig.add_subplot(222, projection="3d")
    configurar_3d(ax, "E4.b - z = log(x) (cilindro logaritmico)", (0, 5), (-3, 3), (-2.5, 2))
    x = np.linspace(0.1, 5, 55)
    y = np.linspace(-3, 3, 35)
    xx, yy = np.meshgrid(x, y)
    zz = np.log(xx)
    ax.plot_surface(xx, yy, zz, color="tab:orange", alpha=0.45, linewidth=0)
    agregar_ejes_3d(ax, (0, 5), (-3, 3), (-2.5, 2))
    etiqueta_3d(ax, 2.2, 0.9, 0.8, "z = log(x)", fontsize=8)

    ax = fig.add_subplot(223, projection="3d")
    configurar_3d(ax, "E4.c - z = e^y (cilindro exponencial)", (-3, 3), (-2, 1.5), (0, 5))
    x = np.linspace(-3, 3, 35)
    y = np.linspace(-2, 1.5, 55)
    xx, yy = np.meshgrid(x, y)
    zz = np.exp(yy)
    ax.plot_surface(xx, yy, zz, color="tab:green", alpha=0.45, linewidth=0)
    agregar_ejes_3d(ax, (-3, 3), (-2, 1.5), (0, 5))
    etiqueta_3d(ax, 0.8, 0.8, 2.4, "z = e^y", fontsize=8)

    ax = fig.add_subplot(224, projection="3d")
    configurar_3d(ax, "E4.d - z = x^(3/2) (ala de gaviota)", (0, 4), (-3, 3), (0, 8.5))
    x = np.linspace(0, 4, 55)
    y = np.linspace(-3, 3, 35)
    xx, yy = np.meshgrid(x, y)
    zz = xx**1.5
    ax.plot_surface(xx, yy, zz, color="tab:red", alpha=0.45, linewidth=0)
    agregar_ejes_3d(ax, (0, 4), (-3, 3), (0, 8.5))
    etiqueta_3d(ax, 1.6, 1.0, 2.5, "z = x^(3/2)", fontsize=8)

    return fig


def ejercicio_05():
    fig = plt.figure(figsize=(13, 10))

    ax = fig.add_subplot(231, projection="3d")
    configurar_3d(ax, "E5.a - z = 1 + y^2 - x^2", (-2.5, 2.5), (-2.5, 2.5), (-5, 6))
    x = np.linspace(-2.2, 2.2, 70)
    y = np.linspace(-2.2, 2.2, 70)
    xx, yy = np.meshgrid(x, y)
    zz = 1 + yy**2 - xx**2
    ax.plot_surface(xx, yy, zz, cmap="viridis", alpha=0.75, linewidth=0)
    t = np.linspace(-2.2, 2.2, 160)
    ax.plot(np.zeros_like(t), t, 1 + t**2, color=COLOR_PUNTO, linewidth=2)
    ax.plot(t, np.zeros_like(t), 1 - t**2, color=COLOR_CURVA, linewidth=2)
    agregar_ejes_3d(ax, (-2.5, 2.5), (-2.5, 2.5), (-5, 6))

    ax = fig.add_subplot(232, projection="3d")
    configurar_3d(ax, "E5.b - y = -(x^2 + z^2)", (-2.2, 2.2), (-8, 0.5), (-2.2, 2.2))
    x = np.linspace(-2, 2, 70)
    z = np.linspace(-2, 2, 70)
    xx, zz = np.meshgrid(x, z)
    yy = -(xx**2 + zz**2)
    ax.plot_surface(xx, yy, zz, cmap="plasma", alpha=0.75, linewidth=0)
    t = np.linspace(-2, 2, 160)
    ax.plot(t, -(t**2), np.zeros_like(t), color=COLOR_CURVA, linewidth=2)
    ax.plot(np.zeros_like(t), -(t**2), t, color=COLOR_PUNTO, linewidth=2)
    agregar_ejes_3d(ax, (-2.2, 2.2), (-8, 0.5), (-2.2, 2.2))

    ax = fig.add_subplot(233, projection="3d")
    configurar_3d(ax, "E5.c - x^2 + y^2 - z^2 = 4", (-4, 4), (-4, 4), (-3, 3))
    theta = np.linspace(0, 2 * math.pi, 80)
    z = np.linspace(-3, 3, 55)
    theta, zz = np.meshgrid(theta, z)
    r = np.sqrt(4 + zz**2)
    xx = r * np.cos(theta)
    yy = r * np.sin(theta)
    ax.plot_surface(xx, yy, zz, cmap="cividis", alpha=0.75, linewidth=0)
    theta_trace = np.linspace(0, 2 * math.pi, 180)
    ax.plot(2 * np.cos(theta_trace), 2 * np.sin(theta_trace), 0, color=COLOR_PUNTO, linewidth=2)
    agregar_ejes_3d(ax, (-4, 4), (-4, 4), (-3, 3))

    ax = fig.add_subplot(234, projection="3d")
    configurar_3d(ax, "E5.d - 16y^2 + 9z^2 = 4x^2", (-4, 4), (-2.2, 2.2), (-3, 3))
    x = np.linspace(-4, 4, 90)
    theta = np.linspace(0, 2 * math.pi, 80)
    xx, theta = np.meshgrid(x, theta)
    yy = np.abs(xx) / 2 * np.cos(theta)
    zz = 2 * np.abs(xx) / 3 * np.sin(theta)
    ax.plot_surface(xx, yy, zz, cmap="magma", alpha=0.72, linewidth=0)
    t = np.linspace(-4, 4, 120)
    ax.plot(t, t / 2, np.zeros_like(t), color=COLOR_CURVA, linewidth=2)
    ax.plot(t, -t / 2, np.zeros_like(t), color=COLOR_CURVA, linewidth=2)
    agregar_ejes_3d(ax, (-4, 4), (-2.2, 2.2), (-3, 3))

    ax = fig.add_subplot(235, projection="3d")
    configurar_3d(ax, "E5.e - x^2 + y^2 = z", (-2.5, 2.5), (-2.5, 2.5), (0, 8))
    x = np.linspace(-2.2, 2.2, 70)
    y = np.linspace(-2.2, 2.2, 70)
    xx, yy = np.meshgrid(x, y)
    zz = xx**2 + yy**2
    ax.plot_surface(xx, yy, zz, cmap="viridis", alpha=0.75, linewidth=0)
    t = np.linspace(-2.2, 2.2, 160)
    ax.plot(t, np.zeros_like(t), t**2, color=COLOR_CURVA, linewidth=2)
    ax.plot(np.zeros_like(t), t, t**2, color=COLOR_PUNTO, linewidth=2)
    agregar_ejes_3d(ax, (-2.5, 2.5), (-2.5, 2.5), (0, 8))

    return fig


def ejercicio_06():
    fig = plt.figure(figsize=(13, 8))

    ax = fig.add_subplot(231, projection="3d")
    configurar_3d(ax, "E6.a - x^2 = 0 -> plano x=0", (-3, 3), (-3, 3), (-3, 3))
    plano_x(ax, 0, (-3, 3), (-3, 3), COLOR_PARED)
    agregar_ejes_3d(ax, (-3, 3), (-3, 3), (-3, 3))

    ax = fig.add_subplot(232, projection="3d")
    configurar_3d(ax, "E6.b - x^2+y^2=0 -> eje z", (-3, 3), (-3, 3), (-3, 3))
    t = np.linspace(-3, 3, 100)
    ax.plot(np.zeros_like(t), np.zeros_like(t), t, color=COLOR_PUNTO, linewidth=3)
    agregar_ejes_3d(ax, (-3, 3), (-3, 3), (-3, 3))

    ax = fig.add_subplot(233, projection="3d")
    configurar_3d(ax, "E6.c - x^2+y^2+z^2=0 -> origen", (-3, 3), (-3, 3), (-3, 3))
    ax.scatter([0], [0], [0], color=COLOR_PUNTO, s=50)
    agregar_ejes_3d(ax, (-3, 3), (-3, 3), (-3, 3))

    ax = fig.add_subplot(234, projection="3d")
    configurar_3d(ax, "E6.d - z^2-1=0 -> z=1 y z=-1", (-3, 3), (-3, 3), (-2, 2))
    plano_z(ax, 1, (-3, 3), (-3, 3), "tab:green", 0.28)
    plano_z(ax, -1, (-3, 3), (-3, 3), "tab:orange", 0.28)
    agregar_ejes_3d(ax, (-3, 3), (-3, 3), (-2, 2))

    ax = fig.add_subplot(235, projection="3d")
    configurar_3d(ax, "E6.e - x=2, y=3 -> recta paralela a z", (0, 4), (1, 5), (-3, 3))
    ax.plot(np.full_like(t, 2), np.full_like(t, 3), t, color=COLOR_PUNTO, linewidth=3)
    agregar_ejes_3d(ax, (0, 4), (1, 5), (-3, 3))

    ax = fig.add_subplot(236, projection="3d")
    configurar_3d(ax, "E6.f - y=3, z=5 -> recta paralela a x", (-4, 4), (1, 5), (3, 7))
    ax.plot(t, np.full_like(t, 3), np.full_like(t, 5), color=COLOR_PUNTO, linewidth=3)
    agregar_ejes_3d(ax, (-4, 4), (1, 5), (3, 7))

    return fig


def ejercicio_07():
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")
    configurar_3d(ax, "E7 - Puntos convertidos entre coordenadas", (-3, 8), (-1, 8), (0, 8))

    puntos = [
        ("a", 8 * math.cos(math.pi / 3), 8 * math.sin(math.pi / 3), 7, COLOR_CURVA),
        ("b", -math.sqrt(2), math.sqrt(2), 1, COLOR_PUNTO),
        (
            "c",
            6 * math.sin(math.pi / 3) * math.cos(math.pi / 4),
            6 * math.sin(math.pi / 3) * math.sin(math.pi / 4),
            6 * math.cos(math.pi / 3),
            COLOR_BORDE,
        ),
    ]

    for etiqueta, x, y, z, color in puntos:
        ax.scatter([x], [y], [z], color=color, s=55, label=f"{etiqueta}: ({x:.2f}, {y:.2f}, {z:.2f})")
        ax.plot([0, x], [0, y], [0, z], color=color, linewidth=1.4, alpha=0.75)
        ax.plot([x, x], [y, y], [0, z], color=color, linestyle="--", linewidth=1)
        etiqueta_3d(ax, x, y, z + 0.25, etiqueta, fontsize=9)

    agregar_ejes_3d(ax, (-3, 8), (-1, 8), (0, 8))
    ax.legend(loc="upper left")
    return fig


def ejercicio_08():
    fig = plt.figure(figsize=(13, 9))

    ax = fig.add_subplot(231, projection="3d")
    configurar_3d(ax, "E8.a - r = 2", (-3, 3), (-3, 3), (-4, 4))
    cilindro_vertical(ax, 2, (-4, 4), "tab:blue")
    agregar_ejes_3d(ax, (-3, 3), (-3, 3), (-4, 4))
    etiqueta_3d(ax, 1.4, 1.4, 1.5, "r = 2", fontsize=8)

    ax = fig.add_subplot(232, projection="3d")
    configurar_3d(ax, "E8.b - r = 0", (-3, 3), (-3, 3), (-4, 4))
    z = np.linspace(-4, 4, 120)
    ax.plot(np.zeros_like(z), np.zeros_like(z), z, color=COLOR_PUNTO, linewidth=3)
    agregar_ejes_3d(ax, (-3, 3), (-3, 3), (-4, 4))

    ax = fig.add_subplot(233, projection="3d")
    configurar_3d(ax, "E8.c - theta = -pi/3", (-3, 3), (-4, 1), (-4, 4))
    r = np.linspace(0, 4, 45)
    z = np.linspace(-4, 4, 45)
    rr, zz = np.meshgrid(r, z)
    theta = -math.pi / 3
    xx = rr * math.cos(theta)
    yy = rr * math.sin(theta)
    ax.plot_surface(xx, yy, zz, color="tab:orange", alpha=0.36, linewidth=0)
    agregar_ejes_3d(ax, (-3, 3), (-4, 1), (-4, 4))
    etiqueta_3d(ax, 1.2, -2.0, 1.5, "theta = -pi/3", fontsize=8)

    ax = fig.add_subplot(234, projection="3d")
    configurar_3d(ax, "E8.d - r = 2 y theta = pi/2", (-3, 3), (0, 4), (-4, 4))
    z = np.linspace(-4, 4, 120)
    ax.plot(np.zeros_like(z), np.full_like(z, 2), z, color=COLOR_PUNTO, linewidth=3)
    agregar_ejes_3d(ax, (-3, 3), (0, 4), (-4, 4))

    ax = fig.add_subplot(235, projection="3d")
    configurar_3d(ax, "E8.e - z = r^2 + 4", (-3, 3), (-3, 3), (0, 13))
    r = np.linspace(0, 3, 60)
    theta = np.linspace(0, 2 * math.pi, 90)
    rr, theta = np.meshgrid(r, theta)
    xx = rr * np.cos(theta)
    yy = rr * np.sin(theta)
    zz = rr**2 + 4
    ax.plot_surface(xx, yy, zz, cmap="viridis", alpha=0.75, linewidth=0)
    agregar_ejes_3d(ax, (-3, 3), (-3, 3), (0, 13))
    etiqueta_3d(ax, 1.0, 1.0, 6.5, "z = r^2 + 4", fontsize=8)

    return fig


def ejercicio_10():
    fig = plt.figure(figsize=(13, 5))

    ax = fig.add_subplot(131, projection="3d")
    configurar_3d(ax, "E10.a - rho = 2", (-2.4, 2.4), (-2.4, 2.4), (-2.4, 2.4))
    esfera(ax, 2, "tab:blue", 0.32)
    agregar_ejes_3d(ax, (-2.4, 2.4), (-2.4, 2.4), (-2.4, 2.4))

    ax = fig.add_subplot(132, projection="3d")
    configurar_3d(ax, "E10.b - phi = pi/6", (-2.5, 2.5), (-2.5, 2.5), (0, 4))
    rho = np.linspace(0, 4, 55)
    theta = np.linspace(0, 2 * math.pi, 90)
    rho, theta = np.meshgrid(rho, theta)
    phi = math.pi / 6
    x = rho * math.sin(phi) * np.cos(theta)
    y = rho * math.sin(phi) * np.sin(theta)
    z = rho * math.cos(phi)
    ax.plot_surface(x, y, z, color="tab:orange", alpha=0.36, linewidth=0)
    agregar_ejes_3d(ax, (-2.5, 2.5), (-2.5, 2.5), (0, 4))

    ax = fig.add_subplot(133, projection="3d")
    configurar_3d(ax, "E10.c - rho = 1, 0 <= phi <= pi/2", (-1.2, 1.2), (-1.2, 1.2), (0, 1.2))
    esfera(ax, 1, "tab:green", 0.42, mitad_superior=True)
    agregar_ejes_3d(ax, (-1.2, 1.2), (-1.2, 1.2), (0, 1.2))

    return fig


def ejercicio_12():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))

    ax = axes[0]
    configurar_2d(ax, "E12.a - Dominio de sqrt(y - x - 2)", (-6, 6), (-6, 8))
    x = np.linspace(-6, 6, 400)
    y_frontera = x + 2
    ax.fill_between(x, y_frontera, 8, color="tab:blue", alpha=0.25, label="y >= x + 2")
    ax.plot(x, y_frontera, color="tab:blue", linewidth=2)
    ax.legend(loc="upper left")

    ax = axes[1]
    configurar_2d(ax, "E12.b - Dominio de ln(x^2 + y^2 - 4)", (-5, 5), (-5, 5))
    x = np.linspace(-5, 5, 400)
    y = np.linspace(-5, 5, 400)
    xx, yy = np.meshgrid(x, y)
    dominio = xx**2 + yy**2 > 4
    ax.contourf(xx, yy, dominio, levels=[0.5, 1.5], colors=["tab:green"], alpha=0.25)
    theta = np.linspace(0, 2 * math.pi, 260)
    ax.plot(2 * np.cos(theta), 2 * np.sin(theta), color=COLOR_PUNTO, linestyle="--", linewidth=2, label="frontera excluida")
    ax.legend(loc="upper right")

    ax = axes[2]
    configurar_2d(ax, "E12.c - Dominio excepto y=x e y=x^3", (-3, 3), (-6, 6), igual=False)
    ax.axhspan(-6, 6, color="tab:orange", alpha=0.11, label="dominio")
    x = np.linspace(-3, 3, 500)
    ax.plot(x, x, color=COLOR_PUNTO, linestyle="--", linewidth=2, label="y = x excluida")
    ax.plot(x, x**3, color=COLOR_CURVA, linestyle="--", linewidth=2, label="y = x^3 excluida")
    ax.legend(loc="upper left")

    return fig


def ejercicio_13():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.2))

    ax = axes[0]
    configurar_2d(ax, "E13.a - x^2 + y^2 = c", (-6, 6), (-6, 6))
    theta = np.linspace(0, 2 * math.pi, 400)
    for c in [0, 1, 4, 9, 16, 25]:
        if c == 0:
            ax.scatter([0], [0], s=35, label="c=0")
        else:
            r = math.sqrt(c)
            ax.plot(r * np.cos(theta), r * np.sin(theta), label=f"c={c}")
    ax.legend(ncol=2)

    ax = axes[1]
    configurar_2d(ax, "E13.b - sqrt(25 - x^2 - y^2) = c", (-6, 6), (-6, 6))
    for c in [0, 1, 2, 3, 4]:
        r = math.sqrt(25 - c**2)
        ax.plot(r * np.cos(theta), r * np.sin(theta), label=f"c={c}")
    ax.legend(ncol=2)

    return fig


def ejercicio_14():
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")
    configurar_3d(
        ax,
        "E14 - Superficies de nivel sqrt(x^2+y^2+z^2)=c",
        (-4.5, 4.5),
        (-4.5, 4.5),
        (-4.5, 4.5),
    )
    for radio, color in [(1, "tab:green"), (2, "tab:orange"), (4, "tab:blue")]:
        esfera(ax, radio, color, 0.20)
        etiqueta_3d(ax, radio, 0, 0, f"c={radio}", fontsize=8)
    agregar_ejes_3d(ax, (-4.5, 4.5), (-4.5, 4.5), (-4.5, 4.5))
    return fig


def panel_dominio_todo_r2(ax, titulo):
    configurar_2d(ax, titulo, (-4, 4), (-4, 4))
    ax.axhspan(-4, 4, color="tab:green", alpha=0.15)
    ax.text(-3.8, 3.45, "Dominio: R^2", fontsize=10)


def ejercicio_15():
    figs = []
    figs.append(ejercicio_15_paraboloide_eliptico())
    figs.append(ejercicio_15_paraboloide_hiperbolico())
    return figs


def ejercicio_15_paraboloide_eliptico():
    fig = plt.figure(figsize=(13, 9))

    ax = fig.add_subplot(221)
    panel_dominio_todo_r2(ax, "E15 - f(x,y)=4x^2+9y^2: dominio")

    ax = fig.add_subplot(222)
    configurar_2d(ax, "Curvas de nivel: 4x^2 + 9y^2 = c", (-4, 4), (-3, 3))
    x = np.linspace(-4, 4, 420)
    y = np.linspace(-3, 3, 420)
    xx, yy = np.meshgrid(x, y)
    zz = 4 * xx**2 + 9 * yy**2
    cs = ax.contour(xx, yy, zz, levels=[4, 9, 16, 25, 36, 49], cmap="viridis")
    ax.clabel(cs, inline=True, fontsize=8)

    ax = fig.add_subplot(223, projection="3d")
    configurar_3d(ax, "Superficie: paraboloide eliptico", (-3, 3), (-3, 3), (0, 45))
    x = np.linspace(-3, 3, 80)
    y = np.linspace(-3, 3, 80)
    xx, yy = np.meshgrid(x, y)
    zz = 4 * xx**2 + 9 * yy**2
    ax.plot_surface(xx, yy, zz, cmap="viridis", alpha=0.78, linewidth=0)
    t = np.linspace(-3, 3, 180)
    ax.plot(t, np.zeros_like(t), 4 * t**2, color=COLOR_CURVA, linewidth=2, label="y=0")
    ax.plot(np.zeros_like(t), t, 9 * t**2, color=COLOR_PUNTO, linewidth=2, label="x=0")
    agregar_ejes_3d(ax, (-3, 3), (-3, 3), (0, 45))

    ax = fig.add_subplot(224)
    ax.set_title("Trazas principales")
    t = np.linspace(-3, 3, 250)
    ax.plot(t, 4 * t**2, label="y=0: z=4x^2")
    ax.plot(t, 9 * t**2, label="x=0: z=9y^2")
    ax.set_xlabel("variable")
    ax.set_ylabel("z")
    ax.set_ylim(0, 45)
    ax.legend()

    return fig


def ejercicio_15_paraboloide_hiperbolico():
    fig = plt.figure(figsize=(13, 9))

    ax = fig.add_subplot(221)
    panel_dominio_todo_r2(ax, "E15 - f(x,y)=x^2-y^2: dominio")

    ax = fig.add_subplot(222)
    configurar_2d(ax, "Curvas de nivel: x^2 - y^2 = c", (-4, 4), (-4, 4))
    x = np.linspace(-4, 4, 500)
    y = np.linspace(-4, 4, 500)
    xx, yy = np.meshgrid(x, y)
    zz = xx**2 - yy**2
    cs = ax.contour(xx, yy, zz, levels=[-9, -4, -1, 0, 1, 4, 9], cmap="coolwarm")
    ax.clabel(cs, inline=True, fontsize=8)

    ax = fig.add_subplot(223, projection="3d")
    configurar_3d(ax, "Superficie: paraboloide hiperbolico", (-3, 3), (-3, 3), (-9, 9))
    x = np.linspace(-3, 3, 80)
    y = np.linspace(-3, 3, 80)
    xx, yy = np.meshgrid(x, y)
    zz = xx**2 - yy**2
    ax.plot_surface(xx, yy, zz, cmap="coolwarm", alpha=0.78, linewidth=0)
    t = np.linspace(-3, 3, 180)
    ax.plot(t, np.zeros_like(t), t**2, color=COLOR_CURVA, linewidth=2, label="y=0")
    ax.plot(np.zeros_like(t), t, -(t**2), color=COLOR_PUNTO, linewidth=2, label="x=0")
    agregar_ejes_3d(ax, (-3, 3), (-3, 3), (-9, 9))

    ax = fig.add_subplot(224)
    ax.set_title("Trazas principales")
    t = np.linspace(-3, 3, 250)
    ax.plot(t, t**2, label="y=0: z=x^2")
    ax.plot(t, -(t**2), label="x=0: z=-y^2")
    ax.axhline(0, color="0.25", linewidth=0.8)
    ax.set_xlabel("variable")
    ax.set_ylabel("z")
    ax.set_ylim(-9, 9)
    ax.legend()

    return fig


def ejercicio_16():
    fig = plt.figure(figsize=(13, 9))

    ax = fig.add_subplot(221)
    configurar_2d(ax, "E16.a - Dominio de U: R^2 sin el origen", (-4, 4), (-4, 4))
    ax.axhspan(-4, 4, color="tab:green", alpha=0.13)
    ax.scatter([0], [0], color=COLOR_PUNTO, s=70, marker="x", linewidths=2, label="origen excluido")
    ax.legend()

    ax = fig.add_subplot(222)
    configurar_2d(ax, "E16.c - Equipotenciales U(x,y)=c", (-4.5, 4.5), (-4.5, 4.5))
    theta = np.linspace(0, 2 * math.pi, 400)
    for c in [0.25, 0.5, 1, 2]:
        r = 1 / c
        ax.plot(r * np.cos(theta), r * np.sin(theta), label=f"c={c:g}, r={r:g}")
    ax.scatter([0], [0], color=COLOR_PUNTO, s=35)
    ax.legend()

    x = np.linspace(-4, 4, 170)
    y = np.linspace(-4, 4, 170)
    xx, yy = np.meshgrid(x, y)
    rr = np.sqrt(xx**2 + yy**2)
    zz = np.full_like(rr, np.nan)
    mascara = rr > 0.22
    zz[mascara] = 1 / rr[mascara]

    ax = fig.add_subplot(223, projection="3d")
    configurar_3d(ax, "E16.d - Potencial U=1/sqrt(x^2+y^2)", (-4, 4), (-4, 4), (0, 4.8))
    ax.plot_surface(xx, yy, zz, cmap="inferno", alpha=0.88, linewidth=0)
    agregar_ejes_3d(ax, (-4, 4), (-4, 4), (0, 4.8))

    ax = fig.add_subplot(224)
    configurar_2d(ax, "Mapa de contorno del potencial", (-4, 4), (-4, 4))
    levels = [0.25, 0.35, 0.5, 0.75, 1, 1.5, 2, 3]
    cs = ax.contour(xx, yy, zz, levels=levels, cmap="inferno")
    ax.clabel(cs, inline=True, fontsize=8)
    ax.scatter([0], [0], color=COLOR_PUNTO, s=25)

    return fig


def ejercicio_17():
    fig, ax = plt.subplots(figsize=(8, 5.5))
    configurar_2d(
        ax,
        "E17 - Isotermas T(P,V)=0.01PV",
        (50, 1000),
        (0, 1250),
        igual=False,
    )
    ax.set_xlabel("Volumen V (litros)")
    ax.set_ylabel("Presion P (atm)")
    volumen = np.linspace(50, 1000, 600)
    for temperatura in [300, 400, 600]:
        presion = temperatura / (0.01 * volumen)
        ax.plot(volumen, presion, linewidth=2, label=f"T = {temperatura} K")
    ax.legend()
    return fig


EJERCICIOS = {
    1: ("Planos coordenados", ejercicio_01, "e01_planos_coordenados"),
    2: ("Planos dados", ejercicio_02, "e02_planos"),
    3: ("Planos hallados", ejercicio_03, "e03_planos_hallados"),
    4: ("Cilindros", ejercicio_04, "e04_cilindros"),
    5: ("Cuadricas", ejercicio_05, "e05_cuadricas"),
    6: ("Reconocimiento de ecuaciones", ejercicio_06, "e06_reconocimiento"),
    7: ("Conversiones de coordenadas", ejercicio_07, "e07_coordenadas"),
    8: ("Coordenadas cilindricas", ejercicio_08, "e08_cilindricas"),
    10: ("Coordenadas esfericas", ejercicio_10, "e10_esfericas"),
    12: ("Dominios en el plano xy", ejercicio_12, "e12_dominios"),
    13: ("Curvas de nivel", ejercicio_13, "e13_curvas_de_nivel"),
    14: ("Superficies de nivel", ejercicio_14, "e14_superficies_de_nivel"),
    15: ("Funciones campo escalar", ejercicio_15, "e15_funciones"),
    16: ("Potencial electrostatico", ejercicio_16, "e16_potencial"),
    17: ("Isotermas", ejercicio_17, "e17_isotermas"),
}


NOTAS = {
    3: [
        "E3.a: 5(x+3)+2y-(z-7)=0 -> 5x+2y-z+22=0.",
        "E3.b: plano vertical paralelo a Oz: x/2 + y/3 = 1.",
    ],
    6: [
        "E6 se incluye como apoyo visual, aunque el enunciado pide reconocer figuras.",
    ],
    10: [
        "E10 se incluye como apoyo visual para los conjuntos esfericos descriptivos.",
    ],
    12: [
        "E12.a: y >= x + 2.",
        "E12.b: x^2 + y^2 > 4.",
        "E12.c: y != x e y != x^3.",
    ],
    14: [
        "E14: las superficies de nivel son esferas x^2+y^2+z^2=c^2.",
    ],
    15: [
        "E15: ambos dominios son R^2. Las superficies son un paraboloide eliptico y un paraboloide hiperbolico.",
    ],
    16: [
        "E16: dominio R^2 sin (0,0); rango (0, infinito); equipotenciales circulos centrados en el origen.",
    ],
    17: [
        "E17: T=0.01PV implica P=T/(0.01V).",
    ],
}


def listar_ejercicios():
    print("Ejercicios disponibles para graficar:")
    for numero, (titulo, _, _) in EJERCICIOS.items():
        print(f"  {numero:>2} - {titulo}")
    print("\nNo se generan graficos de los ejercicios 9 y 11 porque no los piden.")


def pedir_ejercicios_por_menu():
    listar_ejercicios()
    texto = input("\nIngrese numeros separados por coma/espacio, o 'todos': ").strip().lower()
    if texto in {"todos", "todo", "t"}:
        return list(EJERCICIOS)
    texto = texto.replace(",", " ")
    elegidos = []
    for parte in texto.split():
        try:
            numero = int(parte)
        except ValueError:
            continue
        if numero in EJERCICIOS:
            elegidos.append(numero)
        else:
            print(f"Ejercicio {numero} no disponible o no pide grafico.")
    return elegidos


def normalizar_figuras(resultado):
    if isinstance(resultado, list):
        return resultado
    return [resultado]


def ejecutar_ejercicios(numeros, carpeta_salida=None):
    for numero in numeros:
        titulo, funcion, nombre_base = EJERCICIOS[numero]
        print(f"\nGenerando E{numero}: {titulo}")
        for nota in NOTAS.get(numero, []):
            print(f"  {nota}")
        figuras = normalizar_figuras(funcion())
        for indice, fig in enumerate(figuras, start=1):
            sufijo = "" if len(figuras) == 1 else f"_{indice}"
            guardar_o_mostrar(fig, f"{nombre_base}{sufijo}", carpeta_salida)


def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description="Grafica los ejercicios obligatorios del Taller 04 de campos escalares."
    )
    parser.add_argument(
        "--listar",
        action="store_true",
        help="Muestra los ejercicios con graficos disponibles.",
    )
    parser.add_argument(
        "--ejercicio",
        nargs="+",
        type=int,
        help="Numeros de ejercicios a graficar. Ejemplo: --ejercicio 4 12 16",
    )
    parser.add_argument(
        "--todos",
        action="store_true",
        help="Genera todos los graficos disponibles de los ejercicios 1 a 17.",
    )
    parser.add_argument(
        "--guardar",
        nargs="?",
        const=str(DEFAULT_OUTPUT_DIR),
        help="Guarda las figuras en PNG. Si no se indica carpeta, usa graficos_taller_04.",
    )
    return parser.parse_args()


def main():
    args = parsear_argumentos()

    if args.listar:
        listar_ejercicios()
        return

    cargar_dependencias(modo_guardar=bool(args.guardar))
    configurar_estilo()

    if args.ejercicio:
        numeros = []
        for numero in args.ejercicio:
            if numero in EJERCICIOS:
                numeros.append(numero)
            else:
                print(f"Ejercicio {numero} no disponible o no pide grafico.")
    elif args.todos or args.guardar:
        numeros = list(EJERCICIOS)
    else:
        numeros = pedir_ejercicios_por_menu()

    if not numeros:
        print("No se seleccionaron ejercicios.")
        return

    carpeta_salida = Path(args.guardar) if args.guardar else None
    ejecutar_ejercicios(numeros, carpeta_salida)


if __name__ == "__main__":
    main()
