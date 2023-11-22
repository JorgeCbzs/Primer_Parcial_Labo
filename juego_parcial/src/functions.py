import pygame
from pygame.locals import *
from random import randint
from config import *



def crear_objetos(cantidad:int,objetos:list,width_objeto:int,height_objeto:int,img_objeto):
    for i in range(cantidad):
        objetos.append(crear_bloque(img_objeto, (randint(100, WIDTH_SCREEN - BORDE)), 0,width_objeto, height_objeto))


def mover_objeto(objetos):
    for objeto in objetos:
        objeto['rect'].move_ip(0, objeto['speed_y'])
        for objeto in objetos:
            if objeto['rect'].top > HEIGHT_SCREEN:
                objetos.pop(0)

def dibujar_objects(superficie,objects:list):
    for objeto in objects:
        if objeto["imagen"]:
            superficie.blit(objeto["imagen"], objeto["rect"])
        else:
            pygame.draw.rect(
                superficie, objeto["color"], objeto['rect'], objeto["borde"], objeto["radio"])



def crear_bloque(imagen = None, left = 0,top = 0,ancho = 40,alto = 40,color = (255,255,255),
                borde = 0,radio = -1, speed_x = 5, speed_y = 5):
        rec = pygame.Rect(left, top, ancho, alto)
        if imagen: 
                imagen = pygame.transform.scale(imagen,(ancho,alto))
        return {"rect": rec, "color": color, "borde": borde, "radio": radio,
                "speed_x": speed_x, "speed_y": speed_y, "imagen":imagen}


#Cargar objetos

def load_municion(municion:list,cantidad:int,imagen = None):
    pos_y = 220
    pos_x = 535 
    for i in range(cantidad):
        pos_y = pos_y + 40
        recarga = crear_bloque(imagen,pos_x,pos_y,width_municion,height_municion)
        municion.append(recarga)

def load_corazones(corazones:list,cantidad:int,imagen = None):
    pos_y = 20
    pos_x = WIDTH_SCREEN
    for i in range(cantidad):
        pos_x = pos_x - 40
        recarga = crear_bloque(imagen,pos_x,pos_y,40,40)
        corazones.append(recarga)

def terminar():
        pygame.QUIT
        exit()


def pausa():
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                terminar()

            if e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    terminar()
                return