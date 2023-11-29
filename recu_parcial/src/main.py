import pygame
from config import *
from pygame import display, time, event
from functions import *
from colisiones import *
from pygame.locals import *
from utils import *
pygame.init()


screen = display.set_mode(SIZE_SCREEN)
display.set_caption("CAR COLLIDER")

clock = time.Clock()

#Direccion
estado_teclas = {
    "move_up": False,
    "move_right": False,
    "move_down": False,
    "move_left": False,
}


block_titulo = crear_bloque(titulo_img, (0), (0), WIDTH_SCREEN,200)
player = crear_bloque(image_player,CENTER_SCREEN_X,HEIGHT_SCREEN-player_height*2,player_width,player_height,speed_x=speed_player,speed_y=speed_player,vidas= 0)

is_running = False
running = True
municion_total = 0
contador_municion = 0
maximo_puntaje = 0
poder_velocidad = False
tiempo_efecto_poderes = 0


while running:
    contador_puntos = 0
    monedas = []
    municiones = []
    municion_cajas = []
    obstaculos = []
    disparos = []
    poderes = []
    corazones = []
    for evento in event.get():
        if evento.type == pygame.QUIT:
            running = False
            
        if evento.type == MOUSEBUTTONDOWN:
            if evento.button == 1:
                cursor = evento.pos
                
                if button_medio.collidepoint(cursor[0],cursor[1]):
                    if dificultad_media == False or dificultad_media == None:
                        dificultad_media = True
                        sonido_select.play()
                        
                elif button_dificil.collidepoint(cursor[0],cursor[1]):
                    if dificultad_media == True or dificultad_media == None:
                        dificultad_media = False
                        sonido_select.play()
                        
                elif button_comenzar.collidepoint(cursor[0],cursor[1]):
                    if dificultad_media == None:
                        sonido_error.play()

                    else:
                        is_running = True
                        pygame.mixer.music.play(-1)
                        load_municion(municiones,contador_municion,recarga_img)
                        load_corazones(corazones,player['vidas'],corazon_img)

        if dificultad_media == None:
            config_actual = config_dificultad_nula
        elif dificultad_media == True:
            config_actual = config_dificultad_media
        elif dificultad_media == False:
            config_actual = config_dificultad_dificil
        
        color_boton_medio = config_actual['color_boton_medio']
        color_boton_dificil = config_actual['color_boton_dificil']
        player['vidas'] = config_actual['vidas']
        contador_municion = config_actual['contador_municion']
        cantidad_obstaculos = config_actual['cantidad_obstaculos']
        cantidad_monedas = config_actual['cantidad_monedas']


    municion_total = contador_municion        
    screen.fill(GRIS)
    screen.blit(block_titulo["imagen"], block_titulo["rect"])
    boton_medio = crear_boton(screen,color_boton_medio,button_medio,"MEDIO",background_color_button_hover)
    boton_dificil = crear_boton(screen,color_boton_dificil,button_dificil,"DIFICIL",background_color_button_hover)
    boton_start = crear_boton(screen,color_boton_comenzar,button_comenzar,"START",background_color_button_hover)
    pygame.display.flip()
    disparo = None


    while is_running:
        clock.tick(FPS)
        for e in event.get():
            if e.type == pygame.QUIT:
                dificultad_media = None
                is_running = False
                pygame.mixer.music.stop()
            elif e.type == EVENT_MUNICION:
                crear_objetos(1, municion_cajas, width_caja_municion, height_caja_municion, caja_municion_img)
            elif e.type == EVENT_OBSTACULO:
                crear_objetos(cantidad_obstaculos, obstaculos, width_obstaculo, height_obstaculo, obstaculo_img)
            elif e.type == EVENT_COIN:
                crear_objetos(cantidad_monedas, monedas, width_coin, height_coin, moneda_img)
            elif e.type == EVENT_PODER:
                crear_objetos(1, poderes, 50, 50, poder_img)
            elif e.type == KEYDOWN:
                estado_teclas = manejar_teclas_presionadas(e, estado_teclas)
            elif e.type == KEYUP:
                estado_teclas = manejar_teclas_liberadas(e, estado_teclas)
            elif e.type == MOUSEBUTTONDOWN:
                if contador_municion > 0 and e.button == 1:
                    contador_municion = disparar(player, disparos, municiones, contador_municion, sonido_disparo, width_disparo, height_disparo, speed_disparo)


        # ---> ACTUALIZAR ELEMENTOS <---
        
        # MOVIMIENTO ELEMENTOS
        mover_player(player, speed_player, estado_teclas)

        mover_disparos(disparos)

        mover_objeto(monedas)

        mover_objeto(municion_cajas)

        mover_objeto(obstaculos)

        mover_objeto(poderes)
        
        #COLISION MONEDA        
        for coin in monedas[:]:
            contador_puntos = colision_objeto(coin, player, monedas, coin_sound, contador_puntos,1000)
            
        #PUNTOS EXTRA
        poderes, poder_velocidad, tiempo_efecto_poderes, speed_player = colision_poder(poderes, player, coin_sound, poder_velocidad, tiempo_efecto_poderes, speed_player)

        #COLISION CAJA MUNICION
        for caja in municion_cajas[:]:
            if caja['rect'].colliderect(player["rect"]):
                municion_cajas.remove(caja)
                sonido_recarga.play()
                while contador_municion < municion_total:
                    aux = municion_total - contador_municion
                    contador_municion += aux
                    load_municion(municiones, aux, recarga_img)


        #COLISION OBSTACULO
            #---Con player
        for obstaculo in obstaculos[:]:
            if detectar_colision(obstaculo['rect'], player["rect"]):
                maximo_puntaje, is_running, dificultad_media = manejar_colision_obstaculo(obstaculo, player, corazones, dificultad_media, maximo_puntaje, screen, contador_puntos, is_running, obstaculos)
            
            #--- Con disparo
        colision_obstaculos_disparos(obstaculos, disparos, sonido_explosion)

        #DIBUJAR PANTALLA
        screen.blit(background, (0, 0))

        for coin in monedas:
            dibujar_objects(screen,monedas)    

        for municion in municiones:
            dibujar_objects(screen,municiones)
        
        for item in municion_cajas:
            dibujar_objects(screen,municion_cajas)
        
        for obstaculo in obstaculos:
            dibujar_objects(screen,obstaculos)
            #Dibujar disparo    
        for bala in disparos:
            screen.blit(bala["imagen"], bala["rect"])
        
        for punto in poderes:
            dibujar_objects(screen,poderes)
        
        for corazon in corazones:
            dibujar_objects(screen,corazones)

        #Dibujar Texto    
        texto_puntos = fuente.render(f"Puntos: {contador_puntos}", True, WHITE)
        rect_texto_puntos = texto_puntos.get_rect(topleft=(30, 40))
        
        #Dibujar Player
        screen.blit(player["imagen"], player["rect"])
        screen.blit(texto_puntos, rect_texto_puntos)
        pygame.display.flip()
        

pygame.quit()
exit()
