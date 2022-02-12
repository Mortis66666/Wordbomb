import pygame


pygame.font.init()

width, height = 1000, 600
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Word Bomb")


#colours
white = (233,233,233)
black = (0,0,0)



class Bomb:

    def __init__(self, index) -> None:
        self.index = index
        self.y = 0
        self.x = index * 100

    def blit(self):
        pygame.draw.circle(win, black, (self.x, self.y), 20)



class Game:

    def draw_window(self):
        win.fill(white)

        Bomb(1).blit()


        pygame.display.update()

    def start(self):

        run = True
        clock = pygame.time.Clock()
        fps = 60


        while run:

            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            self.draw_window()


if __name__ == '__main__':
    game = Game()

    game.start()

        


