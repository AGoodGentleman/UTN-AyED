import pygame

pygame.init()

pantalla = pygame.display.set_mode((800,600))

clock = pygame.time.Clock()

personaje = pygame.image.load("Miscelaneo\character_bgless.png")

personaje = pygame.transform.scale(personaje, (80,80))

x = 100
y = 100

velocidad = 5

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        x -= velocidad

    if teclas[pygame.K_RIGHT]:
        x += velocidad

    if teclas[pygame.K_UP]:
        y -= velocidad

    if teclas[pygame.K_DOWN]:
        y += velocidad

    if x < 0:
        x = 0

    if x > 720:
        x = 720

    if y < 0:
        y = 0

    if y > 520:
        y = 520

    pantalla.fill("green")

    pantalla.blit(personaje, (x,y))

    pygame.display.update()

    clock.tick(60)

pygame.quit()