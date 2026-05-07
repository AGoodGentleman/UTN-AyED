import pygame

pygame.init()

pantalla = pygame.display.set_mode((800, 600))

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    pantalla.fill("green")

    pygame.display.update()

pygame.quit()