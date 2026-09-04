"""Graficos del Taller 05 - ejercicios 15 al 25.

El script genera los graficos pedidos directamente en el taller y algunos
apoyos visuales para funciones del mismo tramo.

Uso rapido:
    python taller_05_graficos_15_25.py --guardar
    python taller_05_graficos_15_25.py --pedidos --guardar
    python taller_05_graficos_15_25.py --ejercicio 15 16 19 --guardar
    python taller_05_graficos_15_25.py --listar
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


DEFAULT_OUTPUT_DIR = Path(__file__).with_name("graficos_taller_05_15_25")
# Terna derecha estilo hoja: z hacia arriba, y hacia la derecha,
# x en diagonal hacia abajo-izquierda.
VISTA_ELEV = 7
VISTA_AZIM = 7
VISTA_ROLL = -1
COLOR_SUPERFICIE = "#4c78a8"
COLOR_CURVA_1 = "#f58518"
COLOR_CURVA_2 = "#54a24b"
COLOR_TANGENTE = "#e45756"
COLOR_PUNTO = "#b279a2"


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


def malla_xy(xlim, ylim, n=80):
    x = np.linspace(xlim[0], xlim[1], n)
    y = np.linspace(ylim[0], ylim[1], n)
    return np.meshgrid(x, y)


def malla_xz(xlim, zlim, n=80):
    x = np.linspace(xlim[0], xlim[1], n)
    z = np.linspace(zlim[0], zlim[1], n)
    return np.meshgrid(x, z)


def configurar_3d(
    ax,
    titulo,
    xlim,
    ylim,
    zlim,
    elev=VISTA_ELEV,
    azim=VISTA_AZIM,
    roll=VISTA_ROLL,
    etiquetas=("x", "y", "z"),
):
    ax.set_title(titulo)
    ax.set_xlabel(etiquetas[0])
    ax.set_ylabel(etiquetas[1])
    ax.set_zlabel(etiquetas[2])
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_zlim(*zlim)
    try:
        ax.view_init(elev=elev, azim=azim, roll=roll)
    except TypeError:
        ax.view_init(elev=elev, azim=azim)
    ax.grid(True)
    try:
        ax.set_proj_type("ortho")
    except Exception:
        pass

    agregar_ejes_coordenados(ax, xlim, ylim, zlim, etiquetas)
    agregar_terna_cuaderno(ax)


def valor_eje_origen(limite):
    if limite[0] <= 0 <= limite[1]:
        return 0
    return limite[0]


def agregar_ejes_coordenados(ax, xlim, ylim, zlim, etiquetas):
    origen = (
        valor_eje_origen(xlim),
        valor_eje_origen(ylim),
        valor_eje_origen(zlim),
    )
    extremos = [
        (xlim[1], origen[1], origen[2]),
        (origen[0], ylim[1], origen[2]),
        (origen[0], origen[1], zlim[1]),
    ]
    color = "0.15"
    for etiqueta, extremo in zip(etiquetas, extremos):
        dx = extremo[0] - origen[0]
        dy = extremo[1] - origen[1]
        dz = extremo[2] - origen[2]
        if abs(dx) + abs(dy) + abs(dz) < 1e-9:
            continue
        ax.quiver(
            *origen,
            dx,
            dy,
            dz,
            color=color,
            linewidth=1.6,
            arrow_length_ratio=0.075,
            normalize=False,
        )
        ax.text(
            extremo[0],
            extremo[1],
            extremo[2],
            f" {etiqueta}",
            color=color,
            fontsize=10,
            fontstyle="italic",
        )


def agregar_terna_cuaderno(ax):
    origen = (0.18, 0.22)
    ejes = [
        ("z", (0.18, 0.39)),
        ("y", (0.39, 0.22)),
        ("x", (0.055, 0.055)),
    ]
    for etiqueta, destino in ejes:
        ax.annotate(
            "",
            xy=destino,
            xytext=origen,
            xycoords="axes fraction",
            textcoords="axes fraction",
            arrowprops={
                "arrowstyle": "-|>",
                "linewidth": 1.3,
                "color": "0.2",
                "shrinkA": 0,
                "shrinkB": 0,
            },
            annotation_clip=False,
        )
        dx = destino[0] - origen[0]
        dy = destino[1] - origen[1]
        ax.text2D(
            destino[0] + 0.025 * (1 if dx >= 0 else -1),
            destino[1] + 0.025 * (1 if dy >= 0 else -1),
            etiqueta,
            transform=ax.transAxes,
            color="0.2",
            fontsize=10,
            fontstyle="italic",
            clip_on=False,
        )
    try:
        ax.set_box_aspect(
            (xlim[1] - xlim[0], ylim[1] - ylim[0], zlim[1] - zlim[0])
        )
    except Exception:
        pass


def configurar_2d(ax, titulo, xlabel="x", ylabel="z"):
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.axhline(0, color="0.25", linewidth=0.8)
    ax.axvline(0, color="0.25", linewidth=0.8)


def plot_superficie(ax, xlim, ylim, funcion, n=75, alpha=0.72, cmap="viridis"):
    x, y = malla_xy(xlim, ylim, n)
    z = funcion(x, y)
    ax.plot_surface(x, y, z, cmap=cmap, alpha=alpha, linewidth=0, antialiased=True)
    return x, y, z


def plano_x(ax, x0, ylim, zlim, color="#72b7b2", alpha=0.14):
    y, z = np.meshgrid(
        np.linspace(ylim[0], ylim[1], 2),
        np.linspace(zlim[0], zlim[1], 2),
    )
    x = np.full_like(y, x0)
    ax.plot_surface(x, y, z, color=color, alpha=alpha, linewidth=0)


def plano_y(ax, y0, xlim, zlim, color="#ff9da6", alpha=0.14):
    x, z = np.meshgrid(
        np.linspace(xlim[0], xlim[1], 2),
        np.linspace(zlim[0], zlim[1], 2),
    )
    y = np.full_like(x, y0)
    ax.plot_surface(x, y, z, color=color, alpha=alpha, linewidth=0)


def agregar_punto(ax, x, y, z, etiqueta, color=COLOR_PUNTO):
    ax.scatter([x], [y], [z], color=color, s=45, depthshade=False)
    ax.text(x, y, z, f"  {etiqueta}", color=color, fontsize=9)


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


def resistencia_total(r1, r2, r3):
    return 1 / (1 / r1 + 1 / r2 + 1 / r3)


def ejercicio_15():
    fig = plt.figure(figsize=(14, 7))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    xlim = (-1.5, 3.2)
    ylim = (-0.5, 4.7)
    zlim = (0, 24)
    configurar_3d(
        ax,
        "E15 - z = 2x^2 + y^2 con secciones y tangentes",
        xlim,
        ylim,
        zlim,
    )
    plot_superficie(ax, xlim, ylim, lambda x, y: 2 * x**2 + y**2, n=85, alpha=0.58)
    plano_y(ax, 2, xlim, zlim)
    plano_x(ax, 1, ylim, zlim)

    t_x = np.linspace(xlim[0], xlim[1], 260)
    t_y = np.linspace(ylim[0], ylim[1], 260)
    ax.plot(t_x, np.full_like(t_x, 2), 2 * t_x**2 + 4, color=COLOR_CURVA_1, linewidth=3, label="C1: y=2")
    ax.plot(np.full_like(t_y, 1), t_y, 2 + t_y**2, color=COLOR_CURVA_2, linewidth=3, label="C2: x=1")

    s = np.linspace(-1.1, 1.1, 120)
    ax.plot(1 + s, np.full_like(s, 2), 6 + 4 * s, color=COLOR_TANGENTE, linewidth=3, label="Tangente C1")
    ax.plot(np.full_like(s, 1), 2 + s, 6 + 4 * s, color="#d62728", linewidth=3, linestyle="--", label="Tangente C2")
    agregar_punto(ax, 1, 2, 6, "P(1,2,6)")
    ax.legend(loc="upper left")

    ax2 = fig.add_subplot(2, 2, 2)
    configurar_2d(ax2, "Seccion y=2: z=2x^2+4", xlabel="x", ylabel="z")
    x = np.linspace(-1.5, 3.2, 400)
    ax2.plot(x, 2 * x**2 + 4, color=COLOR_CURVA_1, linewidth=2.5, label="curva")
    ax2.plot(x, 4 * x + 2, color=COLOR_TANGENTE, linewidth=2, label="tangente z=4x+2")
    ax2.scatter([1], [6], color=COLOR_PUNTO, zorder=5)
    ax2.legend()

    ax3 = fig.add_subplot(2, 2, 4)
    configurar_2d(ax3, "Seccion x=1: z=2+y^2", xlabel="y", ylabel="z")
    y = np.linspace(-0.5, 4.7, 400)
    ax3.plot(y, 2 + y**2, color=COLOR_CURVA_2, linewidth=2.5, label="curva")
    ax3.plot(y, 4 * y - 2, color=COLOR_TANGENTE, linewidth=2, label="tangente z=4y-2")
    ax3.scatter([2], [6], color=COLOR_PUNTO, zorder=5)
    ax3.legend()
    return fig


def ejercicio_16():
    fig = plt.figure(figsize=(14, 7))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    xlim = (0, 6)
    ylim = (-1, 5)
    zlim = (0, 10)
    configurar_3d(
        ax,
        "E16 - 36z = 4x^2 + 9y^2 con secciones y tangentes",
        xlim,
        ylim,
        zlim,
    )
    plot_superficie(ax, xlim, ylim, lambda x, y: x**2 / 9 + y**2 / 4, n=85, alpha=0.58)
    plano_x(ax, 3, ylim, zlim)
    plano_y(ax, 2, xlim, zlim)

    y = np.linspace(ylim[0], ylim[1], 260)
    x = np.linspace(xlim[0], xlim[1], 260)
    ax.plot(np.full_like(y, 3), y, 1 + y**2 / 4, color=COLOR_CURVA_1, linewidth=3, label="C1: x=3")
    ax.plot(x, np.full_like(x, 2), x**2 / 9 + 1, color=COLOR_CURVA_2, linewidth=3, label="C2: y=2")

    s = np.linspace(-1.25, 1.25, 120)
    ax.plot(np.full_like(s, 3), 2 + s, 2 + s, color=COLOR_TANGENTE, linewidth=3, label="Tangente C1")
    ax.plot(3 + s, np.full_like(s, 2), 2 + (2 / 3) * s, color="#d62728", linewidth=3, linestyle="--", label="Tangente C2")
    agregar_punto(ax, 3, 2, 2, "P(3,2,2)")
    ax.legend(loc="upper left")

    ax2 = fig.add_subplot(2, 2, 2)
    configurar_2d(ax2, "Seccion x=3: z=1+y^2/4", xlabel="y", ylabel="z")
    y = np.linspace(-1, 5, 400)
    ax2.plot(y, 1 + y**2 / 4, color=COLOR_CURVA_1, linewidth=2.5, label="curva")
    ax2.plot(y, y, color=COLOR_TANGENTE, linewidth=2, label="tangente z=y")
    ax2.scatter([2], [2], color=COLOR_PUNTO, zorder=5)
    ax2.legend()

    ax3 = fig.add_subplot(2, 2, 4)
    configurar_2d(ax3, "Seccion y=2: z=x^2/9+1", xlabel="x", ylabel="z")
    x = np.linspace(0, 6, 400)
    ax3.plot(x, x**2 / 9 + 1, color=COLOR_CURVA_2, linewidth=2.5, label="curva")
    ax3.plot(x, 2 + (2 / 3) * (x - 3), color=COLOR_TANGENTE, linewidth=2, label="tangente")
    ax3.scatter([3], [2], color=COLOR_PUNTO, zorder=5)
    ax3.legend()
    return fig


def ejercicio_17():
    fig = plt.figure(figsize=(13, 6.8))

    ax = fig.add_subplot(1, 2, 1, projection="3d")
    xlim = (-6, 6)
    ylim = (-6, 6)
    zlim = (0, 1.15)
    configurar_3d(ax, "E17 - Potencial U=1/sqrt(x^2+y^2)", xlim, ylim, zlim)
    x, y = malla_xy(xlim, ylim, 120)
    r = np.sqrt(x**2 + y**2)
    z = np.where(r < 0.75, np.nan, 1 / r)
    ax.plot_surface(x, y, z, cmap="magma", alpha=0.82, linewidth=0)
    agregar_punto(ax, 3, 4, 1 / 5, "P(3,4)")

    ax2 = fig.add_subplot(1, 2, 2)
    configurar_2d(ax2, "Curvas de nivel y direcciones pedidas", xlabel="x", ylabel="y")
    ax2.set_aspect("equal", adjustable="box")
    x, y = malla_xy(xlim, ylim, 220)
    r = np.sqrt(x**2 + y**2)
    u = np.where(r < 0.4, np.nan, 1 / r)
    cs = ax2.contour(x, y, u, levels=[0.15, 0.2, 0.25, 0.33, 0.5, 0.8], cmap="magma")
    ax2.clabel(cs, inline=True, fontsize=8)
    ax2.scatter([3], [4], color=COLOR_PUNTO, zorder=5, label="P(3,4)")
    ax2.arrow(3, 4, 1.2, 0, head_width=0.18, color=COLOR_CURVA_1, length_includes_head=True, label="direccion x")
    ax2.arrow(3, 4, 0, 1.2, head_width=0.18, color=COLOR_CURVA_2, length_includes_head=True, label="direccion y")
    ax2.legend()
    return fig


def ejercicio_18():
    fig = plt.figure(figsize=(13, 6.8))
    llim = (100, 2000)
    klim = (100, 1200)
    zlim = (0, 170000)

    def produccion(l, k):
        return 100 * l**0.75 * k**0.25

    ax = fig.add_subplot(1, 2, 1, projection="3d")
    configurar_3d(ax, "E18 - Cobb-Douglas P(L,K)", llim, klim, zlim, etiquetas=("L", "K", "P"))
    l, k = malla_xy(llim, klim, 90)
    p = produccion(l, k)
    ax.plot_surface(l, k, p, cmap="viridis", alpha=0.78, linewidth=0)
    ax.set_xlabel("L")
    ax.set_ylabel("K")
    ax.set_zlabel("P")
    agregar_punto(ax, 1000, 500, produccion(1000, 500), "base")

    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_title("Curvas de nivel de produccion")
    ax2.set_xlabel("L")
    ax2.set_ylabel("K")
    cs = ax2.contour(l, k, p, levels=8, cmap="viridis")
    ax2.clabel(cs, inline=True, fontsize=8)
    ax2.scatter([1000], [500], color=COLOR_PUNTO, zorder=5, label="(L,K)=(1000,500)")
    ax2.legend()
    return fig


def ejercicio_19():
    fig = plt.figure(figsize=(13, 10))
    xlim = (-2, 2)
    ylim = (-2, 2)

    ax1 = fig.add_subplot(2, 2, 1, projection="3d")
    configurar_3d(ax1, "E19.a - z = sqrt(y^2) = |y|", xlim, ylim, (0, 2.4))
    plot_superficie(ax1, xlim, ylim, lambda x, y: np.abs(y), n=90, alpha=0.78)
    agregar_punto(ax1, 0, 0, 0, "O")

    ax2 = fig.add_subplot(2, 2, 2, projection="3d")
    configurar_3d(ax2, "E19.b - z = cbrt(x^2)", xlim, ylim, (0, 1.9))
    plot_superficie(ax2, xlim, ylim, lambda x, y: np.cbrt(x**2), n=90, alpha=0.78)
    agregar_punto(ax2, 0, 0, 0, "O")

    ax3 = fig.add_subplot(2, 2, 3, projection="3d")
    configurar_3d(ax3, "E19.c - f=3x^3/(x^2+y^2), f(0,0)=0", xlim, ylim, (-3, 3))
    x, y = malla_xy(xlim, ylim, 100)
    den = x**2 + y**2
    z = np.where(den < 1e-8, 0, 3 * x**3 / den)
    ax3.plot_surface(x, y, z, cmap="coolwarm", alpha=0.82, linewidth=0)
    agregar_punto(ax3, 0, 0, 0, "O")

    ax4 = fig.add_subplot(2, 2, 4, projection="3d")
    configurar_3d(ax4, "E19.d - 1 sobre los ejes, 0 fuera de ellos", xlim, ylim, (-0.15, 1.25))
    x, y = malla_xy(xlim, ylim, 2)
    ax4.plot_surface(x, y, np.zeros_like(x), color=COLOR_SUPERFICIE, alpha=0.18, linewidth=0)
    t = np.linspace(-2, 2, 250)
    ax4.plot(t, np.zeros_like(t), np.ones_like(t), color=COLOR_CURVA_1, linewidth=3, label="eje x")
    ax4.plot(np.zeros_like(t), t, np.ones_like(t), color=COLOR_CURVA_2, linewidth=3, label="eje y")
    agregar_punto(ax4, 0, 0, 1, "O")
    ax4.legend(loc="upper left")
    return fig


def ejercicio_21():
    fig = plt.figure(figsize=(8.5, 6.5))
    ax = fig.add_subplot(111, projection="3d")
    xlim = (-1.4, 1.4)
    ylim = (-1.7, 1.7)
    zlim = (0, 24)
    configurar_3d(ax, "E21 - z=x^2y^2-y^3+3x^4+5", xlim, ylim, zlim)
    plot_superficie(ax, xlim, ylim, lambda x, y: x**2 * y**2 - y**3 + 3 * x**4 + 5, n=100, alpha=0.82)
    return fig


def ejercicio_23():
    fig = plt.figure(figsize=(8.5, 6.5))
    ax = fig.add_subplot(111, projection="3d")
    xlim = (-2.5, 2.5)
    zlim = (0.25, 3.7)
    x, z = malla_xz(xlim, zlim, 110)
    y = x * z - np.log(z) - x
    ylim = (float(np.nanmin(y)), float(np.nanmax(y)))
    configurar_3d(ax, "E23 - xz-ln(z)=x+y, parametrizada con z>0", xlim, ylim, zlim)
    ax.plot_surface(x, y, z, cmap="plasma", alpha=0.82, linewidth=0)
    return fig


def ejercicio_24():
    fig = plt.figure(figsize=(8.5, 6.5))
    ax = fig.add_subplot(111, projection="3d")
    xlim = (-2.2, 2.2)
    zlim = (-0.5, 2.3)
    x, z = malla_xz(xlim, zlim, 110)
    y = x * (2 * z - 1) / (1 + z**3)
    ylim = (-3.5, 3.5)
    y = np.where(np.abs(y) > 3.5, np.nan, y)
    configurar_3d(ax, "E24 - x+y+yz^3-2xz=0", xlim, ylim, zlim)
    ax.plot_surface(x, y, z, cmap="cividis", alpha=0.82, linewidth=0)
    agregar_punto(ax, 1, 1, 1, "punto dado", color=COLOR_TANGENTE)
    ax.text(
        -2.1,
        -3.2,
        2.15,
        "Aviso: F(1,1,1)=1 con la ecuacion escrita.",
        color=COLOR_TANGENTE,
        fontsize=8,
    )
    return fig


def ejercicio_25():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.8))
    r1, r2, r3 = 15, 30, 45
    base = resistencia_total(r1, r2, r3)
    valores = np.linspace(5, 80, 500)
    curvas = [
        ("varia R1", valores, resistencia_total(valores, r2, r3), r1),
        ("varia R2", valores, resistencia_total(r1, valores, r3), r2),
        ("varia R3", valores, resistencia_total(r1, r2, valores), r3),
    ]
    for etiqueta, xs, ys, inicial in curvas:
        ax1.plot(xs, ys, linewidth=2.4, label=etiqueta)
        ax1.scatter([inicial], [base], s=38)
    ax1.set_title("E25 - R total al variar una resistencia")
    ax1.set_xlabel("resistencia variable (ohm)")
    ax1.set_ylabel("R total (ohm)")
    ax1.axhline(base, color="0.35", linestyle=":", linewidth=1)
    ax1.legend()

    derivadas = [
        base**2 / r1**2,
        base**2 / r2**2,
        base**2 / r3**2,
    ]
    barras = ax2.bar(["dR/dR1", "dR/dR2", "dR/dR3"], derivadas, color=[COLOR_CURVA_1, COLOR_CURVA_2, COLOR_TANGENTE])
    ax2.set_title("Sensibilidad en R1=15, R2=30, R3=45")
    ax2.set_ylabel("ohm de R total por ohm incrementado")
    ax2.grid(axis="y", alpha=0.25)
    for barra, valor in zip(barras, derivadas):
        ax2.text(barra.get_x() + barra.get_width() / 2, valor, f"{valor:.4f}", ha="center", va="bottom", fontsize=9)
    return fig


EJERCICIOS = {
    15: ("Superficie, secciones y tangentes", ejercicio_15, "e15_superficie_tangentes", True),
    16: ("Superficie eliptica, secciones y tangentes", ejercicio_16, "e16_superficie_tangentes", True),
    17: ("Potencial electrostatico", ejercicio_17, "e17_potencial", False),
    18: ("Produccion Cobb-Douglas", ejercicio_18, "e18_cobb_douglas", False),
    19: ("Continuidad y derivadas parciales en el origen", ejercicio_19, "e19_continuidad", True),
    21: ("Superficie para derivadas mixtas", ejercicio_21, "e21_derivadas_mixtas", False),
    23: ("Superficie implicita xz-ln(z)=x+y", ejercicio_23, "e23_implicita", False),
    24: ("Superficie implicita con punto dado", ejercicio_24, "e24_implicita", False),
    25: ("Resistores en paralelo", ejercicio_25, "e25_resistores", False),
}


NOTAS = {
    15: [
        "Plano y=2: C1=(t,2,2t^2+4), tangente r=(1,2,6)+s(1,0,4).",
        "Plano x=1: C2=(1,t,2+t^2), tangente r=(1,2,6)+s(0,1,4).",
    ],
    16: [
        "Plano x=3: C1=(3,t,1+t^2/4), tangente r=(3,2,2)+s(0,1,1).",
        "Plano y=2: C2=(t,2,t^2/9+1), tangente r=(3,2,2)+s(1,0,2/3).",
    ],
    17: [
        "En P(3,4): Ux=-3/125=-0.024 y Uy=-4/125=-0.032.",
    ],
    18: [
        "En L=1000, K=500: P_L=63.0689 y P_K=42.0459 aproximadamente.",
    ],
    19: [
        "E19.a y E19.b muestran cuspides: algunas derivadas parciales fallan en el origen.",
        "E19.d es discontinuo: vale 1 sobre los ejes y 0 fuera de ellos.",
    ],
    24: [
        "Aviso: con la ecuacion extraida del PDF, F(1,1,1)=1. El punto dado no cae en la superficie.",
    ],
    25: [
        "R base = 90/11 = 8.1818 ohm.",
        "dR/dR1=36/121, dR/dR2=9/121, dR/dR3=4/121; variar R1 produce el mayor cambio.",
    ],
}


def ejercicios_pedidos_directamente():
    return [numero for numero, (_, _, _, pedido) in EJERCICIOS.items() if pedido]


def listar_ejercicios():
    print("Ejercicios disponibles para graficar:")
    for numero, (titulo, _, _, pedido) in EJERCICIOS.items():
        marca = "pedido directo" if pedido else "apoyo visual"
        print(f"  {numero:>2} - {titulo} ({marca})")
    omitidos = [20, 22]
    print(f"\nNo se incluyen {omitidos} porque solo piden calculo simbolico.")


def pedir_ejercicios_por_menu():
    listar_ejercicios()
    texto = input("\nIngrese numeros separados por coma/espacio, 'pedidos' o 'todos': ").strip().lower()
    if texto in {"pedidos", "pedido", "p"}:
        return ejercicios_pedidos_directamente()
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
            print(f"Ejercicio {numero} no disponible o no pide grafico util.")
    return elegidos


def normalizar_figuras(resultado):
    if isinstance(resultado, list):
        return resultado
    return [resultado]


def ejecutar_ejercicios(numeros, carpeta_salida=None):
    for numero in numeros:
        titulo, funcion, nombre_base, _ = EJERCICIOS[numero]
        print(f"\nGenerando E{numero}: {titulo}")
        for nota in NOTAS.get(numero, []):
            print(f"  {nota}")
        figuras = normalizar_figuras(funcion())
        for indice, fig in enumerate(figuras, start=1):
            sufijo = "" if len(figuras) == 1 else f"_{indice}"
            guardar_o_mostrar(fig, f"{nombre_base}{sufijo}", carpeta_salida)


def parsear_argumentos():
    parser = argparse.ArgumentParser(
        description="Grafica los ejercicios 15 al 25 del Taller 05."
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
        help="Numeros de ejercicios a graficar. Ejemplo: --ejercicio 15 16 19",
    )
    parser.add_argument(
        "--pedidos",
        action="store_true",
        help="Genera solo los graficos pedidos directamente por la consigna: 15, 16 y 19.",
    )
    parser.add_argument(
        "--todos",
        action="store_true",
        help="Genera todos los graficos disponibles entre los ejercicios 15 y 25.",
    )
    parser.add_argument(
        "--guardar",
        nargs="?",
        const=str(DEFAULT_OUTPUT_DIR),
        help="Guarda las figuras en PNG. Si no se indica carpeta, usa graficos_taller_05_15_25.",
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
                print(f"Ejercicio {numero} no disponible o no pide grafico util.")
    elif args.pedidos:
        numeros = ejercicios_pedidos_directamente()
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
