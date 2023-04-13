import pygame, os, sys
from pygame.locals import *

from bullet import *

class brickModel(object):
    
    def __init__(self, x, y, imgX, imgY): 
        '''
        add params here that are like alientype and aniframe - blockX & blockY 
        indicate where at in barn image for easy calling later (since will have diff x positions for each new barn in the set.)
        '''
        self.x = x
        self.y = y
        self.imgX = imgX # coords of barn sprite for each brick doesn't change for each barn
        self.imgY = imgY

    def hit(self, x, y, width, height):
        return (
            x >= self.x
            and y >= self.y
            and x + width <= self.x + 10
            and y + height <= self.y + 10
        )

class barnBuilder(object):
    
    def __init__(self):
        self.bricks = []

        for b in range(50, 800, 200): 
            for row in range(10):
                for col in range(10):
                    brick = brickModel((col * 10) + b, (row*10) + 500, col * 10, row * 10)
                    self.bricks.append(brick)
        ## for testing
        # for b in self.bricks:
        #     print('x: ', b.x, 'y: ', b.y)

class barnView:
    
    def __init__(self, bricks, imgpath):
        self.image = pygame.image.load(imgpath)
        self.bricks = bricks

    def render(self, surface):
        for b in self.bricks.bricks:
            surface.blit(
                self.image,
                (b.x, b.y),  # these should be in the brick info otherwise bullet can't collide with it properly
                (b.imgX, b.imgY, 10, 10),
            )
 

 ### FOR TESTING CLASS

if __name__ == "__main__":
    pygame.init()
    fpsClock = pygame.time.Clock()

    surface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Player Test")
    black = pygame.Color(0, 0, 0)

    imgpath = 'images/barn.png'
    barn = barnBuilder()
    barn_view = barnView(barn, imgpath)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        surface.fill(black)
        barn_view.render(surface)

        pygame.display.update()
        fpsClock.tick(30)


