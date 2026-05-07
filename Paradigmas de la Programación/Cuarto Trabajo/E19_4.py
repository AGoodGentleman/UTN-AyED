import pygame

pygame.init()

pantalla = pygame.display.set_mode((1200, 800))

pygame.display.set_caption("Jax")

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    pantalla.fill("green")

    imagen = pygame.image.load("Miscelaneo\Jax.png")

    imagen = pygame.transform.scale(imagen, (750, 500))

    pantalla.blit(imagen, (250, 150))

    pygame.display.update()

pygame.quit()