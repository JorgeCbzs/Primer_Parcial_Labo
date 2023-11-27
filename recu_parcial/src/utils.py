import pygame
from config import *

def mostrar_texto(superficie, texto, x, y, font_size=36, color=AZUL):
    """
    Muestra un texto en una superficie.

    Parameters:
        superficie: La superficie donde se mostrará el texto.
        texto (str): El texto a mostrar.
        x (int): La posición x del centro del texto.
        y (int): La posición y del centro del texto.
        font_size (int): El tamaño de la fuente del texto (predeterminado a 36).
        color: El color del texto (predeterminado a AZUL).

    Returns:
        None
    """
    ruta_fuente = "assets\\fonts\\Gameplay.ttf"
    fuente = pygame.font.Font(ruta_fuente, font_size)
    render = fuente.render(texto, True, color)
    rect_texto = render.get_rect(center=(x, y))
    superficie.blit(render, rect_texto)

def crear_boton(screen, color_normal, rect: pygame.Rect, texto, color_hover):
    """
    Crea un botón en la pantalla y cambia su color al pasar el mouse sobre él.

    Parameters:
        screen: La pantalla donde se creará el botón.
        color_normal: El color normal del botón.
        rect (pygame.Rect): El rectángulo que define las dimensiones y posición del botón.
        texto (str): El texto que se mostrará en el botón.
        color_hover: El color del botón al pasar el mouse sobre él.

    Returns:
        None
    """
    posicion_mouse = pygame.mouse.get_pos()

    if rect.collidepoint(posicion_mouse):
        pygame.draw.rect(screen, color_hover, rect, border_radius=10)
    else:
        pygame.draw.rect(screen, color_normal, rect, border_radius=10)

    mostrar_texto(screen, texto, rect.centerx, rect.centery)



