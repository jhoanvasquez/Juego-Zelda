import random
from tkinter import filedialog

import pygame
import numpy
import math
from tkinter import *
import tkinter as tk
import pyautogui


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
player = pygame.image.load("fantasma.png")
player = pygame.transform.scale(player, (50, 50))



#lugarllave
filallave=(alto // 50)-1
columnallave=(ancho // 50)-1

#lugarpuerta
filapuerta=(alto // 50) - 1
columnapuerta=0




# menu de inicio
def menu():


    raiz = tk.Tk()
    frame = Frame(raiz, width=350, height=400)
    raiz.resizable(0, 0)

    # icono
    raiz.iconbitmap(r'icon.ico')

    # labels
    label1 = Label(frame, text="Menú del juego", width=100, height=25, font=("", 15), anchor='nw')
    label1.place(x=5, y=5)


    label2 = Label(frame, text="Dimensiones de la patalla", width=100, height=25, font=("", 12), anchor='nw')
    label2.place(x=15, y=50)

    label3 = Label(frame, text="Personalizar tablero:", width=100, height=25, font=("", 12), anchor='nw')
    label3.place(x=15, y=95)

    label4 = Label(frame, text="Dificultad del juego", width=100, height=25, font=("", 12), anchor='nw')
    label4.place(x=15, y=170)

    # combo
    variable = StringVar(raiz)
    variable.set("600 x 400")
    combo = OptionMenu(raiz, variable, "800 x 600", "600 x 400", "400 x 200")
    combo.place(x=240, y=45)

    # botones
    def btn():
        raiz.destroy()
        main(variable.get(), aleatorio, ancho, alto)

    def personalizar():
        choosePerso = filedialog.askopenfilename(filetypes=(("Archivos de texto", "*.txt"),))
        if choosePerso != "":
            btnPerso.config(text="☑")
            raiz.update()
            global aleatorio
            aleatorio = False
            global alto
            global ancho


            archivo = open(choosePerso, "r")
            tablero = archivo.readline()
            archivo.close()


            alto = math.ceil(len(tablero.split(" "))/2) * 100
            ancho = math.ceil(len(tablero.split(" ")[0].split(","))/2) * 100



    btnInicio = Button(frame, text="Inicio", width=20, command=btn)
    btnInicio.place(x=105, y=350)

    btnPerso = Button(frame, text="Seleccionar archivo", width=44,  command=personalizar)
    btnPerso.place(x=15, y=130)

    # radio button
    r1 = Radiobutton(raiz, text="Normal",  value=1)
    r2 = Radiobutton(raiz, text="Dificil",  value=0)
    r1.place(x=240, y=170)
    r2.place(x=240, y=195)

    #dimensiones ventana
    raiz.geometry('{}x{}+{}+{}'.format(350, 400, (raiz.winfo_screenwidth() // 2) - 150, (raiz.winfo_screenheight() // 2) - 200))
    raiz.title("Zelda")
    frame.pack()
    raiz.tk.mainloop()


# inicio del juego
def main(dimension, aleatorio, anchoPerso, altoPerso):
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

        ancho = anchoPerso
        alto = altoPerso
    pygame.init()

    #Suelo
    suelo = pygame.image.load("piso.png")

    #Personaje Link
    link = pygame.image.load("link1.png")
    link_x = random.randint(0, 2)
    link_y = random.randint(0, 2)
    i=0

    #LLave

    llave = pygame.image.load("key.png")
    llave_x = random.randint(2, ((ancho/100)*2)-1)
    llave_y = random.randint(2, ((alto/100)*2)-1)

    meta_x = llave_x
    meta_y = llave_y

    #Puerta

    puerta = pygame.image.load("puerta.png")
    puerta_x = math.ceil(ancho/2)-50
    puerta_y = 0
    pygame.display.set_caption("Zelda")
    icon = pygame.image.load("icon.png")
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
            matrizTablero = tablero(screen, ancho, alto)
            valorAnterior = 0

            #Asignacion posicion llave y puerta
            while matrizTablero[llave_y][llave_x] == 1:
                llave_x = random.randint((ancho/100)-1, ancho/100)
                llave_y = random.randint((alto/100)-1, alto/100)
            matrizTablero[llave_y][llave_x] = 4
            screen.blit(llave, ((llave_x*50)+5, (llave_y*50)+5))



            screen.blit(puerta, (puerta_x-25 , puerta_y-9))

            #Tomar fondo del juego
            global screenshot
            screenshot = screen.copy()
            screen.blit(screenshot, (0, 0))

            #Asignacion posicion link
            while matrizTablero[link_y][link_x] == 1:

                link_x = random.randint(link_x, link_x+3)
                link_y = random.randint(link_y, link_y+3)


            screen.blit(link, (link_x * 50, link_y * 50))
            matrizTablero[link_y][link_x] = 2
            link_y*=50
            link_x*=50

            #Asignacion posicion puerta

            matrizTablero[math.ceil(puerta_y*2/100)][math.ceil(puerta_x*2/100)] = 5


            #Creacion de fantasmas
            CrearFantasmas(screenshot, matrizTablero, ancho,alto)

            #gasto de cada movimiento
            matrizGasto = numpy.zeros((len(matrizTablero),len(matrizTablero[0])))


            for i in range(0, len(matrizTablero)):
                for j in range (0, len(matrizTablero[0])):
                    if matrizTablero[i][j] == 1:
                        matrizGasto[i][j] = None
                    if matrizTablero[i][j] == 4:
                        matrizGasto[i][j] = 0

        #Evento para cierre de ventana
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

        #Ejecucion algoritmo de busqueda
        if math.ceil(link_x/50) == llave_x and math.ceil(link_y/50) == llave_y:
            llave_x = math.ceil(puerta_x/50)
            llave_y = math.ceil(puerta_y/50)

            if ctrl_puerta == 0:
                suelo1 = pygame.transform.scale(suelo, (97, 100))
                screen.blit(suelo1, (link_x-24, link_y-24.8))
                screenshot = screen.copy()
                screen.blit(screenshot, (0, 0))
            matrizUpdate(matrizTablero, matrizGasto)
            movimiento = asterisco(matrizGasto,math.ceil(link_x/50)  , math.ceil(link_y/50), llave_x , llave_y)
            ctrl_puerta += 1

            if ctrl_puerta > 1:
                movimiento = None

        else:
            matrizUpdate(matrizTablero, matrizGasto)
            movimiento = asterisco(matrizGasto,math.ceil(link_x/50), math.ceil(link_y/50) ,llave_x , llave_y)


        #Movimientos de link
        if crearTablero == True:

            if movimiento == "l":
                if link_x >= 50:
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                    valorAnterior = matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)-1]
                    link_x -= 50
                    screen.blit(screenshot, (0, 0))
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2
                    matrizGasto[math.ceil(link_y/50)][math.ceil(link_x/50)+1] +=1
                    screen.blit(link, (link_x, link_y))


            if movimiento == "r":
                if link_x <= ancho-100:
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                    valorAnterior = matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)+1]
                    link_x += 50
                    screen.blit(screenshot, (0, 0))
                    matrizGasto[math.ceil(link_y/50)][math.ceil(link_x/50)-1]+=1
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2
                    screen.blit(link, (link_x, link_y))

            if movimiento == "u":
                if link_y >= 50:
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                    valorAnterior = matrizTablero[math.ceil(link_y/50)-1][math.ceil(link_x/50)]
                    link_y -= 50
                    screen.blit(screenshot, (0, 0))
                    matrizGasto[math.ceil(link_y/50)+1][math.ceil(link_x/50)] += 1
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2
                    screen.blit(link, (link_x, link_y))

            if movimiento == "d":
                if link_y <= alto-100:
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                    valorAnterior = matrizTablero[math.ceil(link_y/50)+1][math.ceil(link_x/50)]
                    link_y += 50
                    screen.blit(screenshot, (0, 0))
                    matrizGasto[math.ceil(link_y/50)-1][math.ceil(link_x/50)] += 1
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2
                    screen.blit(link, (link_x, link_y))

         # mover y pintar fantasmas
        for p in range(0, cantidadfantasmas):
                (fantasmasimgrect[p], a) = MoverFantasma(fantasmasimgrect[p], matrizTablero, ancho, alto)
                screen.blit(fantasmasimg[p], fantasmasimgrect[p])

        # mover y pintar fantasmas
        if moverenemigos == True:
            for p in range(0, cantidadfantasmas):
                (fantasmasimgrect[p], a) = MoverFantasma(fantasmasimgrect[p], matrizTablero, ancho, alto)
                screen.blit(fantasmasimg[p], fantasmasimgrect[p])
                #print(matrizTablero)

        crearTablero = True
        moverenemigos=True
        pygame.time.delay(500)
        pygame.display.update()

# tablero del juego
def tablero (screen, ancho, alto):
    # ciclo para suelo
    for j in range(0, (math.ceil(alto / 100)) * 2):
        for i in range(0, (math.ceil(ancho / 100)) * 2):
            sueloimg.append(pygame.image.load("piso.png"))
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
            obsimg.append(pygame.image.load("obstaculo.png"))
            screen.blit(obsimg[z], (posicionX, posicionY))
    return matrizObstaculos

#Algoritmo de busqueda A*
def asterisco(matriz, link_x, link_y, meta_x, meta_y):
    mov_disp = []

    if link_y-1 >= 0:
        up = matriz[link_y-1][link_x] + calulo_manhatan(link_x, link_y-1, meta_x, meta_y)
        mov_disp+=[up]

    else:
        up = None

    if link_y + 1 <= len(matriz)-1:
        down = matriz[link_y+1][link_x] + calulo_manhatan(link_x, link_y+1, meta_x, meta_y)
        mov_disp+=[down]

    else:
        down = None

    if link_x + 1 <= len(matriz[0])-1:
        rigth = matriz[link_y][link_x+1] +calulo_manhatan(link_x+1, link_y, meta_x, meta_y)
        mov_disp+=[rigth]

    else:
        rigth = None

    if link_x - 1 >= 0 :
            left = matriz[link_y][link_x-1] + calulo_manhatan(link_x-1, link_y, meta_x, meta_y)
            mov_disp+=[left]
    else:
        left = None


    #Diccionario con movimientos disponibles
    movements = {left : "l", down : "d", rigth: "r", up : "u"}

    #Ordenar matriz de posibles movimientos
    a = numpy.array([mov_disp])
    a.sort(axis=1)
    mov_ordenados = a[0]
    movimiento = movements.get(mov_ordenados[0])
    return movimiento


 
#para fantasmas
#Crear fantasmas
def CrearFantasmas(screen, a, ancho,alto):

    # agregar 0s a arrays de posiciones de fantasmas
    fantasmasimgx = numpy.zeros((cantidadfantasmas), dtype=int)
    fantasmasimgy = numpy.zeros((cantidadfantasmas), dtype=int)

    # crear fantasmas
    for f in range(0, cantidadfantasmas):
        newfantas = pygame.image.load("fantasma.png")
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
             if tablero[x][i] == 0 and gastos[x][i] == 3 and \
                     (tablero[x-1][i] != 2 or tablero[x+1][i] != 2 or tablero[x][i-1] != 2 or tablero[x][i+1] != 2):
                gastos[x][i] = 0
    except :
        pass

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



def calulo_manhatan(link_x, link_y, meta_x, meta_y):
    manhatan=math.ceil(math.fabs(link_x - meta_x)) + math.ceil(math.fabs(link_y - meta_y))
    return manhatan

if __name__ == '__main__':

    menu()

    main("400 x 200", True, 0, 0)

    #menu()
    main("600 x 400", True, 0, 0)


#Falta pitar llave, arbol, personalizar juegos parte de componentes