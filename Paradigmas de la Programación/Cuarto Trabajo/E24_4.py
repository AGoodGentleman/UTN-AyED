import pygame

pygame.init()

ANCHO = 800
ALTO = 600

pantalla = pygame.display.set_mode((ANCHO, ALTO))

clock = pygame.time.Clock()

spritesheet = pygame.image.load().convert_alpha()

ANCHO_FRAME = 100
ALTO_FRAME = 100

def obtener_frame(fila, columna):

    x = columna * ANCHO_FRAME
    y = fila * ALTO_FRAME

    frame = spritesheet.subsurface(
        (x, y, ANCHO_FRAME, ALTO_FRAME)
    )

    return frame

animacion_abajo = []
animacion_izquierda = []
animacion_derecha = []
animacion_arriba = []

for i in range(4):

    animacion_abajo.append(
        obtener_frame(0, i)
    )

    animacion_izquierda.append(
        obtener_frame(1, i)
    )

    animacion_derecha.append(
        obtener_frame(2, i)
    )

    animacion_arriba.append(
        obtener_frame(3, i)
    )

x = 300
y = 300

velocidad = 5

direccion = "abajo"

frame_actual = 0

ejecutando = True

while ejecutando:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            ejecutando = False

    teclas = pygame.key.get_pressed()

    moviendo = False

    if teclas[pygame.K_LEFT]:

        x -= velocidad
        direccion = "izquierda"
        moviendo = True

    if teclas[pygame.K_RIGHT]:

        x += velocidad
        direccion = "derecha"
        moviendo = True

    if teclas[pygame.K_UP]:

        y -= velocidad
        direccion = "arriba"
        moviendo = True

    if teclas[pygame.K_DOWN]:

        y += velocidad
        direccion = "abajo"
        moviendo = True

    if moviendo:

        frame_actual += 0.15

        if frame_actual >= 4:
            frame_actual = 0

    else:
        frame_actual = 0

    if direccion == "abajo":

        imagen = animacion_abajo[
            int(frame_actual)
        ]

    elif direccion == "izquierda":

        imagen = animacion_izquierda[
            int(frame_actual)
        ]

    elif direccion == "derecha":

        imagen = animacion_derecha[
            int(frame_actual)
        ]

    elif direccion == "arriba":

        imagen = animacion_arriba[
            int(frame_actual)
        ]

    pantalla.fill((30,30,30))

    pantalla.blit(imagen, (x,y))

    pygame.display.update()

    clock.tick(60)

pygame.quit()