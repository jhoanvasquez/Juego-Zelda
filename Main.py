import random
import pygame
import numpy
import math

from GUI import *
from Asterisco import *

aleatorio = True
tablero =""
ancho = 0
alto=0

#tamaños
width=800
height=600
x=0
y=50

(ancho, alto)=(800 , 600)


#matriz tablero
matrizTablero=[]


# cargar img del suelo
sueloimg = []

# cargar img obtaculo
obsimg = []


#fantasmas
fantasmasimg = []
fantasmasimgrect = []
fantasmasimgx=[]
fantasmasimgy=[]
cantidadfantasmas=5
player = pygame.image.load("./imgs/fantasma.png")
player = pygame.transform.scale(player, (50, 50))


#lugarllave
filallave=(alto // 50)-1
columnallave=(ancho // 50)-1

#lugarpuerta
filapuerta=(alto // 50) - 1
columnapuerta=0

# inicio del juego
def main(dimension, aleatorio, matrizPersonalizada, anchoPersonalizado, altoPersonalizado):
    if aleatorio == True:
        if dimension == "800 x 600":
            ancho = 800
            alto =600

        if dimension == "600 x 400":
            ancho = 600
            alto =400

        if dimension == "400 x 200":
            ancho = 400
            alto = 200
    else:
        ancho = anchoPersonalizado // 2
        alto = altoPersonalizado  // 2

    pygame.init()

    #Suelo
    suelo = pygame.image.load("./imgs/piso.png")
    obstaculo = pygame.image.load("./imgs/obstaculo.png")

    #Personaje Link
    link = pygame.image.load("./imgs/link1.png")
    link_x = random.randint(0, 2)
    link_y = random.randint(0, 2)
    i=0

    #LLave

    llave = pygame.image.load("./imgs/key.png")
    llave_x = random.randint(2, 7)
    llave_y = random.randint(2, 7)

    meta_x = llave_x
    meta_y = llave_y

    #Puerta

    puerta = pygame.image.load("./imgs/puerta.png")
    puerta_x = math.ceil(ancho/2)-50
    puerta_y = 0
    pygame.display.set_caption("Zelda")
    icon = pygame.image.load("./imgs/icon.png")
    pygame.display.set_icon(icon)


    screen = pygame.display.set_mode((ancho, alto))


    #para matriz
    filas = alto // 50
    columnas = ancho // 50


    #Loop principal
    running = True
    crearTablero = False
    crearfantasmas = False
    moverenemigos = True
    ctrl_puerta = 0

    while running:

        #Crear mapa
        if crearTablero == False:
            global matrizTablero
            if aleatorio == True:
                matrizTablero = tablero(screen, ancho, alto)

                #Asignacion posicion llave y puerta
                while matrizTablero[llave_y][llave_x] == 1:
                    llave_x = random.randint((ancho/100)-1, ancho/100)
                    llave_y = random.randint((alto/100)-1, alto/100)
                matrizTablero[llave_y][llave_x] = 4
                screen.blit(llave, ((llave_x*50)+5, (llave_y*50)+5))
                screen.blit(puerta, (puerta_x-25 , puerta_y-9))

                #Asignacion posicion link

                while matrizTablero[link_y][link_x] == 1:

                    link_x = random.randint(link_x, link_x+3)
                    link_y = random.randint(link_y, link_y+3)

                #Tomar fondo del juego
                global screenshot
                screenshot = screen.copy()
                screen.blit(screenshot, (0, 0))


                screen.blit(link, (link_x * 50, link_y * 50))
                matrizTablero[link_y][link_x] = 2


                #Asignacion posici
                # on puerta

                matrizTablero[math.ceil(puerta_y*2/100)][math.ceil(puerta_x*2/100)] = 5

                #gasto de cada movimiento
                matrizGasto = numpy.zeros((len(matrizTablero),len(matrizTablero[0])))

                #Creacion de fantasmas
                CrearFantasmas(screenshot, matrizTablero, ancho,alto)

                # mover y pintar fantasmas
                for p in range(0, cantidadfantasmas):
                    (fantasmasimgrect[p], a) = MoverFantasma(fantasmasimgrect[p], matrizTablero, ancho, alto)
                    screen.blit(fantasmasimg[p], fantasmasimgrect[p])

            else:
                matrizTablero = matrizPersonalizada
                matrizGasto = numpy.zeros((len(matrizTablero),len(matrizTablero[0])))
                tableroPersonalizado(matrizPersonalizada, screen, suelo, obstaculo, llave, puerta, link, player)
                screenshot = screen.copy()
                link_x =3
                link_y=2
                meta_x=1
                meta_y=0

        #Actulizacion de matrices
        matrizGasto = matrizUpdate(matrizTablero, matrizGasto)


        #Llamado a algorimto de busqueda Link
        global mov

        print (matrizTablero)
        asterisco = Asterisco(matrizGasto, link_x, link_y, meta_x, meta_y)
        mov = asterisco.mov


        #Evento para cierre de ventana
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

        valorAnterior = 0

        #Movimientos de link

        if(mov == []):
            mov = [None]
        if crearTablero == True:
            movimiento = moverLink(mov[0], link_x, link_y, matrizTablero, matrizGasto, valorAnterior)
            link_x = movimiento[0]
            link_y = movimiento[1]
            matrizTablero = movimiento[2]
            matrizGasto = movimiento[3]
            valorAnterior = movimiento[4]
            screen.blit(screenshot, (0, 0))
            screen.blit(link, (link_x * 50, link_y * 50))
            #print (matrizTablero)


        crearTablero = True
        moverenemigos= True
        pygame.time.delay(500)
        pygame.display.update()

# tablero del juego
def tablero (screen, ancho, alto):
    # ciclo para suelo
    for j in range(0, (math.ceil(alto / 100)) * 2):
        for i in range(0, (math.ceil(ancho / 100)) * 2):
            sueloimg.append(pygame.image.load("./imgs/piso.png"))
            screen.blit(sueloimg[i], (i * 50 - 24, j * 50 - 25))

    # ciclo para obstaculos
    matrizObstaculos = numpy.zeros(((math.ceil(alto / 100)) * 2,
                                    (math.ceil(ancho / 100)) * 2), dtype=int)

    for x in range(0, math.ceil(alto / 100)):
        for z in range(0, (math.ceil(ancho / 100))):
            posicionX = random.randint(0, (math.ceil(ancho / 100)) * 2) * 50
            posicionY = random.randint(0, (math.ceil(ancho / 100)) * 2) * 50
            if posicionX <= ancho-50 and posicionY <= alto-50:
                matrizObstaculos[math.floor(posicionY * 2 / 100)][math.floor(posicionX * 2 / 100)] = 1
            obsimg.append(pygame.image.load("./imgs/obstaculo.png"))
            screen.blit(obsimg[z], (posicionX, posicionY))
    return matrizObstaculos

#Movimientos de link
def moverLink(movimiento, link_x, link_y, matrizTablero, matrizGasto, valorAnterior):
        link_x *= 50
        link_y *= 50

        if movimiento == "l":
            if link_x >= 50:
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                valorAnterior = matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)-1]
                link_x -= 50
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2
                matrizGasto[math.ceil(link_y/50)][math.ceil(link_x/50)+1] +=1

        if movimiento == "r":
            if link_x <= ancho-100:
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                valorAnterior = matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)+1]
                link_x += 50
                matrizGasto[math.ceil(link_y/50)][math.ceil(link_x/50)-1]+=1
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2


        if movimiento == "u":
            if link_y >= 50:
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                valorAnterior = matrizTablero[math.ceil(link_y/50)-1][math.ceil(link_x/50)]
                link_y -= 50
                matrizGasto[math.ceil(link_y/50)+1][math.ceil(link_x/50)] += 1
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2


        if movimiento == "d":
            if link_y <= alto-100:
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                valorAnterior = matrizTablero[math.ceil(link_y/50)+1][math.ceil(link_x/50)]
                link_y += 50
                matrizGasto[math.ceil(link_y/50)-1][math.ceil(link_x/50)] += 1
                matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2

        return math.ceil(link_x/50), math.ceil(link_y/50), matrizTablero, matrizGasto, valorAnterior



