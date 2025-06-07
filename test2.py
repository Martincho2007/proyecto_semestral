import pygame
import sys
import math
import time

pygame.init()
pygame.mixer.init()

ANCHO, ALTO = 916, 613
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Portada con efecto negro y fade Space")

# Cargar la imagen de fondo y escalarla
fondo_original = pygame.image.load("true_port2.png").convert()
fondo = pygame.transform.scale(fondo_original, (ANCHO, ALTO))

pygame.mixer.music.load("uncharted.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Fuente y texto "Space"
fuente_boton = pygame.font.SysFont("Arial", 18)
texto_space = "Space"
color_texto = (80, 80, 80)

# Posición base para centrar el texto y cuadro (ajustada)
pos_centro_x = 430
pos_centro_y = (ALTO // 2 + 100) + 10

# Tamaño del cuadro plomo (margen alrededor del texto)
padding_x = 20
padding_y = 10

clock = pygame.time.Clock()
start_time = time.time()

# Duración total del revelado en segundos (más rápido)
duracion_revelado = 2.5

def easing_in_out(t):
    # Función de easing suave para velocidad variable
    return 0.5 - 0.5 * math.cos(math.pi * t)

def crear_mascara_negra_diagonal(progreso, borde=150):
    # Crea una máscara negra con barrido diagonal y borde difuso, opacidad variable
    mascara = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)

    # Opacidad total del negro que disminuye conforme avanza el progreso
    alpha_total = int(255 * (1 - progreso))
    if alpha_total < 0:
        alpha_total = 0

    # Rellenar con negro opaco según alpha_total
    mascara.fill((0, 0, 0, alpha_total))

    max_diag = math.hypot(ANCHO, ALTO)
    diag_actual = max_diag * progreso

    ancho_rect = diag_actual * math.sqrt(2)
    alto_rect = ANCHO + ALTO  # suficientemente grande para cubrir la pantalla

    rect_surf = pygame.Surface((int(ancho_rect), int(alto_rect)), pygame.SRCALPHA)
    rect_surf.fill((0, 0, 0, 0))

    # Relleno negro opaco con alpha_total
    rect_surf.fill((0, 0, 0, alpha_total))

    # Dibujar múltiples elipses concéntricas para degradado difuso en borde derecho,
    # con alpha proporcional a alpha_total para que se desvanezca también
    for i in range(borde):
        alpha = int(alpha_total * (1 - i / borde) * 0.7)
        ancho_elipse = int(borde * 2 - i * 2)
        alto_elipse = int(alto_rect)
        elipse_rect = pygame.Rect(ancho_rect - borde * 2 + i, 0, ancho_elipse, alto_elipse)
        pygame.draw.ellipse(rect_surf, (0, 0, 0, alpha), elipse_rect, width=1)

    rect_rotado = pygame.transform.rotate(rect_surf, -45)

    pos_x = -rect_rotado.get_width() // 2
    pos_y = -rect_rotado.get_height() // 2

    # Usar BLEND_RGBA_SUB para "recortar" el agujero del barrido
    mascara.blit(rect_rotado, (pos_x, pos_y), special_flags=pygame.BLEND_RGBA_SUB)

    return mascara

# Variables para el fade in/out del texto
alpha_texto = 0
fade_in = True
fade_speed = 4  # velocidad del fade

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            pygame.quit()
            sys.exit()

    t = time.time() - start_time
    progreso = min(t / duracion_revelado, 1.0)
    progreso_suave = easing_in_out(progreso)

    # Actualizar alpha del texto para fade in/out continuo
    if fade_in:
        alpha_texto += fade_speed
        if alpha_texto >= 255:
            alpha_texto = 255
            fade_in = False
    else:
        alpha_texto -= fade_speed
        if alpha_texto <= 0:
            alpha_texto = 0
            fade_in = True

    pantalla.blit(fondo, (0, 0))

    # Aplicar máscara negra con barrido diagonal y borde difuso
    if progreso < 1.0:
        mascara_negra = crear_mascara_negra_diagonal(progreso_suave, borde=150)
        pantalla.blit(mascara_negra, (0, 0))

    # Renderizar texto "Space" con cuadro plomo y fade animado
    texto_surface = fuente_boton.render(texto_space, True, color_texto)
    texto_surface.set_alpha(alpha_texto)
    texto_rect = texto_surface.get_rect(center=(pos_centro_x, pos_centro_y))

    cuadro_width = texto_rect.width + padding_x
    cuadro_height = texto_rect.height + padding_y
    cuadro_surface = pygame.Surface((cuadro_width, cuadro_height), pygame.SRCALPHA)
    cuadro_surface.fill((150, 150, 150, alpha_texto))
    cuadro_rect = cuadro_surface.get_rect(center=(pos_centro_x, pos_centro_y))

    pantalla.blit(cuadro_surface, cuadro_rect.topleft)
    pantalla.blit(texto_surface, texto_rect.topleft)

    pygame.display.flip()
    clock.tick(60)