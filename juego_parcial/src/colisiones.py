from math import sqrt

# def detectar_colision(rect_1, rect_2):
    
#     if punto_en_rect(rect_1.topleft,rect_2)or\
#         punto_en_rect(rect_1.topright,rect_2)or\
#         punto_en_rect(rect_1.bottomleft, rect_2)or\
#         punto_en_rect(rect_1.bottomright,rect_2)or\
#         punto_en_rect(rect_2.topleft,rect_1)or\
#         punto_en_rect(rect_2.topright,rect_1)or\
#         punto_en_rect(rect_2.bottomleft, rect_1)or\
#         punto_en_rect(rect_2.bottomright,rect_1):
#             return True
#     else:
#         return False

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