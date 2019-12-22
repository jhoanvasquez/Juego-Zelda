import random
import pygame
import numpy
import math
from tkinter import *
import tkinter as tk
import pyautogui


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

    label3 = Label(frame, text="Dificultad del juego", width=100, height=25, font=("", 12), anchor='nw')
    label3.place(x=15, y=95)

    # combo
    variable = StringVar(raiz)
    variable.set("600 x 400")
    combo = OptionMenu(raiz, variable, "800 x 600", "600 x 400", "400 x 200")
    combo.place(x=240, y=45)

    # botones
    def btn():
        raiz.destroy()
        main(variable.get())

    btnPoblacion = Button(frame, text="Inicio", width=20, command=btn)
    btnPoblacion.place(x=105, y=350)


    # radio button
    r1 = Radiobutton(raiz, text="Normal",  value=1)
    r2 = Radiobutton(raiz, text="Dificil",  value=0)
    r1.place(x=240, y=95)
    r2.place(x=240, y=120)

    #dimensiones ventana
    raiz.geometry('{}x{}+{}+{}'.format(350, 400, (raiz.winfo_screenwidth() // 2) - 150, (raiz.winfo_screenheight() // 2) - 200))
    raiz.title("Zelda")
    frame.pack()
    raiz.tk.mainloop()


# inicio del juego
def main(dimension):

    if dimension == "800 x 600":
        ancho = 800
        alto =600

    if dimension == "600 x 400":
        ancho = 600
        alto =400

    if dimension == "400 x 200":
        ancho = 400
        alto = 200

    pygame.init()

    #Personaje Link y llave
    link = pygame.image.load("link1.png")
    link_x = 0
    link_y = 0
    i=0

    #LLave
    llave = pygame.image.load("key.png")
    llave_x = (random.randint(0, 3)*50) + 5
    llave_y = (random.randint(0, 3)*50) + 5

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
            movements = ["b", "b", "b", "r", "r", "r", "l", "t", "t", "b"]
            matrizTablero = tablero(screen, ancho, alto)
            screen.blit(llave, (llave_x, llave_y))
            screenshot = screen.copy()
            screen.blit(screenshot, (0, 0))
            screen.blit(link, (link_x, 0))


        #Evento para cierre de ventana
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False


        #Movimientos de link
        if i < movements.__len__() and crearTablero==True:

            if movements[i] == "l":
                if link_x >= 50:
                    link_x -= 50
                    screen.blit(screenshot, (0, 0))
                    screen.blit(link, (link_x, link_y))

            if movements[i] == "r":
                if link_x <= ancho-100:
                    link_x += 50
                    screen.blit(screenshot, (0, 0))
                    screen.blit(link, (link_x, link_y))

            if movements[i] == "t":
                if link_y >= 50:
                    link_y -= 50
                    screen.blit(screenshot, (0, 0))
                    screen.blit(link, (link_x, link_y))

            if movements[i] == "b":
                if link_y <= alto-100:
                    link_y += 50
                    screen.blit(screenshot, (0, 0))
                    screen.blit(link, (link_x, link_y))
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


def asterisco(matriz, link_x, link_y, meta_x, meta_y):
     eureka = False

     while(eureka==False):
         pass
 

#para agregar fantasmas
def fantasmas(screen,matriz):
    screen.blit(fantasimg, (x,y))
    print(matriz)


if __name__ == '__main__':
    #menu()
    main("600 x 400")
