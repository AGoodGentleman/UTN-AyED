import pygame
import numpy as np

pygame.init()

# =========================================================
# CONFIGURACIÓN
# =========================================================

ANCHO = 1400
ALTO = 750

screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Verlet + Masa Resorte")

clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 20)

DT = 0.016

GRAVEDAD = np.array([0, 980.0])

ITERACIONES = 8

# =========================================================
# FUNCIÓN LIMPIAR
# =========================================================

def limpiar(valor, epsilon=0.005):

    if abs(valor) < epsilon:
        return 0.0

    return valor

# =========================================================
# SLIDER
# =========================================================

class Slider:

    def __init__(
        self,
        x,
        y,
        ancho,
        minimo,
        maximo,
        valor,
        texto
    ):

        self.rect = pygame.Rect(x, y, ancho, 6)

        self.min = minimo
        self.max = maximo

        self.valor = valor

        self.texto = texto

        self.dragging = False

    # =====================================================

    def manejar_evento(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION:

            if self.dragging:

                mouse_x = event.pos[0]

                t = (
                    mouse_x - self.rect.x
                ) / self.rect.w

                t = max(0, min(1, t))

                self.valor = (
                    self.min
                    + t * (self.max - self.min)
                )

    # =====================================================

    def dibujar(self):

        pygame.draw.rect(
            screen,
            (100, 100, 100),
            self.rect
        )

        t = (
            self.valor - self.min
        ) / (
            self.max - self.min
        )

        knob_x = self.rect.x + t * self.rect.w

        pygame.draw.circle(
            screen,
            (255, 180, 80),
            (int(knob_x), self.rect.y + 3),
            10
        )

        texto = font.render(
            f"{self.texto}: {self.valor:.2f}",
            True,
            (255, 255, 255)
        )

        screen.blit(
            texto,
            (self.rect.x, self.rect.y - 30)
        )

# =========================================================
# PARTÍCULA
# =========================================================

class Particula:

    def __init__(self, x, y, fija=False):

        self.pos = np.array([x, y], dtype=float)

        self.pos_anterior = np.array([x, y], dtype=float)

        self.aceleracion = np.zeros(2)

        self.aceleracion_actual = np.zeros(2)

        self.fija = fija

        self.masa = 1.0

    # =====================================================

    def aplicar_fuerza(self, fuerza):

        a = fuerza / self.masa

        self.aceleracion += a

    # =====================================================

    def verlet(self):

        if self.fija:
            return

        # =====================================================
        # VELOCIDAD IMPLÍCITA
        # =====================================================

        velocidad = (
            self.pos - self.pos_anterior
        ) / DT

        # =====================================================
        # AMORTIGUADOR FÍSICO REAL
        # =====================================================

        # constante c
        c = slider_c.valor

        # Fd = -c*v
        fuerza_amortiguador = (
            -c * velocidad
        )

        # a = F/m
        aceleracion_amortiguador = (
            fuerza_amortiguador / self.masa
        )

        # =====================================================
        # ACELERACIÓN TOTAL
        # =====================================================

        aceleracion_total = (
            self.aceleracion
            + aceleracion_amortiguador
        )

        # =====================================================
        # ECUACIÓN DE VERLET
        # =====================================================

        nueva_pos = (
            self.pos
            + velocidad * DT
            + aceleracion_total * DT * DT
        )

        # =====================================================
        # ACTUALIZAR
        # =====================================================

        self.pos_anterior = self.pos.copy()

        self.pos = nueva_pos

        self.aceleracion_actual = (
            aceleracion_total.copy()
        )

        self.aceleracion = np.zeros(2)

    # =====================================================

    def dibujar(self):

        color = (255, 100, 100) if self.fija else (255, 255, 255)

        pygame.draw.circle(
            screen,
            color,
            self.pos.astype(int),
            6
        )

# =========================================================
# RESTRICCIÓN
# =========================================================

class Restriccion:

    def __init__(self, p1, p2):

        self.p1 = p1
        self.p2 = p2

        self.longitud = np.linalg.norm(
            p2.pos - p1.pos
        )

    # =====================================================

    def resolver(self):

        delta = self.p2.pos - self.p1.pos

        distancia = np.linalg.norm(delta)

        if distancia == 0:
            return

        diferencia = (
            self.longitud - distancia
        ) / distancia

        # =============================================
        # RIGIDEZ
        # =============================================

        rigidez = slider_rigidez.valor

        correccion = (
            delta
            * 0.5
            * diferencia
            * rigidez
        )

        if not self.p1.fija:
            self.p1.pos -= correccion

        if not self.p2.fija:
            self.p2.pos += correccion

    # =====================================================

    def dibujar(self):

        pygame.draw.line(
            screen,
            (200, 200, 200),
            self.p1.pos.astype(int),
            self.p2.pos.astype(int),
            2
        )

# =========================================================
# CREAR CUERDA
# =========================================================

particulas = []
restricciones = []

cantidad = 12
espaciado = 50

for i in range(cantidad):

    fija = (i == 0)

    p = Particula(
        250 + i * espaciado,
        150,
        fija
    )

    particulas.append(p)

for i in range(cantidad - 1):

    r = Restriccion(
        particulas[i],
        particulas[i + 1]
    )

    restricciones.append(r)

# =========================================================
# SLIDERS
# =========================================================

slider_rigidez = Slider(
    80,
    670,
    320,
    0.1,
    1.5,
    1.0,
    "Rigidez"
)

slider_k = Slider(
    540,
    670,
    320,
    100.0,
    1000.0,
    500.0,
    "Constante K"
)

slider_c = Slider(
    1000,
    670,
    320,
    0.0,
    10.0,
    5.0,
    "Constante C"
)

# =========================================================
# MOUSE
# =========================================================

particula_agarrada = None

fuerza_mouse = np.zeros(2)

# =========================================================
# LOOP PRINCIPAL
# =========================================================

running = True

while running:

    clock.tick(60)

    screen.fill((25, 25, 35))

    # =====================================================
    # EVENTOS
    # =====================================================

    for event in pygame.event.get():

        slider_rigidez.manejar_evento(event)
        slider_k.manejar_evento(event)
        slider_c.manejar_evento(event)

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse = np.array(
                pygame.mouse.get_pos(),
                dtype=float
            )

            for p in particulas:

                d = np.linalg.norm(
                    p.pos - mouse
                )

                if d < 20:

                    particula_agarrada = p

                    break

        if event.type == pygame.MOUSEBUTTONUP:

            particula_agarrada = None

            fuerza_mouse = np.zeros(2)

    # =====================================================
    # FUERZAS
    # =====================================================

    for p in particulas:

        fuerza_gravedad = GRAVEDAD * p.masa

        p.aplicar_fuerza(fuerza_gravedad)

    # =====================================================
    # FUERZA DEL MOUSE
    # =====================================================

    if particula_agarrada is not None:

        mouse = np.array(
            pygame.mouse.get_pos(),
            dtype=float
        )

        delta = mouse - particula_agarrada.pos

        k_mouse = slider_k.valor

        fuerza_mouse = delta * k_mouse

        particula_agarrada.aplicar_fuerza(
            fuerza_mouse
        )

    # =====================================================
    # VERLET
    # =====================================================

    for p in particulas:

        p.verlet()

    # =====================================================
    # RESTRICCIONES
    # =====================================================

    for _ in range(ITERACIONES):

        for r in restricciones:

            r.resolver()

    # =====================================================
    # DIBUJAR CUERDA
    # =====================================================

    for r in restricciones:
        r.dibujar()

    for p in particulas:
        p.dibujar()

    # =====================================================
    # VISUALIZAR FUERZA DEL MOUSE
    # =====================================================

    if particula_agarrada is not None:

        mouse = np.array(
            pygame.mouse.get_pos(),
            dtype=float
        )

        pygame.draw.line(
            screen,
            (100, 255, 100),
            particula_agarrada.pos.astype(int),
            mouse.astype(int),
            3
        )

    # =====================================================
    # DATOS FÍSICOS
    # =====================================================

    p = particulas[-1]

    velocidad = (
        p.pos - p.pos_anterior
    ) / DT

    rapidez = np.linalg.norm(velocidad)

    aceleracion = p.aceleracion_actual

    # =====================================================
    # TEXTO
    # =====================================================

    texto = [

        "MODELO VERLET",
        "",

        "x_new = 2*x - x_old + a*dt^2",
        "",

        f"dt = {DT:.3f}",
        "",

        "PARTICULA FINAL",
        "",

        f"x  = {p.pos[0]:.2f} px",
        f"y  = {p.pos[1]:.2f} px",
        "",

        f"vx = {limpiar(velocidad[0]/100):.2f} m/s",
        f"vy = {limpiar(velocidad[1]/100):.2f} m/s",
        "",

        f"|v| = {rapidez/100:.2f}",
        "",

        f"ax = {limpiar(aceleracion[0]/100):.2f} m/s²",
        f"ay = {limpiar(aceleracion[1]/100):.2f} m/s²",
        "",

        "FUERZA DEL MOUSE",
        "",

        f"Fx = {limpiar(fuerza_mouse[0]/10000):.2f} N",
        f"Fy = {limpiar(fuerza_mouse[1]/10000):.2f} N",
    ]

    y = 20

    for linea in texto:

        render = font.render(
            linea,
            True,
            (255, 255, 255)
        )

        screen.blit(render, (820, y))

        y += 28

    # =====================================================
    # DIBUJAR SLIDERS
    # =====================================================

    slider_rigidez.dibujar()
    slider_k.dibujar()
    slider_c.dibujar()

    # =====================================================
    # UPDATE
    # =====================================================

    pygame.display.flip()

pygame.quit()