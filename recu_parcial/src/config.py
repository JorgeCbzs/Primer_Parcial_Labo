import pygame
pygame.init()



WIDTH_SCREEN = 600
HEIGHT_SCREEN = 800
BORDE = WIDTH_SCREEN // (WIDTH_SCREEN //100)

SIZE_SCREEN = (WIDTH_SCREEN, HEIGHT_SCREEN)
CENTER_SCREEN_X = WIDTH_SCREEN //2
CENTER_SCREEN_Y = HEIGHT_SCREEN //2


#Obstaculo
width_obstaculo = 50
height_obstaculo = 50


#Disparo
size_disparo = (6,15)
width_disparo = 20
height_disparo = 25
speed_disparo = 6


#Moneda
width_coin = 30
height_coin = 30
speed_y_coin = 3


#MUNICION
width_municion = 30
height_municion = 30


#CAJA MUNICION
width_caja_municion = 50
height_caja_municion = 50


#PLAYER
player_width = 65
player_height = 145
speed_player = 6

#Colores 
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRIS = (41,41,41)
AZUL = (194,219,255)
OSCURO = (55,50,50)
MAS_OSCURO = (30,30,30)


FPS = 60


#MENU
background_color_button = AZUL
background_color_button_hover = MAS_OSCURO
button_width = 230
button_height = 50


#CARGAR IMAGENES
image_player = pygame.image.load("assets/imagenes/batmovil.png")
background = pygame.transform.scale(pygame.image.load("assets/imagenes/road.png"), SIZE_SCREEN)
titulo_img = pygame.image.load("assets/imagenes/titulo.png")
disparo_img = pygame.image.load("assets/imagenes/bala.png")
moneda_img = pygame.image.load("assets/imagenes/moneda.png")
obstaculo_img = pygame.image.load("assets/imagenes/obstaculo.png")
recarga_img = pygame.image.load("assets/imagenes/municion.png")
caja_municion_img = pygame.image.load("assets/imagenes/caja_municion.png")
poder_img = pygame.image.load("assets/imagenes/poder.png")
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


#FUENTE
ruta_fuente = "assets/fonts/Gameplay.ttf"
fuente = pygame.font.Font(ruta_fuente, 26)


#MENU
background_color_button = AZUL
background_color_button_hover = MAS_OSCURO
button_medio = pygame.Rect(CENTER_SCREEN_X - button_width //2 ,640,button_width,button_height)
button_dificil = pygame.Rect(CENTER_SCREEN_X - button_width //2 ,700,button_width,button_height)
button_comenzar = pygame.Rect(CENTER_SCREEN_X - button_width //2 ,560,button_width,button_height)
dificultad_media = None
color_boton_medio = OSCURO
color_boton_dificil = OSCURO
color_boton_comenzar = OSCURO





config_dificultad_nula = {
    'color_boton_dificil': OSCURO,
    'color_boton_medio': OSCURO,
    'vidas': 0,  
    'contador_municion': 0,
    'cantidad_obstaculos': 0,
    'cantidad_monedas': 0
}

config_dificultad_media = {
    'color_boton_medio': MAS_OSCURO,
    'color_boton_dificil': OSCURO,
    'vidas': 5,
    'contador_municion': 5,
    'cantidad_obstaculos': 6,
    'cantidad_monedas': 4
}

config_dificultad_dificil = {
    'color_boton_medio': OSCURO,
    'color_boton_dificil': MAS_OSCURO,
    'vidas': 3,
    'contador_municion': 3,
    'cantidad_obstaculos': 8,
    'cantidad_monedas': 3
}

#EVENTOS
EVENT_MUNICION = pygame.USEREVENT + 1
EVENT_OBSTACULO = pygame.USEREVENT + 2
EVENT_COIN = pygame.USEREVENT + 3
EVENT_PODER = pygame.USEREVENT + 4


pygame.time.set_timer(EVENT_MUNICION, 10000)
pygame.time.set_timer(EVENT_OBSTACULO,2500)
pygame.time.set_timer(EVENT_COIN,800)
pygame.time.set_timer(EVENT_PODER,8000)