import sys
import pygame as pg
import random
import numpy

black = 32, 32, 32

(ancho, alto)=(400,450)

#fantasmas
fantasmasimg = []
fantasmasimgrect = []
fantasmasimgx=[]
fantasmasimgy=[]


player = pg.image.load("fantasma.png")
player = pg.transform.scale(player, (50, 50))


player2 = pg.image.load("fantasma.png")
player2 = pg.transform.scale(player, (50, 50))

def main():

    pg.init()
    screen = pg.display.set_mode((ancho, alto))

    # matriz tablero
    a = []
    filas = alto // 50
    columnas = ancho // 50
    a = numpy.zeros((filas,columnas),dtype=int)
    # llenado de matrix
    for i in range(filas):
        for j in range(columnas):
            if i == j:
                a[i][j]=1

    # agregar 0s a arrays de posiciones de fantasmas
    fantasmasimgx = numpy.zeros((3), dtype=int)
    fantasmasimgy = numpy.zeros((3), dtype=int)




    #screen.blit(player, (5, 5))
    playerrect = player.get_rect()
    playerrect.left=50
    playerrect.top=0


    player2rect = player2.get_rect()
    player2rect.left=0
    player2rect.top=alto-50


    #cargar obstaculos de prueba
    obstimg = []
    obstimgrects = []
    x2 = 0
    y2 = 0

    for f in range(0,columnas):

        obstimg.append(pg.image.load("obstaculo.png"))
        screen.blit(obstimg[f], (x2,y2))
        rect=obstimg[f].get_rect()
        obstimgrects.append(rect)
        rect.left=x2
        rect.top=y2
        #print(rect )
        #print(obstimgrects[f])
        #print(playerrect)
        #print("-")

        x2= x2+ 50
        y2= y2+ 50

# Crear y mostrar valores x y y de fantasmas creados desde 0
    #for f in range(0, 3):
     #   (fantasmasimgx[f], fantasmasimgy[f]) = buscar(a)
    #print(fantasmasimgx, " ---- ", fantasmasimgy)

    #crear fantasmas
    x3=100
    y3=50
    for f in range(0,3):
        newfantas=pg.image.load("fantasma.png")
        newfantas = pg.transform.scale(player, (50, 50))
        fantasmasimg.append(newfantas)
        (fantasmasimgx[f], fantasmasimgy[f]) = buscar(a)
        screen.blit(fantasmasimg[f], (fantasmasimgx[f],fantasmasimgy[f]))
        rect=fantasmasimg[f].get_rect()
        fantasmasimgrect.append(rect)
        rect.left=fantasmasimgx[f]
        rect.top=fantasmasimgy[f]
        #print(rect )
        #print(obstimgrects[f])
        #print(playerrect)
        #print("-")

        x3= x3+ 50
        y3= y3+ 50





    runing=True
    pintar = False
    crearfantasmas=False


    while runing:

        for row in a:
            print(' '.join([str(elem) for elem in row]))







        # crear fantasmas con base en espacios vacios
       # if crearfantasmas == False:
        #    numeroespaciosenmapa = AgregarFantasmas(a, filas, columnas, screen)
         #   crearfantasmas=True



        #mostrar matriz inicial sin fantasmas por consola
        #if pintar == False :
         #   for row in a:
          #      print(' '.join([str(elem) for elem in row]))
            #saber filas y columnas
            #print(a.shape)
           # pintar = True

        #asignar movimiento a cada fantasma con la matrix
        #(playerrect,a) = MoverFantasma(playerrect,a)
        #(player2rect,a) = MoverFantasma(player2rect, a)

        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                runing = False



        pg.time.delay(1000)
        screen.fill(black)

        for f in range(0, columnas):
            screen.blit(obstimg[f], obstimgrects[f])

        #pintar y mover fantasmas
        for p in range(0, 3):
            (fantasmasimgrect[p],a)=MoverFantasma(fantasmasimgrect[p],a)
            screen.blit(fantasmasimg[p], fantasmasimgrect[p])


        #screen.blit(player2, player2rect)
        #screen.blit(player, playerrect)

        pg.display.update()


#Agregar Fantasmas al mapa
def AgregarFantasmas(matrix, fi, co):
    numeroespacios=0
    x0=0
    y0=0

    #contar espacios en matriz
    for i in range(fi):
        for j in range(co):
            if matrix[i][j] == 0:
                numeroespacios+=1


    numerofantasmas=numeroespacios//8
    numerofantasmas=6

    for p in range(numerofantasmas):


        valor = random.randint(0, numeroespacios)

    return x0, y0

def buscar(matrix):
    (filaescogida, columnaescogida) = (0, 0)
    valorfila=random.randint(0, (alto // 50)-1)
    valorcolum=random.randint(0, (ancho // 50)-1)
    encontrado=False

    if matrix[valorfila][valorcolum] == 0:
        encontrado=True
    elif matrix[valorfila][valorcolum] != 0:
        encontrado=False
    else:
        encontrado=False

    valorfila=valorfila*50
    valorcolum=valorcolum*50

    if encontrado == True:
        (filaescogida, columnaescogida) = (valorfila, valorcolum)
        return filaescogida,columnaescogida
    elif encontrado == False:
        return buscar(matrix)






#mover fantasmas con la posicion de cada uno y la matriz del mapa
def MoverFantasma(fantasma, matrixobst):
    opciones = []
    (arr, aba, der, izq) = (True, True, True, True)
    (bordearr, bordeaba, bordeder, bordeizq) = (False, False, False, False)

#Capturo posicion fantasma
    posicionc=fantasma.left//50
    posicionf=fantasma.top//50
#quedan como posiciones anteriores
    posicioncvieja=posicionc
    posicionfvieja=posicionf



#posicion en la que esta el fantasma en la matriz = 3
    matrixobst[posicionf][posicionc]=3
    #print("actual")
    #print(posicionf, posicionc)
    #for row in matrixobst:
        #print(' '.join([str(elem) for elem in row]))

#Miro si esta en un limite del mapa
    #Esta arriba Max
    if posicionf == 0 :
        print("Esta Arriba")
        arr=False
        bordearr=True

    # Esta abajo Max
    if posicionf == (alto//50)-1:
        print("Esta Abajo")
        aba=False
        bordeaba=True

    # Esta izquierda Max
    if posicionc == 0:
        print("Esta a la Izquierda")
        izq=False
        bordeizq=True

    # Esta Derecha Max
    if posicionc == (ancho // 50) - 1:
        print("Esta a la Derecha")
        der=False
        bordeder=True

#Miro si tiene obstaculos al rededor
    #a la izquierda
    if bordeizq == False :
        if matrixobst[posicionf][posicionc-1] == 1 :
            izq=False
        else:
            izq:True

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

#modifico posiciones viejas con 0 = vacio
    #print("nueva")
    #print(posicionfnueva, posicioncnueva)
    matrixobst[posicionfvieja][posicioncvieja] = 0
    matrixobst[posicionfnueva][posicioncnueva] = 3
    #for row in matrixobst:
     #   print(' '.join([str(elem) for elem in row]))

    return fantasma, matrixobst




if __name__ == "__main__":
    main()