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
# cargar img del suelo
sueloimg = []

# cargar img obtaculo
obsimg = []

#cargar img fantasma
fantasimg = []
fantasimg= pygame.image.load("fantasma.png")
fantasimg = pygame.transform.scale(fantasimg, (50,50))
fantasrect=fantasimg.get_rect()

#tamaños
width=800
height=600
x=0
y=50


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

    #Personaje Link y llave
    link = pygame.image.load("link1.png")
    link_x = random.randint(0, 3)
    link_y = random.randint(0, 3)
    i=0

    #LLave
    llave = pygame.image.load("key.png")
    llave_x = random.randint(0, 3)
    llave_y = random.randint(0, 3)

    #Icono y titulo ventana
    pygame.display.set_caption("Zelda")
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)

    screen = pygame.display.set_mode((ancho, alto))

    #Loop principal
    running = True
    crearTablero = False
    while running:

        #Crear mapa
        if crearTablero == False:
            movements = ["r", "r", "r"]
            matrizTablero = tablero(screen, ancho, alto)
            valorAnterior = 0

            #Asignacion posicion llave
            matrizTablero[llave_y][llave_x] = 3
            screen.blit(llave, ((llave_x*50)+5, (llave_y*50)+5))
            screenshot = screen.copy()
            screen.blit(screenshot, (0, 0))

            #Asignacion posicion link
            screen.blit(link, (link_x * 50, link_y * 50))
            matrizTablero[link_y][link_x] = 2
            link_y*=50
            link_x*=50

        #Evento para cierre de ventana
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False


        #Movimientos de link
        if i < movements.__len__() and crearTablero == True:

            if movements[i] == "l":
                if link_x >= 50:
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                    valorAnterior = matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)-1]
                    link_x -= 50
                    screen.blit(screenshot, (0, 0))
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2
                    screen.blit(link, (link_x, link_y))

            if movements[i] == "r":
                if link_x <= ancho-100:
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                    valorAnterior = matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)+1]
                    link_x += 50
                    screen.blit(screenshot, (0, 0))
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2
                    screen.blit(link, (link_x, link_y))

            if movements[i] == "u":
                if link_y >= 50:
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                    valorAnterior = matrizTablero[math.ceil(link_y/50)-1][math.ceil(link_x/50)]
                    link_y -= 50
                    screen.blit(screenshot, (0, 0))
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2
                    screen.blit(link, (link_x, link_y))


            if movements[i] == "d":
                if link_y <= alto-100:
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = valorAnterior
                    valorAnterior = matrizTablero[math.ceil(link_y/50)+1][math.ceil(link_x/50)]
                    link_y += 50
                    screen.blit(screenshot, (0, 0))
                    screen.blit(link, (link_x, link_y))
                    matrizTablero[math.ceil(link_y/50)][math.ceil(link_x/50)] = 2

            i+=1

        pygame.display.update()
        pygame.time.delay(500)
        crearTablero = True


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

#Algoritmo de busqueda A* Falta acumular pasos
def asterisco(matriz, link_x, link_y, meta_x, meta_y):
    mov_disp = []

    if link_y-1 >= 0:
        if matriz [link_y-1][link_x] != 1:
            up = matriz[link_y-1][link_x] + calulo_manhatan(link_x, link_y-1, meta_x, meta_y)
            mov_disp+=[up]
        else:
            up = None
    else:
        up = None

    if link_y + 1 <= len(matriz)-1:
        if matriz [link_y+1][link_x] != 1:
            down = matriz[link_y+1][link_x] + calulo_manhatan(link_x, link_y+1, meta_x, meta_y)
            mov_disp+=[down]
        else:
            down = None
    else:
        down = None

    if link_x + 1 <= len(matriz[0])-1:
       if matriz [link_y][link_x+1] != 1:
            rigth = matriz[link_y][link_x+1] +calulo_manhatan(link_x+1, link_y, meta_x, meta_y)
            mov_disp+=[rigth]
       else:
           rigth = None
    else:
        rigth = None

    if link_x - 1 >= 0 :
        if matriz [link_y][link_x-1] != 1:
            left = matriz[link_y][link_x-1] + calulo_manhatan(link_x-1, link_y, meta_x, meta_y)
            mov_disp+=[left]
        else:
            left = None
    else:
        left = None


    #Diccionario con movimientos disponibles
    movements = {left : "l", down : "d", rigth: "r", up : "u"}

    #Ordenar matriz de posibles movimientos
    a = numpy.array([mov_disp])
    a.sort(axis=1)
    mov_ordenados = a[0]
    movimiento = movements.get(mov_ordenados[0])
    return print(movimiento)



#para agregar fantasmas
def fantasmas(screen,matriz):
    screen.blit(fantasimg, (x,y))
    print(matriz)


def calulo_manhatan(link_x, link_y, meta_x, meta_y):
    manhatan=math.ceil(math.fabs(link_x - meta_x)) + math.ceil(math.fabs(link_y - meta_y))

    return manhatan

if __name__ == '__main__':
    #menu()
    main("600 x 400", True, 0, 0)

    """ab=[[0,3,3],[2,5,6]]
    asterisco(ab, 0, 0, 2, 1)"""

    """movi = []
    try:
        if type(ab[0][9]).__name__ == "int":
            movi+=["up"]

        if type(ab[0][0])==0:
            print("entra")
            movi+=["down"]
        if type(ab[0][0]).__name__ == "int":
            movi+=["rigth"]
        if type(ab[3][4]).__name__ == "int":
            movi+=["left"]
    except IndexError:
        pass
    print(len(ab[0]))"""

    """ab=[[1,2],[3,4]]
    derecha = {'direccion':'r', "valor": 3, "manhatan":3}
    izquierda = {'direccion':'l', "valor": 0, "manhatan":2}

    up = 0
    b=[derecha["valor"], izquierda["valor"]]
    movements = {None : "l", None : "d", 0: "r", None : "up" }
    #a = numpy.array([[*movements.keys()]])
    #a.sort(axis=1)
    print(movements.get(0)) """


