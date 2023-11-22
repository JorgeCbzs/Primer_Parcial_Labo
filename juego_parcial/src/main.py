import pygame
from config import *
from pygame import display, time, event
from functions import *
from colisiones import *
from pygame.locals import *
from utils import *
pygame.init()



#CARGAR IMAGENES
image_player = pygame.image.load("assets/imagenes/batmovil.png")
background = pygame.transform.scale(pygame.image.load("assets/imagenes/road.png"), SIZE_SCREEN)
titulo_img = pygame.image.load("assets/imagenes/titulo.png")
disparo_img = pygame.image.load("assets/imagenes/bala.png")
moneda_img = pygame.image.load("assets/imagenes/moneda.png")
obstaculo_img = pygame.image.load("assets/imagenes/obstaculo.png")
recarga_img = pygame.image.load("assets/imagenes/municion.png")
caja_municion_img = pygame.image.load("assets/imagenes/caja_municion.png")
puntos_extra_img = pygame.image.load("assets/imagenes/puntos_extra.png")
corazon_img = pygame.image.load("assets/imagenes/vida1.png")

#CARGAR SONIDOS
pygame.mixer.music.load("assets/sonidos/auto_fantastico.mp3")
pygame.mixer.music.set_volume(0.7)
crash_sound = pygame.mixer.Sound("assets/sonidos/collision.wav")
coin_sound = pygame.mixer.Sound("assets/sonidos/coin.mp3")
sonido_error = pygame.mixer.Sound("assets/sonidos/error.mp3")
sonido_select = pygame.mixer.Sound("assets/sonidos/select.mp3")
game_over_sound = pygame.mixer.Sound("assets/sonidos/game_over.mp3")
sonido_recarga = pygame.mixer.Sound("assets/sonidos/sound_recarga.wav")
sonido_disparo = pygame.mixer.Sound("assets/sonidos/sound_disparo.mp3")
sonido_explosion = pygame.mixer.Sound("assets/sonidos/sound_explosion.mp3")
sonido_game_over = pygame.mixer.Sound("assets/sonidos/game_over.mp3")



screen = display.set_mode(SIZE_SCREEN)
display.set_caption("CAR COLLIDER")



#FUENTE
ruta_fuente = "assets/fonts/Gameplay.ttf"
fuente = pygame.font.Font(ruta_fuente, 26)




#EVENTOS
EVENT_MUNICION = pygame.USEREVENT + 1
pygame.time.set_timer(EVENT_MUNICION, 10000)


EVENT_OBSTACULO = pygame.USEREVENT + 2
pygame.time.set_timer(EVENT_OBSTACULO,2500)


EVENT_COIN = pygame.USEREVENT + 3
pygame.time.set_timer(EVENT_COIN,800)

EVENT_PUNTOS_EXTRA = pygame.USEREVENT + 4
pygame.time.set_timer(EVENT_PUNTOS_EXTRA,8000)


# Creo un reloj
clock = time.Clock()


#Direccion
move_up = False
move_right = False
move_down = False
move_left = False



