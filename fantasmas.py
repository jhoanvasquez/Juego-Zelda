import pygame as pg

black = 32, 32, 32
(x,y)=(40,40)

def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))



    player = pg.image.load("fantasma.png")
    background = pg.image.load("link.png")
    player = pg.transform.scale(player, (50, 50))

    # scale the background image so that it fills the window and
    #   successfully overwrites the old sprite position.
    background = pg.transform.scale2x(background)



    #screen.blit(background, (100, 100))
    runing=True


    while runing:
        global x,y
        for evento in pg.event.get():
            if evento.type == pg.QUIT:
                runing = False

            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_LEFT:
                    x = x-20
                if evento.key == pg.K_RIGHT:
                    x = x+20
                if evento.key == pg.K_DOWN:
                    y = y+20
                if evento.key == pg.K_UP:
                    y = y-20



        pg.time.delay(10)
        screen.fill(black)
        screen.blit(background, (100, 100))
        screen.blit(player, (x, y))
        pg.display.update()



if __name__ == "__main__":
    main()