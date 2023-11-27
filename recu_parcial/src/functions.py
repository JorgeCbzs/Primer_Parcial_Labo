import pygame
from pygame.locals import *
from random import randint
from config import *
from utils import *



def crear_objetos(cantidad:int,objetos:list,width_objeto:int,height_objeto:int,img_objeto):
    """
    Crea una lista de objetos con posiciones y tamaños aleatorios.

    Parameters:
        cantidad (int): La cantidad de objetos a crear.
        objetos (list): La lista donde se agregarán los objetos.
        width_objeto (int): El ancho de los objetos.
        height_objeto (int): La altura de los objetos.
        img_objeto: La imagen para los objetos.

    Returns:
        None
    """
    try:
        for i in range(cantidad):
            objetos.append(crear_bloque(img_objeto, (randint(100, WIDTH_SCREEN - BORDE)), 0,width_objeto, height_objeto))
    except Exception:
        print(f"Error al crear objetos.")
        exit()


def crear_bloque(imagen = None, left = 0,top = 0,ancho = 40,alto = 40,color = (255,255,255),borde = 0,radio = -1, speed_x = 5, speed_y = 5,vidas = 0):
    """
    Crea un bloque con propiedades específicas.

    Parameters:
        imagen: La imagen del bloque.
        left (int): La posición x del bloque.
        top (int): La posición y del bloque.
        ancho (int): El ancho del bloque.
        alto (int): La altura del bloque.
        color (tuple): El color del bloque.
        borde (int): El grosor del borde del bloque.
        radio (int): El radio de las esquinas del bloque.
        speed_x (int): La velocidad en el eje x del bloque.
        speed_y (int): La velocidad en el eje y del bloque.

    Returns:
        dict: Un diccionario que representa el bloque.
    """
    rec = pygame.Rect(left, top, ancho, alto)
    if imagen: 
            imagen = pygame.transform.scale(imagen,(ancho,alto))
    return {"rect": rec, "color": color, "borde": borde, "radio": radio,
            "speed_x": speed_x, "speed_y": speed_y, "imagen":imagen, "vidas":vidas}

#CARGAR OBJETOS

def load_municion(municion: list, cantidad: int, imagen=None):
    try:
        cantidad = int(cantidad)  # Intenta convertir la cantidad a un entero
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser un número negativo")
        
        pos_y = 220
        pos_x = 535

        for i in range(cantidad):
            pos_y = pos_y + 40
            recarga = crear_bloque(imagen, pos_x, pos_y, width_municion, height_municion)
            municion.append(recarga)
    except ValueError as e:
        print(f"Error al cargar municiones: {e}")
        exit()

def load_corazones(corazones:list,cantidad:int,imagen = None):
    pos_y = 20
    pos_x = WIDTH_SCREEN
    for i in range(cantidad):
        pos_x = pos_x - 40
        recarga = crear_bloque(imagen,pos_x,pos_y,40,40)
        corazones.append(recarga)



#MOVER OBJETOS

def mover_player(player, speed, estado_teclas):
    """
    Mueve al jugador según el estado actual de las teclas.

    Parameters:
        player: El jugador a mover.
        speed (int): La velocidad del jugador.
        estado_teclas (dict): El estado actual de las teclas de movimiento.

    Returns:
        None
    """
    if estado_teclas["move_right"] and player["rect"].right <= (WIDTH_SCREEN - BORDE):
        # Derecha
        player["rect"].left += speed

    if estado_teclas["move_left"] and player["rect"].left >= (0 + BORDE):
        # Izquierda
        player["rect"].left -= speed

    if estado_teclas["move_up"] and player["rect"].top >= (0 + speed):
        # Arriba
        player["rect"].top -= speed

    if estado_teclas["move_down"] and player["rect"].bottom <= (HEIGHT_SCREEN - speed):
        # Abajo
        player["rect"].top += speed


def mover_disparos(disparos):
    """
    Mueve los disparos hacia arriba y elimina los que salen de la pantalla.

    Parameters:
        disparos (list): La lista de disparos.

    Returns:
        None
    """
    for bala in disparos[:]:
        if bala["rect"].bottom >= 0:
            bala["rect"].move_ip(0, -bala["speed_y"])
        else:
            disparos.remove(bala)


def mover_objeto(objetos:list):
    """
    Mueve los objetos hacia abajo y elimina los objetos que salen de la pantalla.

    Parameters:
        objetos (list): La lista de objetos a mover.

    Returns:
        None
    """
    for objeto in objetos:
        objeto['rect'].move_ip(0, objeto['speed_y'])
        for objeto in objetos:
            if objeto['rect'].top > HEIGHT_SCREEN:
                objetos.pop(0)


