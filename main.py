import pygame
import sys
import random
import time
import threading
from enum import Enum


pygame.font.init()

width, height = 1000, 600
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Word Bomb")

font = pygame.font.SysFont("archivo", 30)
boom = pygame.font.SysFont("archivo", 25)


#colours
white = (233, 233, 233)
black = (0, 0, 0)
red = (233, 0, 0)


class status(Enum):
    OK = 1
    EXPLODE = 2
    DESTROYED = 3

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,  *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class Bomb:

    def __init__(self, index) -> None:
        self.index = index
        self.y = 30
        self.x = index * 100 + 30
        self.status = status.OK
        self.char = random.choice("`1234567890-=qwertyuiop[]\\asdfghjkl;'zxcvbnm,./").upper()
        self.display = 0


    def blit(self) -> bool:

        match self.status:

            case status.OK:

                pygame.draw.circle(win, black, (self.x, self.y), 30)
                text = font.render(self.char, True, white)
                win.blit(text, (self.x - 10, self.y - 10))
                self.down()

                return True

            case status.EXPLODE:

                pygame.draw.circle(win, red, (self.x, self.y), 30)
                text = font.render("BOOM", True, white)
                win.blit(text, (self.x - 30, self.y - 10))
                self.display += 1

                if self.display == 80:
                    self.status = status.DESTROYED

                return True

            case status.DESTROYED:

                return False

    
    def explode(self):
        self.status = status.EXPLODE

    
    def down(self):
        self.y += 2


    def handle(self, key):

        if pygame.key.name(key).upper() == self.char:
            self.explode()
    

class Game:

    bombs = []

    def draw_window(self):
        win.fill(white)

        for bomb in self.bombs:
            if not bomb.blit():
                self.bombs.remove(bomb)

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

        thread = StoppableThread(target=self.make_bombs)
        thread.start()


        while run:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    thread.stop()
                elif event.type == pygame.KEYDOWN:
                    for bomb in self.bombs:
                        bomb.handle(event.key)
                

            self.draw_window()



if __name__ == '__main__':
    game = Game()
    game.start()
   