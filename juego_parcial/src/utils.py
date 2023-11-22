import pygame
from config import *

def mostrar_texto(superficie,texto,x,y,font_size = 36,color = AZUL):
    ruta_fuente = "assets\\fonts\\Gameplay.ttf"

    fuente = pygame.font.Font(ruta_fuente, font_size)  
    render = fuente.render(texto, True,color)
    rect_texto = render.get_rect(center = (x,y))
    superficie.blit(render,rect_texto)

def crear_boton(screen, color_normal, rect:pygame.Rect, texto, color_hover):
    posicion_mouse = pygame.mouse.get_pos()
    
    if rect.collidepoint(posicion_mouse):
        pygame.draw.rect(screen,color_hover,rect, border_radius= 10)
    else:
        pygame.draw.rect(screen,color_normal,rect, border_radius= 10)

    mostrar_texto(screen,texto,rect.centerx,rect.centery)
