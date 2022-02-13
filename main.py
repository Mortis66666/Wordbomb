import pygame
import math
import random
import time
from enum import Enum
from datetime import datetime


pygame.font.init()

width, height = 1000, 600
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Word Bomb")

font = pygame.font.SysFont("archivo", 30)
boom = pygame.font.SysFont("archivo", 25)

gameover = pygame.USEREVENT + 1

#colours
white = (233, 233, 233)
black = (0, 0, 0)
red = (233, 0, 0)


class status(Enum):
    OK = 1
    EXPLODE = 2
    DESTROYED = 3


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

                if self.y - 30 > height:
                    pygame.event.post(pygame.event.Event(gameover))

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


    def handle(self, key, score) -> int:

        if pygame.key.name(key).upper() == self.char:
            self.explode()
            score += 1
        
        return score
    

class Game:

    bombs = []

    def draw_window(self):
        win.fill(white)

        for bomb in self.bombs:
            if not bomb.blit():
                self.bombs.remove(bomb)

        pygame.display.update()

    def random_bombs(self, k) -> set:

        return set(
            random.choices(
                list(range(10)),
                k = random.randint(1,k)
            )
        )

    def make_bombs(self, start):

        k = math.ceil((time.time() - start) / 10 + 3)

        for bomb in self.random_bombs(k):
            self.bombs.append(Bomb(bomb))

    def start(self):

        run = True
        clock = pygame.time.Clock()
        fps = 60
        score = 0
        start = time.time()
        last_make = 0

        while run:
            clock.tick(fps)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    return

                elif event.type == gameover:
                    text = font.render("Gameover", True, black)
                    sco = font.render(f"Score: {score}", True, black)
                    win.blit(text, (width//2-text.get_width(), 0))
                    win.blit(sco, (width//2-text.get_width(), text.get_height()))

                    with open("logs.txt", "a") as logs:
                        print(datetime.now().strftime("[%d/%m/%Y %H:%M]: "),str(score), file=logs)

                    print("Score: ", score)

                    pygame.display.update()

                    time.sleep(1.5)
                    self.bombs.clear()
                    self.start()

                
                elif event.type == pygame.KEYDOWN:
                    for bomb in self.bombs:
                        score = bomb.handle(event.key, score)
                

            self.draw_window()

            if (n:=time.time()) - last_make >= 3:
                self.make_bombs(start)
                last_make = n



if __name__ == '__main__':
    game = Game()
    game.start()
   