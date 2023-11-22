import pygame
from sys import exit
from config import *
from pygame import display, time, draw, event
from functions import *
from colisiones import *
from pygame.locals import *
from utils import *

pygame.init()



screen = display.set_mode(SIZE_SCREEN)
display.set_caption("Menu")  # Nombre de la ventana

# Creo un reloj
clock = time.Clock()


running = True

background_color_button = AZUL
background_color_button_hover = MAS_OSCURO



ruta_fuente = "assets\\fonts\\Gameplay.ttf"

fuente = pygame.font.Font(ruta_fuente, 26)

button_medio = pygame.Rect(CENTER_SCREEN_X - button_width //2 ,640,button_width,button_height)
button_dificil = pygame.Rect(CENTER_SCREEN_X - button_width //2 ,700,button_width,button_height)
button_comenzar = pygame.Rect(CENTER_SCREEN_X - button_width //2 ,560,button_width,button_height)

dificultad_media = None
color_boton_medio = OSCURO
color_boton_dificil = OSCURO
color_boton_comenzar = OSCURO

titulo_img = pygame.image.load("assets\\imagenes\\titulo.png")

sonido_error = pygame.mixer.Sound("assets/sonidos/error.mp3")
sonido_select = pygame.mixer.Sound("assets/sonidos/select.mp3")
block_titulo = crear_bloque(titulo_img, (0), (0), WIDTH_SCREEN,200)

while running:
    for evento in event.get():
            if evento.type == pygame.QUIT:
                running = False
            if evento.type == MOUSEBUTTONDOWN:
                if evento.button == 1:
                    cursor = evento.pos
                    
                    if button_medio.collidepoint(cursor[0],cursor[1]):
                        dificultad_media = True
                        sonido_select.play()
                        color_boton_medio = MAS_OSCURO
                        color_boton_dificil = OSCURO
                    
                    elif button_dificil.collidepoint(cursor[0],cursor[1]):
                        dificultad_media == False
                        sonido_select.play()
                        color_boton_medio = OSCURO
                        color_boton_dificil = MAS_OSCURO
                    
                    elif button_comenzar.collidepoint(cursor[0],cursor[1]):
                        if dificultad_media == None:
                            sonido_error.play()
                        else:
                            running = False
                    
                print(dificultad_media)
    #Coordenadas donde se hace click
    screen.fill(GRIS)
    screen.blit(block_titulo["imagen"], block_titulo["rect"])
    crear_boton(screen,color_boton_medio,button_medio,"MEDIO",background_color_button_hover)
    crear_boton(screen,color_boton_dificil,button_dificil,"DIFICIL",background_color_button_hover)
    crear_boton(screen,color_boton_comenzar,button_comenzar,"START",background_color_button_hover)
    pygame.display.flip()




pygame.quit()
exit()