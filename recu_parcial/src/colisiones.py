from math import sqrt
import pygame
from config import *
from functions import game_over

def punto_en_rect(punto, rect):
    x,y = punto
    return x >= rect.left and x <= rect.right and y >= rect.top and y <= rect.bottom



def detectar_colision(rect_1,rect_2):
    distancia = distancia_entre_puntos(rect_1.center, rect_2.center)
    r1 = calcular_radio_rectangulo(rect_1)
    r2 = calcular_radio_rectangulo(rect_2)
    
    return distancia <= (r1 + r2)


def distancia_entre_puntos(punto_1,punto_2):
    x1,y1 = punto_1
    x2,y2 = punto_2
    return sqrt((y1 - y2) ** 2 + (x1 - x2) ** 2)

def calcular_radio_rectangulo(rect):
    return rect.width //2



def distancia_centros_rect(rect_1,rect_2):
    return distancia_entre_puntos(rect_1.center, rect_2.center)


def colision_objeto(objeto1, objeto2, objetos, sonido, contador_puntos,puntos_sumados:int):
    if detectar_colision(objeto1['rect'], objeto2["rect"]):
        objetos.remove(objeto1)
        sonido.play()
        contador_puntos += puntos_sumados
    return contador_puntos



def colision_poder(poderes:list, player:dict, coin_sound:pygame.mixer.Sound, poder_velocidad:bool, tiempo_efecto_poderes:int, speed_player:int):
    """
    Evalúa la colisión entre el jugador y los objetos de poder.

    Parameters:
    poderes (list): Lista de diccionarios que representan los objetos de poder en pantalla.
    player (dict): Diccionario que representa al jugador.
    coin_sound (pygame.mixer.Sound): Objeto de sonido para reproducir al recoger un poder.
    poder_velocidad (bool): Indica si el poder de velocidad está activo.
    tiempo_efecto_poderes (int): Tiempo en milisegundos desde que se activó el poder.
    speed_player (int): Velocidad actual del jugador.

    Returns:
    Tuple: Una tupla que contiene los siguientes valores actualizados:
    poderes (list): Lista de diccionarios actualizada después de procesar colisiones.
    poder_velocidad (bool): Estado actualizado del poder de velocidad.
    tiempo_efecto_poderes (int): Tiempo actualizado desde que se activó el poder.
    speed_player (int): Velocidad del jugador actualizada después de aplicar el poder.
    """
    for punto in poderes[:]:
        if detectar_colision(punto['rect'], player["rect"]):
            poderes.remove(punto)
            coin_sound.play()
            poder_velocidad = True
            tiempo_efecto_poderes = pygame.time.get_ticks()
            speed_player = speed_player * 2

    if poder_velocidad:
        tiempo_transcurrido = pygame.time.get_ticks() - tiempo_efecto_poderes
        if tiempo_transcurrido > 5000:
            poder_velocidad = False
            speed_player = speed_player / 2

    return poderes, poder_velocidad, tiempo_efecto_poderes, speed_player


def colision_obstaculos_disparos(obstaculos, disparos, sonido_explosion):
    """
    Maneja las colisiones entre obstáculos y disparos en un juego.

    Parameters:
    obstaculos (list): Una lista de diccionarios representando los obstáculos en el juego.
    disparos (list): Una lista de diccionarios representando los disparos en el juego.
    sonido_explosion (objeto): Objeto que representa el sonido de la explosión al ocurrir una colisión.
    

    Returns:
    None
    """
    for obstaculo in obstaculos[:]:
        for bala in disparos[:]:
            if detectar_colision(obstaculo['rect'], bala["rect"]):
                obstaculos.remove(obstaculo)
                sonido_explosion.play()
                sonido_explosion.set_volume(0.2)


def manejar_colision_obstaculo(obstaculo, player, corazones, dificultad_media, maximo_puntaje, screen, contador_puntos, is_running, obstaculos):
    """
    Maneja la colisión con un obstáculo, reproduce el sonido de choque y reduce las vidas del jugador.
    Parameters:
        obstaculo (dict): El obstáculo con el que se produjo la colisión.
        player (dict): El jugador.
        corazones (list): La lista de corazones.
        dificultad_media: El estado de dificultad actual.
        maximo_puntaje (int): El máximo puntaje.
        screen: La pantalla del juego.
        contador_puntos (int): El contador de puntos.
        is_running (bool): Variable que indica si el juego está en ejecución.
        obstaculos (list): La lista de obstáculos.

    Returns:
        int: El nuevo máximo puntaje.
        bool: La nueva condición de ejecución del juego.
        any: El nuevo estado de dificultad.
    """
    crash_sound.play()
    crash_sound.set_volume(0.4)
    obstaculos.remove(obstaculo)

    if corazones:
        corazones.pop(0)

    if player['vidas'] > 1:
        player['vidas'] -= 1
    else:
        dificultad_media = None
        maximo_puntaje = game_over(screen, contador_puntos, maximo_puntaje)
        is_running = False

    return maximo_puntaje, is_running, dificultad_media