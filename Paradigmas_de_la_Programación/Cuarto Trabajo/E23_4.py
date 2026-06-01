import pygame
import random

pygame.init()

ANCHO = 800
ALTO = 600

pantalla = pygame.display.set_mode((ANCHO, ALTO))

pygame.display.set_caption("Evita los enemigos")

clock = pygame.time.Clock()

fuente = pygame.font.SysFont(None, 50)

jugador = pygame.Rect(350, 500, 80, 80)

velocidad_jugador = 7

enemigo = pygame.Rect(
    random.randint(0,760),
    0,
    50,
    50
)

velocidad_enemigo = 5

puntos = 0

game_over = False

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

    if not game_over:

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
            jugador.x -= velocidad_jugador

        if teclas[pygame.K_RIGHT]:
            jugador.x += velocidad_jugador

        if jugador.x < 0:
            jugador.x = 0

        if jugador.x > 720:
            jugador.x = 720

        enemigo.y += velocidad_enemigo

        if enemigo.y > ALTO:

            enemigo.x = random.randint(0,760)
            enemigo.y = 0

            puntos += 100

            velocidad_enemigo += 0.5

        if jugador.colliderect(enemigo):

            game_over = True

    pantalla.fill("black")

    pygame.draw.rect(
        pantalla,
        "cyan",
        jugador
    )

    pygame.draw.rect(
        pantalla,
        "red",
        enemigo
    )

    texto_puntos = fuente.render(
        f"Puntos: {puntos}",
        True,
        "white"
    )

    pantalla.blit(texto_puntos, (10,10))

    if game_over:

        texto_game_over = fuente.render(
            "GAME OVER",
            True,
            "red"
        )

        pantalla.blit(
            texto_game_over,
            (260,250)
        )

    pygame.display.update()

    clock.tick(60)

pygame.quit()