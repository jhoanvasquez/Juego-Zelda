import random
import pygame
import numpy
import math
from tkinter import *
import tkinter as tk

# cargar img del suelo
sueloimg = []

# cargar img obtaculo
obsimg = []

fantasmimg = []



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
    variable.set("800 x 600")
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
    pygame.display.set_caption("Zelda")
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    screen = pygame.display.set_mode((ancho, alto))
    running = True
    crearTablero = False
    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
        if crearTablero == False:
            tablero(screen, ancho, alto)
            pygame.display.update()
        crearTablero = True


# tablero del juego
def tablero(screen, ancho, alto):
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
    personaje(screen, matrizObstaculos)

#para agregar fantasmas
    fantasimg = imagen("fantasma.png", True)
    fantasimg = pygame.transform.scale(fantasimg, (50,50))
    screen.blit(fantasimg, (0,0))

#para agregar imagenes
def imagen (filename, transparente = False) :
        try : image = pygame.image.load(filename)
        except pygame.error as message:
            raise SystemExit(message)
        image = image.convert()
        if transparente:
                color = image.get_at(( 0, 0))
                image.set_colorkey( color)
        return image


def personaje(screen, matrizObstaculos):
    link = pygame.image.load("link.png")
    if matrizObstaculos[0][0] != 1 and matrizObstaculos[0][1] != 1:
        matrizObstaculos[0][0] = 2
        screen.blit(link, (0, 0))


if __name__ == '__main__':
    menu()

