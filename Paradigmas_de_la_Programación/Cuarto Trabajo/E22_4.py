import pygame
import random

pygame.init()

ANCHO = 800
ALTO = 600

pantalla = pygame.display.set_mode((ANCHO, ALTO))

pygame.display.set_caption("Catching Stars")

clock = pygame.time.Clock()

fuente = pygame.font.SysFont(None, 40)

jugador = pygame.Rect(350, 500, 80, 80)

velocidad_jugador = 7

estrella = pygame.Rect(
    random.randint(0, 760),
    0,
    40,
    40
)

velocidad_estrella = 5

puntos = 0

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        jugador.x -= velocidad_jugador

    if teclas[pygame.K_RIGHT]:
        jugador.x += velocidad_jugador

    if jugador.x < 0:
        jugador.x = 0

    if jugador.x > 720:
        jugador.x = 720

    estrella.y += velocidad_estrella

    if estrella.y > ALTO:

        estrella.x = random.randint(0, 760)
        estrella.y = 0

    if jugador.colliderect(estrella):

        puntos += 100

        estrella.x = random.randint(0, 760)
        estrella.y = 0

    pantalla.fill("black")

    pygame.draw.rect(
        pantalla,
        "blue",
        jugador
    )

    pygame.draw.rect(
        pantalla,
        "yellow",
        estrella
    )

    texto = fuente.render(
        f"Puntos: {puntos}",
        True,
        "white"
    )

    pantalla.blit(texto, (10,10))

    pygame.display.update()

    clock.tick(60)

pygame.quit()