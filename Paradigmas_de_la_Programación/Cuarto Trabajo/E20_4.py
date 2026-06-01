import pygame

pygame.init()

pantalla = pygame.display.set_mode((800, 600))

ejecutando = True

x = 100
velocidad = 0.5
y = 200
ancho = 200
alto = 200

while ejecutando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    pantalla.fill("green")

    x += velocidad

    pygame.draw.rect(
    pantalla,
    "blue",
    (x, y, ancho, alto)
    )

    if x <= 0 or x >= 750-100:
        velocidad *= -1

    pygame.display.update()

pygame.quit()