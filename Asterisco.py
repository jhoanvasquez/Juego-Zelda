import math
import numpy
class Asterisco:

    def __init__(self, matriz, link_x, link_y, meta_x, meta_y):
        mov_disp = []
        movimiento = []

        link_x = link_x//100
        link_y = link_y//100
        self.matriz = numpy.zeros((len(matriz),len(matriz[0])))
        self.matriz = Asterisco.bloques(self.matriz, matriz)

        while link_x != meta_x and link_y != meta_y:

            if link_y-1 >= 0:
                up = self.matriz[link_y-1][link_x] + Asterisco.calulo_manhatan(link_x, link_y-1, meta_x, meta_y)
                mov_disp+=[up]

            else:
                up = None

            if link_y + 1 <= len(matriz)-1:
                down = self.matriz[link_y+1][link_x] + Asterisco.calulo_manhatan(link_x, link_y+1, meta_x, meta_y)
                mov_disp+=[down]

            else:
                down = None

            if link_x + 1 <= len(matriz[0])-1:
                rigth = self.matriz[link_y][link_x+1] + Asterisco.calulo_manhatan(link_x+1, link_y, meta_x, meta_y)
                mov_disp+=[rigth]

            else:
                rigth = None

            if link_x - 1 >= 0 :
                left = self.matriz[link_y][link_x-1] + Asterisco.calulo_manhatan(link_x-1, link_y, meta_x, meta_y)
                mov_disp+=[left]
            else:
                left = None


            #Diccionario con movimientos disponibles
            movements = {left : "l", down : "d", rigth: "r", up : "u"}

            #Ordenar matriz de posibles movimientos
            a = numpy.array([mov_disp])
            a.sort(axis=1)
            mov_ordenados = a[0]
            movimiento += movements.get(mov_ordenados[0])


            #Actualizar posocion link
            if movements.get(mov_ordenados[0]) == "u":
                link_y -= 1

            if movements.get(mov_ordenados[0]) == "d":
                link_y += 1

            if movements.get(mov_ordenados[0]) == "l":
                link_x -= 1

            if movements.get(mov_ordenados[0]) == "r":
                link_x += 1

            self.matriz[link_y][link_x] = 2
            print (self.matriz)
            a = []
            mov_disp = []
            mov_ordenados = []

        print (str(link_x) +"="+str(meta_x))
        print (str(link_y) + "=" +str(meta_y))
        self.arrayMov = movimiento


    def calulo_manhatan(link_x, link_y, meta_x, meta_y):
      manhatan=math.ceil(math.fabs(link_x - meta_x)) + math.ceil(math.fabs(link_y - meta_y))
      return manhatan

    def bloques(matriz, matrizT):
        for i in range(0, len(matriz)):
            for j in range(0, len(matriz[0])):
                if matrizT[i][j] == 0:
                    matriz[i][j] = 0
                if matrizT[i][j] == 3:
                    matriz[i][j] = 3
                if matrizT[i][j] == 4:
                    matriz[i][j] = 1
                if matrizT[i][j] == 5:
                    matriz[i][j] = 1
                if matrizT[i][j] == 2:
                    matriz[i][j] = 2
                if matrizT[i][j] == 1:
                   matriz[i][j] = None
        return matriz