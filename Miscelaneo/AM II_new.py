import pygame
from pygame.math import Vector2

# =========================================================
# CONFIGURACIÓN
# =========================================================

WIDTH, HEIGHT = 1300, 800
FPS = 60

BACKGROUND = (20, 20, 30)

GRAVITY = Vector2(0, 900)

NODE_RADIUS = 8
SEGMENT_LENGTH = 40
NUM_NODES = 14

FONT_SIZE = 18


# =========================================================
# SLIDER
# =========================================================

class Slider:

    def __init__(self, x, y, w,
                 min_val, max_val,
                 start_val, text):

        self.rect = pygame.Rect(x, y, w, 6)

        self.handle_x = x
        self.radius = 10

        self.min_val = min_val
        self.max_val = max_val

        self.value = start_val

        self.text = text

        self.dragging = False

        self.set_value(start_val)

    def set_value(self, value):

        self.value = max(
            self.min_val,
            min(self.max_val, value)
        )

        t = (
            (self.value - self.min_val) /
            (self.max_val - self.min_val)
        )

        self.handle_x = self.rect.x + t * self.rect.w

    def update(self, mouse_pressed, mouse_pos):

        handle_pos = Vector2(
            self.handle_x,
            self.rect.centery
        )

        if mouse_pressed:

            if (handle_pos - mouse_pos).length() < 15:
                self.dragging = True

        else:
            self.dragging = False

        if self.dragging:

            self.handle_x = max(
                self.rect.x,
                min(self.rect.x + self.rect.w,
                    mouse_pos.x)
            )

            t = (
                (self.handle_x - self.rect.x)
                / self.rect.w
            )

            self.value = (
                self.min_val +
                t * (self.max_val - self.min_val)
            )

    def draw(self, screen, font):

        pygame.draw.rect(
            screen,
            (120, 120, 120),
            self.rect
        )

        pygame.draw.circle(
            screen,
            (220, 220, 220),
            (int(self.handle_x), self.rect.centery),
            self.radius
        )

        txt = f"{self.text}: {self.value:.3f}"

        surf = font.render(
            txt,
            True,
            (255, 255, 255)
        )

        screen.blit(
            surf,
            (self.rect.x, self.rect.y - 28)
        )


# =========================================================
# NODO
# =========================================================

class Node:

    def __init__(self, x, y, locked=False):

        self.pos = Vector2(x, y)

        self.old_pos = Vector2(x, y)

        self.external_force = Vector2(0, 0)

        self.locked = locked

    def velocity(self, dt):

        return (
            (self.pos - self.old_pos) / dt
        )

    def update(self, dt, b):

        if self.locked:
            return

        vel = self.pos - self.old_pos

        # amortiguador
        vel *= b

        total_acc = (
            GRAVITY +
            self.external_force
        )

        new_pos = (
            self.pos +
            vel +
            total_acc * (dt * dt)
        )

        self.old_pos = self.pos.copy()

        self.pos = new_pos

    def constrain_screen(self):

        if self.locked:
            return

        bounce = 0.5

        vel = self.pos - self.old_pos

        if self.pos.x < 0:

            self.pos.x = 0

            self.old_pos.x = (
                self.pos.x +
                vel.x * bounce
            )

        elif self.pos.x > WIDTH:

            self.pos.x = WIDTH

            self.old_pos.x = (
                self.pos.x +
                vel.x * bounce
            )

        if self.pos.y < 0:

            self.pos.y = 0

            self.old_pos.y = (
                self.pos.y +
                vel.y * bounce
            )

        elif self.pos.y > HEIGHT:

            self.pos.y = HEIGHT

            self.old_pos.y = (
                self.pos.y +
                vel.y * bounce
            )


# =========================================================
# SEGMENTO
# =========================================================

class Segment:

    def __init__(self, a, b, length):

        self.a = a
        self.b = b

        self.length = length

    def solve(self, stiffness):

        delta = self.b.pos - self.a.pos

        dist = delta.length()

        if dist == 0:
            return

        diff = (
            (dist - self.length) / dist
        )

        correction = (
            delta *
            0.5 *
            diff *
            stiffness
        )

        if not self.a.locked:
            self.a.pos += correction

        if not self.b.locked:
            self.b.pos -= correction


# =========================================================
# CREAR CADENA
# =========================================================

def create_chain():

    nodes = []
    segments = []

    start_x = 500
    start_y = 120

    for i in range(NUM_NODES):

        locked = (i == 0)

        n = Node(
            start_x,
            start_y + i * SEGMENT_LENGTH,
            locked
        )

        nodes.append(n)

        if i > 0:

            s = Segment(
                nodes[i - 1],
                nodes[i],
                SEGMENT_LENGTH
            )

            segments.append(s)

    return nodes, segments