background_color_button = AZUL
background_color_button_hover = MAS_OSCURO
button_medio = pygame.Rect(CENTER_SCREEN_X - button_width //2 ,640,button_width,button_height)
button_dificil = pygame.Rect(CENTER_SCREEN_X - button_width //2 ,700,button_width,button_height)
button_comenzar = pygame.Rect(CENTER_SCREEN_X - button_width //2 ,560,button_width,button_height)
dificultad_media = None
color_boton_medio = OSCURO
color_boton_dificil = OSCURO
color_boton_comenzar = OSCURO
block_titulo = crear_bloque(titulo_img, (0), (0), WIDTH_SCREEN,200)

is_running = False
running = True


municion_total = 0
contador_municion = 0
maximo_puntaje = 0
player = crear_bloque(image_player,CENTER_SCREEN_X,HEIGHT_SCREEN-player_height*2,player_width,player_height)
efecto_puntos_extra = False
tiempo_efecto_puntos_extra = 0
while running:
    
    contador_puntos = 0
    monedas = []
    municiones = []
    municion_cajas = []
    obstaculos = []
    disparos = []
    puntos_extra = []
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
                            is_running = False
                        else:
                            is_running = True
                            pygame.mixer.music.play(-1)
                            load_municion(municiones,contador_municion,recarga_img)
                            load_corazones(corazones,vidas,corazon_img)
            if dificultad_media == None:
                color_boton_dificil = OSCURO
                color_boton_medio = OSCURO
                            
            if dificultad_media == True:
                vidas = 5
                contador_municion = 5
                cantidad_obstaculos = 6
                cantidad_monedas = 4
                color_boton_medio = MAS_OSCURO
                color_boton_dificil = OSCURO
            
            if dificultad_media == False:
                color_boton_medio = OSCURO
                color_boton_dificil = MAS_OSCURO
                vidas = 2
                contador_municion = 3
                dificultad_media = False
                cantidad_obstaculos = 8
                cantidad_monedas = 3
                
    municion_total = contador_municion        
    screen.fill(GRIS)
    screen.blit(block_titulo["imagen"], block_titulo["rect"])
    crear_boton(screen,color_boton_medio,button_medio,"MEDIO",background_color_button_hover)
    crear_boton(screen,color_boton_dificil,button_dificil,"DIFICIL",background_color_button_hover)
    crear_boton(screen,color_boton_comenzar,button_comenzar,"START",background_color_button_hover)
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
                crear_objetos(1,municion_cajas,width_caja_municion,height_caja_municion,caja_municion_img)
            
            elif e.type == EVENT_OBSTACULO:
                crear_objetos(cantidad_obstaculos,obstaculos,width_obstaculo,height_obstaculo,obstaculo_img)
            
            elif e.type == EVENT_COIN:
                crear_objetos(cantidad_monedas,monedas,width_coin,height_coin,moneda_img)
            
            elif e.type == EVENT_PUNTOS_EXTRA:
                crear_objetos(1,puntos_extra,50,50,puntos_extra_img)
                
                #PRESIONAR TECLAS
            elif e.type == KEYDOWN:
                
                #Mover derecha
                if e.key == K_RIGHT or e.key == K_d:
                    move_right = True
                    move_left = False

                #Mover izquierda
                elif e.key == K_LEFT or e.key == K_a:
                    move_left = True
                    move_right = False

                #Mover arriba
                elif e.key == K_UP or e.key == K_w:
                    move_up = True
                    move_down = False
                
                #Mover abajo
                elif e.key == K_DOWN or e.key == K_s:
                    move_down = True
                    move_up = False
                
                elif e.key == K_p:
                    pygame.mixer.music.pause()
                    mostrar_texto(screen,"PAUSA",WIDTH_SCREEN//2,WIDTH_SCREEN //2,36,RED)
                    pygame.display.flip()
                    pausa()
                    pygame.mixer.music.unpause()

            elif e.type == MOUSEBUTTONDOWN:
                if contador_municion > 0 and e.button == 1:
                    midtop_player = player["rect"].midtop
                    nueva_bala = crear_bloque(disparo_img, midtop_player[0] - width_disparo // 2, midtop_player[1] - height_disparo, width_disparo, height_disparo, BLUE, speed_y=speed_disparo)
                    disparos.append(nueva_bala)
                    
                    if municiones:
                            municiones.pop()
                            contador_municion -= 1
                            sonido_disparo.play()
                            sonido_disparo.set_volume(0.5)
                    
                #SOLTAR TECLAS
            if e.type == KEYUP:
                if e.key == K_RIGHT or e.key == K_d:
                    move_right = False
                    
                elif e.key == K_LEFT or e.key == K_a:
                    move_left = False
                    
                elif e.key == K_UP or e.key == K_w:
                    move_up = False
                    
                elif e.key == K_DOWN or e.key == K_s:
                    move_down = False
                    
                elif e.key == K_ESCAPE:
                    is_running = False
                    pygame.mixer.music.stop()

        # ---> ACTUALIZAR ELEMENTOS <---
        
        # MOVIMIENTO PLAYER
        if move_right and player["rect"].right <= (WIDTH_SCREEN - BORDE):
            # Derecha
            player["rect"].left += speed

        if move_left and player["rect"].left >= (0 + BORDE):
            # Izquierda
            player["rect"].left -= speed

        if move_up and player["rect"].top >= (0 + speed):
            # Arriba
            player["rect"].top -= speed

        if move_down and player["rect"].bottom <= (HEIGHT_SCREEN - speed):
            # Abajo
            player["rect"].top += speed
        
        
        

        #MOVIMIENTO DISPARO
        for bala in disparos[:]:
            if bala["rect"].bottom >= 0:
                bala["rect"].move_ip(0, -bala["speed_y"])
            else:
                disparos.remove(bala)

        #MOVIMIENTO MONEDA
        mover_objeto(monedas)

        #MOVIMIENTO CAJA MUNICION
        mover_objeto(municion_cajas)

        #MOVIMIENTO OBSTACULO
        mover_objeto(obstaculos)
        
        #MOVIMIENTO PUNTOS EXTRA
        mover_objeto(puntos_extra)
            
        
        #COLISION MONEDA        
        for coin in monedas[:]:
            if detectar_colision(coin['rect'], player["rect"]):
                monedas.remove(coin)
                contador_puntos += 1000
                coin_sound.play()
        
        #COLISION CAJA MUNICION
        for caja in municion_cajas[:]:
            if detectar_colision(caja['rect'], player["rect"]):
                municion_cajas.remove(caja)
                sonido_recarga.play()
                while contador_municion < municion_total:
                    aux = municion_total - contador_municion
                    contador_municion += aux
                    load_municion(municiones, aux, recarga_img)
        #PUNTOS EXTRA
        for punto in puntos_extra[:]:
            if detectar_colision(punto['rect'], player["rect"]):
                puntos_extra.remove(punto)
                contador_puntos += 10000
                coin_sound.play()
                efecto_puntos_extra = True
                tiempo_efecto_puntos_extra = pygame.time.get_ticks()  # Obtiene el tiempo actual en milisegundos
                FPS = 30
        
        if efecto_puntos_extra:
            tiempo_transcurrido = pygame.time.get_ticks() - tiempo_efecto_puntos_extra
            if tiempo_transcurrido > 5000:  # 5000 milisegundos = 5 segundos
                FPS = 60
                efecto_puntos_extra = False

        
        #COLISION OBSTACULO
            #---Con player
        for obstaculo in obstaculos[:]:
            if detectar_colision(obstaculo['rect'], player["rect"]):
                crash_sound.play()
                crash_sound.set_volume(0.4)
                obstaculos.remove(obstaculo)
                corazones.pop(0)
                if vidas > 1:
                    vidas -= 1
                else:
                    dificultad_media = None
                    game_over_sound.play()
                    if contador_puntos > maximo_puntaje:
                        maximo_puntaje = contador_puntos
                    screen.fill(BLACK)
                    mostrar_texto(screen, "Game Over", WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2, 50, RED)
                    mostrar_texto(screen, f"Puntos: {contador_puntos}", WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2 + 200, 18, AZUL)
                    mostrar_texto(screen, f"Maximo Puntaje: {maximo_puntaje}", WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2 + 250, 18, AZUL)
                    pygame.display.flip()
                    pygame.mixer.music.stop()
                    is_running = False  # Termina el bucle principal y, por lo tanto, el juego
                    pygame.time.wait(4000)  # Espera 2 segundos para que el jugador vea el mensaje de Game Over
            
            #--- Con disparo
        for obstaculo in obstaculos[:]:
            for bala in disparos[:]:
                if detectar_colision(obstaculo['rect'], bala["rect"]):
                    obstaculos.remove(obstaculo)
                    sonido_explosion.play()
                    sonido_explosion.set_volume(0.2)
                    contador_puntos += 2000
        
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
        
        for punto in puntos_extra:
            dibujar_objects(screen,puntos_extra)
        
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

