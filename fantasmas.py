import sys
import pygame as pg
import random
import numpy

black = 32, 32, 32

(ancho, alto)=(250,250)

#fantasmas
fantasmasimg = []
fantasmasimgrect = []
fantasmasimgx=[]
fantasmasimgy=[]
cantidadfantasmas=1

#lugarllave
filallave=(alto // 50)-1
columnallave=(ancho // 50)-1

#lugarpuerta
filapuerta=(alto // 50) - 1
columnapuerta=0

player = pg.image.load("./imgs/fantasma.png")
player = pg.transform.scale(player, (50, 50))


def main():

    pg.init()
    screen = pg.display.set_mode((ancho, alto))

    # matriz tablero
    a = []
    filas = alto // 50
    columnas = ancho // 50
    matrizinicial = numpy.zeros((filas,columnas),dtype=int)

    # llenado de matrix con 1 para obstaculos
    #for i in range(filas):
        #for j in range(columnas):
            #if i == j:
                #matrizinicial[i][j]=1




    #llave = 4
    #matrizinicial[ (alto // 50)-1 ][ (ancho // 50)-1] = 4
    #matrizinicial[3][4] = 4
    #puerta = 5
    #matrizinicial[(alto // 50) - 1][0] = 5
    #link = 2
    #matrizinicial[(alto // 50) - 1][3] = 2
    #matrizinicial[0][4] = 2
    #matrizinicial[3][2] = 2


    #cargar obstaculos de prueba
    obstimg = []
    obstimgrects = []
    x2 = 0
    y2 = 0


    #link de prueba
    matrizinicial[3][3] = 2
    #obstaculos de prueba
    matrizinicial[1][1] = 1
    matrizinicial[3][2] = 1

    #1
    obstimg.append(pg.image.load("./imgs/obstaculo.png"))
    screen.blit(obstimg[0], (50, 50))
    rect = obstimg[0].get_rect()
    obstimgrects.append(rect)
    #2
    obstimg.append(pg.image.load("./imgs/obstaculo.png"))
    screen.blit(obstimg[1], (100, 150))
    rect = obstimg[1].get_rect()
    obstimgrects.append(rect)



    #for f in range(0,columnas):

     #   obstimg.append(pg.image.load("obstaculo.png"))
      #  screen.blit(obstimg[f], (x2,y2))
       # rect=obstimg[f].get_rect()
       # obstimgrects.append(rect)
       # rect.left=x2
       # rect.top=y2
       # x2= x2+ 50
       # y2= y2+ 50



    runing=True
    pintar = False
    crearfantasmas=False

    hola=""
    word = "[(0,1)(1,0)(0,4)]"
    word += "\n"
    word += "[(2,2)(1,0)(0,4)]"
    word += "\n"
    word += "[(1,1)(1,1)(1,1)]"


    while runing:
        #crear fantasmas
        if crearfantasmas== False:
            CrearFantasmas(screen,matrizinicial)
            crearfantasmas=True

        print("Vuelta --------------")


        #mostrar matriz
        for row in matrizinicial:
            print(' '.join([str(elem) for elem in row]))


        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                runing = False


        pg.time.delay(1000)
        screen.fill(black)


        #pintar los obstaculos en el mapa
        #for f in range(0, columnas):
         #   screen.blit(obstimg[f], obstimgrects[f])

        #for f in range(0, 2):
        #    screen.blit(obstimg[f], obstimgrects[f])

        screen.blit(obstimg[0], (50, 50))
        screen.blit(obstimg[1], (100, 150))


        arbolito=""

        #print(Libres(3,3,matrizinicial,ancho,alto,word,3,3))
        Libres(3, 3, matrizinicial, ancho, alto, word, 3, 3)

        hola+="1"
        hola+="\n"
        hola+="2"
        chao="[(,1)(1,0)(0,4)]"
        # print(chao[1:5])

        word2 = """[(0,1)(1,0)(0,4)]
                   [(0,1)(1,0)(0,4)] 
                   [(1,1)(1,1)(1,1)]"""
        L = word.splitlines()
        L1=L[0]
        L2 = (L[L.__len__() - 1].split()[0])
        L3 = (L[L.__len__()-1])
        L4 = L3[1:6]

        #print(L)
        #print(L3)
        #print(L4)

        m = '[[1,2,3],[4,5,6],[7,8,9]]'
        m = eval(m.split()[0])




        #mover fantasmas por profundidad
        #for p in range(0, cantidadfantasmas):
         #   (fantasmasimgrect[p],matrizinicial)=Profundidadsinciclos(fantasmasimgrect[p],matrizinicial , ancho , alto)
          #  screen.blit(fantasmasimg[p], fantasmasimgrect[p])


        #mover y pintar fantasmas
        #for p in range(0, cantidadfantasmas):
         #   (fantasmasimgrect[p],matrizinicial)=MoverFantasma(fantasmasimgrect[p],matrizinicial , ancho , alto)
          #  screen.blit(fantasmasimg[p], fantasmasimgrect[p])

        pg.display.update()

def Libres(posicionf,posicionc,matrixobst, ancho , alto, arbol, linkf, linkc):

    # para escoger una direccion disponible
    (arr, aba, der, izq) = (True, True, True, True)

    # para mirar si esta en un borde del mapa
    (bordearr, bordeaba, bordeder, bordeizq) = (False, False, False, False)

    # opciones de movimiento disponibles
    opciones = []

    libres = arbol


    # Miro si esta en un limite del mapa
    # Esta arriba Max, no se puede mover hacia arriba
    if posicionf == 0:
        # print("Esta Arriba")
        arr = False
        bordearr = True

    # Esta abajo Max, no se puede mover hacia abajo
    if posicionf == (alto // 50) - 1:
        # print("Esta Abajo")
        aba = False
        bordeaba = True

    # Esta izquierda Max, no se puede mover hacia la izquierda
    if posicionc == 0:
        # print("Esta a la Izquierda")
        izq = False
        bordeizq = True

    # Esta Derecha Max, no se puede mover hacia la derecha
    if posicionc == (ancho // 50) - 1:
        # print("Esta a la Derecha")
        der = False
        bordeder = True

    # Miro si tiene obstaculos al rededor
    # a la izquierda
    if bordeizq == False:
        if matrixobst[posicionf][posicionc - 1] == 1:
            izq = False
        else:
            izq: True

    # a la derecha
    if bordeder == False:
        if matrixobst[posicionf][posicionc + 1] == 1:
            der = False
        else:
            der = True

    # arriba
    if bordearr == False:
        if matrixobst[posicionf - 1][posicionc] == 1:
            arr = False
        else:
            arr = True

    # abajo
    if bordeaba == False:
        if matrixobst[posicionf + 1][posicionc] == 1:
            aba = False
        else:
            aba = True


    #arbol de forma matricial
    arbolmatrix=""

    #ultimos hijos
    ultimoshijos=""

    #hijo a expandir
    hijo = ""

    #hijo entrante , valor entrante
    hijoentrante = "(" + str(posicionf) + ","+ str(posicionc) + ")"

    #variable para ancestro
    ancestro = False


#####capturo valores para trabajar
    if arbol != "" :
        arbolmatrix = arbol.splitlines()
        ultimoshijos = (arbolmatrix[arbolmatrix.__len__()-1])
        hijo = ultimoshijos[1:6]



#####validar si es ancestro
    if arbol != "" :
        for x in range(0, arbolmatrix.__len__()):
            filahijos = (arbolmatrix[x])
            onehijo = filahijos[1:6]
            if hijoentrante == onehijo:
                ancestro = True




##### validar si la opción que llega es meta
    if matrixobst[posicionf][posicionc] == matrixobst[linkf][linkc]:
        filahijos = (arbolmatrix[1])
        onehijo = filahijos[1:6]
        print("llegamos a la meta, devuelve el primer valor del primer hijo de la raiz" + onehijo)

    ####Validar si es Raiz
    elif arbol == "":
        libres += "[(" + str(posicionf) + "," + str(posicionc) + ")]"
        print("Soy la Raiz, me pongo, pongo mis hijos y mando mi primer hijo para repetir este metodo y seguir creando el arbol ")

    #validar si ya estoy de ancestro.
    elif ancestro == True:
        print("YA ESTA REPETIDO , me quito de la lista y envio a mi hermano. porque ENTRA EN CICLO")

    ######






    libres += "["
    # Agrego opciones de movimientos al array y a libres
    if arr == True:
        opciones.append(4)
        libres += "(" + str(posicionf-1) + "," + str(posicionc) + ")"

    if der == True:
        opciones.append(1)
        libres += "(" + str(posicionf) + "," + str(posicionc+1) + ")"

    if aba == True:
        opciones.append(2)
        libres += "(" + str(posicionf+1)+ "," + str( posicionc) + ")"

    if izq == True:
        opciones.append(3)
        libres += "(" + str(posicionf) + "," + str(posicionc-1) + ")"

    libres += "]"


    return libres


def Profundidadsinciclos(fantasma, matrixobst, ancho , alto, arbol, linkc,linkf):
    #reglas: arriba, derecha, abajo ,izquierda

    global filallave, columnallave, filapuerta, columnapuerta

    # Capturo posicion fantasma
    posicionc = fantasma.left // 50
    posicionf = fantasma.top // 50
    # quedan como posiciones anteriores
    posicioncvieja = posicionc
    posicionfvieja = posicionf




    ##### validar si la opción que llega es meta
    if matrixobst[posicionf][posicionc] == matrixobst[linkf][linkc]:
        print("llegamos a la meta")


    return fantasma, matrixobst


#Crear fantasmas
def CrearFantasmas(screen, a):

    # agregar 0s a arrays de posiciones de fantasmas
    fantasmasimgx = numpy.zeros((cantidadfantasmas), dtype=int)
    fantasmasimgy = numpy.zeros((cantidadfantasmas), dtype=int)

    # crear fantasmas
    for f in range(0, cantidadfantasmas):
        newfantas = pg.image.load("./imgs/fantasma.png")
        newfantas = pg.transform.scale(player, (50, 50))
        fantasmasimg.append(newfantas)
        #(fantasmasimgy[f], fantasmasimgx[f]) = Buscar(a, ancho, alto)
        (fantasmasimgy[f], fantasmasimgx[f])=(0,0)
        screen.blit(fantasmasimg[f], (fantasmasimgx[f], fantasmasimgy[f]))
        rect = fantasmasimg[f].get_rect()
        fantasmasimgrect.append(rect)
        rect.left = fantasmasimgx[f]
        rect.top = fantasmasimgy[f]
        a[fantasmasimgy[f] // 50][fantasmasimgx[f] // 50] = 3


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

#mover fantasmas con la posicion de cada uno , la matriz del mapa, el ancho y alto de la ventana
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
            print("pase por la llave")
            matrixobst[posicionfnueva][posicioncnueva] = 4
            #(filallave,columnallave)=(posicionfnueva,posicioncnueva)

        elif matrixobst[posicionfnueva][posicioncnueva] == 5:
            print("pase por la puerta")
            matrixobst[posicionfnueva][posicioncnueva] = 5
            (filapuerta, columnapuerta) = (posicionfnueva, posicioncnueva)
    else:
        matrixobst[posicionfnueva][posicioncnueva] = 3


    return fantasma, matrixobst




if __name__ == "__main__":
    main()