#Para matriz personalizada
def tableroPersonalizado(matriz, screen, suelo, obstaculo ,llave, puerta, link, fantasma):
    for x in range(0, len(matriz)):
        for z in range(0, len(matriz[0])):
            if matriz[x][z] == 0:
                screen.blit(suelo, (z*50-25, x*50-25))
            if matriz[x][z] == 1:
                screen.blit(obstaculo, (z*50, x*50))
            if matriz[x][z] == 2:
                screen.blit(suelo, (z*50-25, x*50-25))
                screen.blit(link, (z*50, x*50))
            if matriz[x][z] == 3:
                screen.blit(suelo, (z*50-25, x*50-25))
                screen.blit(fantasma, (z*50, x*50))
            if matriz[x][z] == 4:
                screen.blit(suelo, (z*50-25, x*50-25))
                screen.blit(llave, (z*50+5, x*50+5))
            if matriz[x][z] == 5:
                screen.blit(suelo, (z*50-25, x*50-25))
                screen.blit(puerta, (z*50-25 , x*50-9))

#para fantasmas
#Crear fantasmas
def CrearFantasmas(screen, a, ancho,alto):

    # agregar 0s a arrays de posiciones de fantasmas
    fantasmasimgx = numpy.zeros((cantidadfantasmas), dtype=int)
    fantasmasimgy = numpy.zeros((cantidadfantasmas), dtype=int)

    # crear fantasmas
    for f in range(0, cantidadfantasmas):
        newfantas = pygame.image.load("./imgs/fantasma.png")
        newfantas = pygame.transform.scale(player, (50, 50))
        fantasmasimg.append(newfantas)
        (fantasmasimgy[f], fantasmasimgx[f]) = Buscar(a, ancho, alto)
        #screen.blit(fantasmasimg[f], (fantasmasimgx[f], fantasmasimgy[f]))
        rect = fantasmasimg[f].get_rect()
        fantasmasimgrect.append(rect)
        rect.left = fantasmasimgx[f]
        rect.top = fantasmasimgy[f]
        a[fantasmasimgy[f] // 50][fantasmasimgx[f] // 50] = 3

#Actualizar matriz gastos
def matrizUpdate(tablero, gastos):
    try:
        for x in range(0, len(tablero)):
            for i in range(0, len(tablero[0])-1):
             if tablero[x][i] == 3:
                gastos[x][i] = 3
             if tablero[x][i] == 1:
                gastos[x][i] = None
             """if tablero[x][i] == 0 and gastos[x][i] == 3 and \
                     (tablero[x-1][i] != 2 or tablero[x+1][i] != 2 or tablero[x][i-1] != 2 or tablero[x][i+1] != 2):
                gastos[x][i] = 0"""
    except :
        pass
    return gastos
#Busca valores (x,y) para un nuevo fantasma
def Buscar(matrix, ancho,alto):

    #valores iniciales
    valorfila=random.randint(0, (alto // 50)-1)
    valorcolum=random.randint(0, (ancho // 50)-1)

    # valores finales
    (filaescogida, columnaescogida) = (0, 0)

    #si encontro el numero adecuado
    encontrado=False
    #si se cumple la distancia de link
    lejos=False

    # para mirar si esta en un borde del mapa
    (bordearr, bordeaba, bordeder, bordeizq) = (False, False, False, False)


#mirar si esta en un borde del mapa
    # Esta arriba max
    if valorfila == 0:
        bordearr = True

    # Esta abajo Max
    if valorfila == (alto // 50) - 1:
        bordeaba = True

    # Esta izquierda Max
    if valorcolum == 0:
        bordeizq = True

    # Esta Derecha Max
    if valorcolum == (ancho // 50) - 1:
        bordeder = True


#mirar si esta en dos bordes al mismo tiempo
    #arriba y a un lado
    if (bordearr == True and bordeder == True) or (bordearr == True and bordeizq == True):
        if bordearr == True and bordeder == True:
            #print("arriba y a la derecha")
            if (matrix[0][valorcolum-1] != 2) and (matrix[1][valorcolum-1] != 2) and (matrix[1][valorcolum] != 2) :
                #print("si esta lejos link")
                lejos=True
        elif bordearr == True and bordeizq == True:
            #print("arriba y a la izquierda")
            if (matrix[0][1] != 2) and (matrix[1][1] != 2) and (matrix[1][0] != 2) :
                #print("si esta lejos link")
                lejos=True

    #abajo y a un lado
    if (bordeaba == True and bordeder == True) or (bordeaba == True and bordeizq == True):
        if bordeaba == True and bordeder == True:
            #print("abajo y a la derecha")
            if (matrix[valorfila][valorcolum-1] != 2) and (matrix[valorfila-1][valorcolum-1] != 2) and (matrix[valorfila-1][valorcolum] != 2) :
                #print("si esta lejos link")
                lejos=True
        elif bordeaba == True and bordeizq == True:
            #print("abajo y a la izquierda")
            if (matrix[valorfila][1] != 2) and (matrix[valorfila-1][1] != 2) and (matrix[valorfila-1][0] != 2) :
                #print("si esta lejos link")
                lejos=True

#mirar si esta solo en un borde
    # si esta arriba solamente
    if bordearr == True and bordeaba == False and bordeder == False and bordeizq == False:
        #print("solamente arriba")
        if (matrix[0][valorcolum - 1] != 2) and (matrix[0][valorcolum + 1] != 2) and (matrix[1][valorcolum-1] != 2) \
                and (matrix[1][valorcolum] != 2) and (matrix[1][valorcolum+1] != 2):
            #print("si esta lejos link")
            lejos = True

    # si esta abajo solamente
    if bordeaba == True and bordearr == False and bordeder == False and bordeizq == False:
        #print("solamente abajo")
        if (matrix[valorfila][valorcolum-1] != 2) and (matrix[valorfila][valorcolum+1] != 2) \
                and (matrix[valorfila - 1][valorcolum-1] != 2) and (matrix[valorfila - 1][valorcolum] != 2) and (matrix[valorfila - 1][valorcolum+1] != 2):
            #print("si esta lejos link")
            lejos = True


    # si esta a la izquierda solamente
    if bordeizq == True and bordeaba == False and bordeder == False and bordearr == False:
        #print("solamente izquierda")
        if (matrix[valorfila-1][0] != 2) and (matrix[valorfila+1][0] != 2) and (matrix[valorfila - 1][valorcolum + 1] != 2)\
                and (matrix[valorfila][valorcolum+1] != 2) and (matrix[valorfila + 1][valorcolum + 1] != 2):
            #print("si esta lejos link")
            lejos = True

    # si esta a la derecha solamente
    if bordeder == True and bordeaba == False and bordearr == False and bordeizq == False:
        #print("solamente derecha")
        if (matrix[valorfila-1][valorcolum] != 2) and (matrix[valorfila+1][valorcolum] != 2) and (matrix[valorfila - 1][valorcolum - 1] != 2)\
                and (matrix[valorfila][valorcolum-1] != 2) and (matrix[valorfila + 1][valorcolum - 1] != 2):
            #print("si esta lejos link")
            lejos = True

#mirar si no esta en ningun borde
    if bordeder == False and bordeaba == False and bordearr == False and bordeizq == False:
        #print("no esta en ningun borde ")
        if (matrix[valorfila-1][valorcolum-1] != 2) and (matrix[valorfila-1][valorcolum] != 2) and (matrix[valorfila - 1][valorcolum + 1] != 2)\
                and (matrix[valorfila][valorcolum+1] != 2) and (matrix[valorfila ][valorcolum - 1] != 2) and (matrix[valorfila+1][valorcolum-1] != 2) \
                and (matrix[valorfila+1][valorcolum] != 2) and (matrix[valorfila + 1][valorcolum + 1] != 2):
            #print("si esta lejos link")
            lejos = True



    #pasar valores a #*50
    valorfila = valorfila * 50
    valorcolum = valorcolum * 50

    if valorfila == alto:
        valorfila = valorfila - 50

    if valorcolum == ancho:
        valorcolum = valorcolum - 50

    if matrix[valorfila//50][valorcolum//50] == 0:
        encontrado=True
    elif matrix[valorfila//50][valorcolum//50] != 0:
        encontrado=False
    else:
        encontrado=False



    if encontrado == True and lejos == True:
        (filaescogida, columnaescogida) = (valorfila, valorcolum)
        return filaescogida,columnaescogida
    elif encontrado == False or lejos == False:
        return Buscar(matrix, ancho , alto)

#mover fantasmas aleatoriamente con la posicion de cada uno , la matriz del mapa, el ancho y alto de la ventana
def MoverFantasma(fantasma, matrixobst, ancho , alto):
    global filallave,columnallave,filapuerta,columnapuerta
    #capturar si paso por llave o puerta
    (hayllave,haypuerta)=(False,False)

    #opciones de movimiento disponibles
    opciones = []

    #para escoger una direccion disponible
    (arr, aba, der, izq) = (True, True, True, True)

    #para mirar si esta en un borde del mapa
    (bordearr, bordeaba, bordeder, bordeizq) = (False, False, False, False)

#Capturo posicion fantasma
    posicionc=fantasma.left//50
    posicionf=fantasma.top//50
#quedan como posiciones anteriores
    posicioncvieja=posicionc
    posicionfvieja=posicionf

    #si paso por llave
    #if matrixobst[posicionf][posicionc]==4:
     #   print("paso por la llave")
      #  pg.quit()






#Miro si esta en un limite del mapa
    #Esta arriba Max, no se puede mover hacia arriba
    if posicionf == 0 :
        #print("Esta Arriba")
        arr=False
        bordearr=True

    # Esta abajo Max, no se puede mover hacia abajo
    if posicionf == (alto//50)-1:
        #print("Esta Abajo")
        aba=False
        bordeaba=True

    # Esta izquierda Max, no se puede mover hacia la izquierda
    if posicionc == 0:
        #print("Esta a la Izquierda")
        izq=False
        bordeizq=True

    # Esta Derecha Max, no se puede mover hacia la derecha
    if posicionc == (ancho // 50) - 1:
        #print("Esta a la Derecha")
        der=False
        bordeder=True

#Miro si tiene obstaculos al rededor
    #a la izquierda
    if bordeizq == False :
        if matrixobst[posicionf][posicionc-1] == 1 :
            izq=False
        else:
            izq=True

    #a la derecha
    if bordeder == False :
        if matrixobst[posicionf][posicionc+1] == 1 :
            der=False
        else:
            der=True

    #arriba
    if bordearr == False :
        if matrixobst[posicionf-1][posicionc] == 1 :
            arr=False
        else:
            arr=True

    #abajo
    if bordeaba == False :
        if matrixobst[posicionf+1][posicionc] == 1 :
            aba=False
        else:
            aba=True

#Agrego opciones de movimientos al array
    if der == True:
        opciones.append(1)
    if aba == True:
        opciones.append(2)
    if izq == True:
        opciones.append(3)
    if arr == True:
        opciones.append(4)

    valor = random.randint(0, opciones.__len__()-1)
    elegido=opciones[valor]
    #print(opciones)

    # movimiento despues de elegir el lado a donde se va a mover
    # mover derecha
    if elegido == 1 and fantasma.left <= ancho - 100:
        fantasma.left += 50
        # mover abajo
    if elegido == 2 and fantasma.top <= alto - 100:
        fantasma.top += 50
        # mover izquierda
    if elegido == 3 and fantasma.left >= 50:
        fantasma.left += -50
        # mover arriba
    if elegido == 4 and fantasma.top >= 50:
        fantasma.top += -50

#capturo posiciones nuevas
    posicioncnueva = fantasma.left // 50
    posicionfnueva = fantasma.top // 50

#modifico posiciones viejas con 0 = vacio, o con 4 = llave , o 5 = puerta
    #print("nueva")
    #print(posicionfnueva, posicioncnueva)

    #actualizo si estaba la llave en la posicion vieja
    if (filallave == posicionfvieja and columnallave == posicioncvieja) or (filapuerta == posicionfvieja and columnapuerta == posicioncvieja) :
        if (filallave == posicionfvieja and columnallave == posicioncvieja):
            matrixobst[posicionfvieja][posicioncvieja] = 4
        elif (filapuerta == posicionfvieja and columnapuerta == posicioncvieja):
            matrixobst[posicionfvieja][posicioncvieja] = 5
    else :
        matrixobst[posicionfvieja][posicioncvieja] = 0

    #si me muevo a la llave o a la puerta dejo la matrix como estaba con la llave o puerta
    if matrixobst[posicionfnueva][posicioncnueva] == 4 or matrixobst[posicionfnueva][posicioncnueva] == 5:
        if matrixobst[posicionfnueva][posicioncnueva] == 4:
            #print("pase por la llave")
            matrixobst[posicionfnueva][posicioncnueva] = 4
            #(filallave,columnallave)=(posicionfnueva,posicioncnueva)

        elif matrixobst[posicionfnueva][posicioncnueva] == 5:
            #print("pase por la puerta")
            matrixobst[posicionfnueva][posicioncnueva] = 5
            (filapuerta, columnapuerta) = (posicionfnueva, posicioncnueva)
    else:
        matrixobst[posicionfnueva][posicioncnueva] = 3


    return fantasma, matrixobst



if __name__ == '__main__':
    gui = GUI()
    #main("600 x 400", True, [], 0, 0)
    """a =[10]
    
    def algo(w, x):
        w+=[3]
        w+=[2]
        return w

    algo1 = algo(a, 3)
    print (algo1[0])"""