# =========================================================
# MAIN
# =========================================================

def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption(
        "Cadena Verlet"
    )

    clock = pygame.time.Clock()

    font = pygame.font.SysFont(
        "consolas",
        FONT_SIZE
    )

    small_font = pygame.font.SysFont(
        "consolas",
        16
    )

    nodes, segments = create_chain()

    # =====================================================
    # SLIDERS
    # =====================================================

    stiffness_slider = Slider(
        920, 100, 250,
        0.1, 1.0,
        0.9,
        "Rigidez"
    )

    b_slider = Slider(
        920, 180, 250,
        0.90, 1.0,
        0.995,
        "b Amortiguador"
    )

    k_slider = Slider(
        920, 260, 250,
        0.1, 5.0,
        1.0,
        "k Resorte"
    )

    selected_node = None

    running = True

    while running:

        dt = clock.tick(FPS) / 1000.0

        mouse_pos = Vector2(
            pygame.mouse.get_pos()
        )

        mouse_pressed = pygame.mouse.get_pressed()[0]

        # =================================================
        # EVENTOS
        # =================================================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                for n in nodes:

                    if (
                        (n.pos - mouse_pos).length()
                        < 20
                    ):

                        selected_node = n
                        break

            if event.type == pygame.MOUSEBUTTONUP:
                selected_node = None

        # =================================================
        # UPDATE SLIDERS
        # =================================================

        stiffness_slider.update(
            mouse_pressed,
            mouse_pos
        )

        b_slider.update(
            mouse_pressed,
            mouse_pos
        )

        k_slider.update(
            mouse_pressed,
            mouse_pos
        )

        stiffness = stiffness_slider.value

        b = b_slider.value

        k = k_slider.value

        # =================================================
        # FUERZA EXTERNA
        # =================================================

        for n in nodes:
            n.external_force = Vector2(0, 0)

        if (
            selected_node and
            not selected_node.locked
        ):

            displacement = (
                mouse_pos -
                selected_node.pos
            )

            force = displacement * k * 8

            selected_node.external_force = force

        # =================================================
        # UPDATE NODOS
        # =================================================

        for n in nodes:
            n.update(dt, b)

        # =================================================
        # CONSTRAINTS
        # =================================================

        iterations = 12

        for _ in range(iterations):

            for s in segments:
                s.solve(stiffness)

            for n in nodes:
                n.constrain_screen()

        # =================================================
        # DIBUJO
        # =================================================

        screen.fill(BACKGROUND)

        # ---------------- SEGMENTOS ----------------

        for s in segments:

            pygame.draw.line(
                screen,
                (220, 220, 220),
                s.a.pos,
                s.b.pos,
                3
            )

        # ---------------- NODOS ----------------

        for n in nodes:

            color = (
                (255, 80, 80)
                if n.locked
                else
                (80, 200, 255)
            )

            pygame.draw.circle(
                screen,
                color,
                (int(n.pos.x), int(n.pos.y)),
                NODE_RADIUS
            )

        # =================================================
        # DIBUJAR SLIDERS
        # =================================================

        stiffness_slider.draw(screen, font)

        b_slider.draw(screen, font)

        k_slider.draw(screen, font)

        # =================================================
        # ECUACIONES
        # =================================================

        eq1 = "m*x'' + b*x' + k*x = Fext"
        eq2 = "x(t+dt)=x(t)+(x(t)-x(t-dt))*b+a*dt²"

        surf1 = small_font.render(
            eq1,
            True,
            (255, 255, 120)
        )

        surf2 = small_font.render(
            eq2,
            True,
            (255, 255, 120)
        )

        screen.blit(surf1, (880, 340))
        screen.blit(surf2, (880, 370))

        # =================================================
        # INFO DEL ÚLTIMO NODO
        # =================================================

        target = nodes[-1]

        vel = target.velocity(dt)

        rapidez = vel.length()

        info = [

            f"PosX: {target.pos.x:.2f} px",
            f"PosY: {target.pos.y:.2f} px",

            f"VelX: {vel.x:.2f} px/s",
            f"VelY: {vel.y:.2f} px/s",

            f"Rapidez: {rapidez:.2f} px/s",

            f"FextX: {target.external_force.x:.2f} N",
            f"FextY: {target.external_force.y:.2f} N",

        ]

        y = 450

        for txt in info:

            surf = font.render(
                txt,
                True,
                (255, 255, 255)
            )

            screen.blit(
                surf,
                (920, y)
            )

            y += 30

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()