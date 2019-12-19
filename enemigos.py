import pygame as pg

black = 32, 32, 32

class GameObject:
    def __init__(self, image, height, speed):
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0, height)

    def move(self):
        self.pos = self.pos.move(self.speed, -1)

        #lados
        if self.pos.right > 640:
            #self.pos.left = 0
            self.speed=-1
            #self.pos.right = 0
            #self.speed = -1 * self.speed
        if self.pos.left < 0:
            #self.pos.right = 590
            self.speed=1

        #up/down
        if self.pos.top > 480:
            #self.speed = 1
            self.pos.top=0
            #self.pos=self.pos.move(-self.speed,1)


            #self.speed = 10
        if self.pos.top < 0:
            self.speed = 1
            self.pos.top = 479
            #self.speed = 10



# here's the full code
def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))



    player = pg.image.load("fantasma.png")
    background = pg.image.load("link.png")
    player = pg.transform.scale(player, (50, 50))

    # scale the background image so that it fills the window and
    #   successfully overwrites the old sprite position.
    background = pg.transform.scale2x(background)
    background = pg.transform.scale2x(background)
    background = pg.transform.scale2x(background)

    screen.blit(background, (0, 0))

    objects = []
    for x in range(3):
        o = GameObject(player, x * 50, x+5)
        objects.append(o)

    while 1:
        for event in pg.event.get():
            if event.type in (pg.QUIT, pg.KEYDOWN):
                return

        for o in objects:
            screen.blit(background, o.pos, o.pos)
            pg.display.update()
        for o in objects:

            o.move()
            #screen.blit(background, o.pos, o.pos)
            screen.blit(o.image, o.pos)
            pg.display.update()
            #screen.blit(background, o.pos, o.pos)

        pg.display.update()
        pg.time.delay(10)
        screen.fill(black)
        #screen.blit(background, o.pos, o.pos)
        screen.blit(background, (0, 0))



if __name__ == "__main__":
    main()