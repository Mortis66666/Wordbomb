import pygame
import random
import time
from threading import Thread



pygame.font.init()

width, height = 1000, 600
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Word Bomb")

font = pygame.font.SysFont("archivo", 30)


#colours
white = (233,233,233)
black = (0,0,0)



class Bomb:

    def __init__(self, index) -> None:
        self.index = index
        self.y = 30
        self.x = index * 100 + 30
        self.available = True
        self.char = random.choice("`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./").upper()

    def blit(self):
        pygame.draw.circle(win, black, (self.x, self.y), 30)
        text = font.render(self.char, True, white)
        win.blit(text, (self.x - 10, self.y - 10))



class Game:

    bombs = []

    def draw_window(self):
        win.fill(white)

        for bomb in self.bombs:
            bomb.blit()

        pygame.display.update()

    def random_bombs(self) -> set:

        return set(
            random.choices(
                list(range(10)),
                k = random.randint(1,3)
            )
        )

    def make_bombs(self):

        while True:
            for bomb in self.random_bombs():
                self.bombs.append(Bomb(bomb))
            time.sleep(3)

    def start(self):

        run = True
        clock = pygame.time.Clock()
        fps = 60

        thread = Thread(target=self.make_bombs)
        thread.start()


        while run:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                

            self.draw_window()



if __name__ == '__main__':
    game = Game()
    game.start()
   