def game_over(screen,puntos,maximo_puntaje):
    """
    Muestra la pantalla de Game Over y espera un tiempo antes de regresar al menú principal.

    Parameters:
        screen: La pantalla del juego.
        puntos (int): Los puntos obtenidos en el juego.
        maximo_puntaje (int): El máximo puntaje alcanzado anteriormente.

    Returns:
        int: El nuevo máximo puntaje.
    """
    game_over_sound.play()
    if puntos > maximo_puntaje:
        maximo_puntaje = puntos
    screen.fill(BLACK)
    mostrar_texto(screen, "Game Over", WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2, 50, RED)
    mostrar_texto(screen, f"Puntos: {puntos}", WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2 + 200, 18, AZUL)
    mostrar_texto(screen, f"Maximo Puntaje: {maximo_puntaje}", WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2 + 250, 18, AZUL)
    pygame.display.flip()
    pygame.mixer.music.stop()
    pygame.time.wait(4000)
    return maximo_puntaje



#TECLAS
def manejar_teclas_presionadas(event, estado_teclas):
    """
    Maneja la lógica de las teclas presionadas y actualiza el estado de las teclas.

    Parameters:
    - event (pygame.event.Event): Evento de tecla presionada.
    - estado_teclas (dict): Diccionario que representa el estado actual de las teclas.

    Returns:
    dict: Estado de las teclas actualizado después de procesar el evento de tecla.
    """
    if event.key == K_RIGHT or event.key == K_d:
        estado_teclas["move_right"] = True
        estado_teclas["move_left"] = False
    elif event.key == K_LEFT or event.key == K_a:
        estado_teclas["move_left"] = True
        estado_teclas["move_right"] = False
    elif event.key == K_UP or event.key == K_w:
        estado_teclas["move_up"] = True
        estado_teclas["move_down"] = False
    elif event.key == K_DOWN or event.key == K_s:
        estado_teclas["move_down"] = True
        estado_teclas["move_up"] = False
    return estado_teclas


def manejar_teclas_liberadas(event, estado_teclas):
    """
    Maneja la lógica de las teclas liberadas y actualiza el estado de las teclas.

    Parameters:
    - event (pygame.event.Event): Evento de tecla liberada.
    - estado_teclas (dict): Diccionario que representa el estado actual de las teclas.

    Returns:
    dict: Estado de las teclas actualizado después de procesar el evento de tecla liberada.
    """
    if event.key == K_RIGHT or event.key == K_d:
        estado_teclas["move_right"] = False
    elif event.key == K_LEFT or event.key == K_a:
        estado_teclas["move_left"] = False
    elif event.key == K_UP or event.key == K_w:
        estado_teclas["move_up"] = False
    elif event.key == K_DOWN or event.key == K_s:
        estado_teclas["move_down"] = False
    elif event.key == K_ESCAPE:
        estado_teclas["is_running"] = False
        pygame.mixer.music.stop()

    return estado_teclas



def disparar(player, disparos, municiones, contador_municion, sonido_disparo, width_disparo, height_disparo, speed_disparo):
    """
    Maneja la lógica de disparar, agregando una nueva bala a la lista de disparos.

    Parameters:
        player: El jugador que realiza el disparo.
        disparos (list): La lista de disparos.
        municiones (list): La lista de municiones.
        contador_municion (int): El contador de municiones restantes.
        sonido_disparo: El sonido que se reproduce al disparar.
        width_disparo (int): El ancho de la bala.
        height_disparo (int): La altura de la bala.
        speed_disparo (int): La velocidad de la bala.

    Returns:
        int: El nuevo contador de municiones después de efectuar el disparo.
    """
    if contador_municion > 0:
        midtop_player = player["rect"].midtop
        nueva_bala = crear_bloque(disparo_img, midtop_player[0] - width_disparo // 2, midtop_player[1] - height_disparo, width_disparo, height_disparo, BLUE, speed_y=speed_disparo)
        disparos.append(nueva_bala)
        
        if municiones:
            municiones.pop()
            contador_municion -= 1
            sonido_disparo.play()
            sonido_disparo.set_volume(0.5)

    return contador_municion


def terminar():
        pygame.quit()
        exit()

def dibujar_objects(superficie,objects:list):
    """
    Dibuja los objetos en la superficie.

    Parameters:
        superficie: La superficie donde se dibujarán los objetos.
        objects (list): La lista de objetos a dibujar.

    Returns:
        None
    """
    for objeto in objects:
        if objeto["imagen"]:
            superficie.blit(objeto["imagen"], objeto["rect"])
        else:
            pygame.draw.rect(
                superficie, objeto["color"], objeto['rect'], objeto["borde"], objeto["radio"])
