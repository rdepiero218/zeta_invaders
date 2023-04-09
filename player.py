import pygame, os, sys
from pygame.locals import *

from bullet import *
from bitmapfont import *

## PLAYER MODEL
class PlayerModel(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lives = 3
        self.score = 0
        self.speed = 100 # pixels per second
        

## PUT TANK AT BOTTOM OF SCREEN
class PlayerController(object):
    def __init__(self, x, y):
        self.model = PlayerModel(x, y)
        self.isPaused = False
        self.bullets = BulletController(-200) # pixels per sec
        self.shootSound = pygame.mixer.Sound('audio/playershoot.wav')
        
    def pause(self, isPaused): # prevent player from moving
        self.isPaused = isPaused
        
    def update(self, gameTime):
        self.bullets.update(gameTime)
        
        if (self.isPaused):
            return
            
        keys = pygame.key.get_pressed()
        
        if(keys[K_RIGHT] and self.model.x < 800 - 32):
            self.model.x += (gameTime / 1000.0) * self.model.speed
        elif (keys[K_LEFT] and self.model.x > 0):
            self.model.x -= (gameTime / 1000.0) * self.model.speed
            
        if (keys[K_SPACE] and self.bullets.canFire()):
            x = self.model.x + 9 # bullet is 8 pixels
            y = self.model.y - 16
            self.bullets.addBullet(x, y)
            self.shootSound.play()
            
    def hit(self, x, y, width, height): # test collisions
        return (x >= self.model.x and y >= self.model.y and x + width <= self.model.x + 32 and y + height <= self.model.y + 32)


## RENDERS PLAYER TANK

class PlayerView(object):
    def __init__(self, player, imgpath):
        self.player = player
        self.image = pygame.image.load(imgpath)
        
    def render(self, surface):
        surface.blit(self.image, (self.player.model.x, self.player.model.y, 32, 32))

## RENDERS NUMBER OF LIVES
class PlayerLivesView(object):
    def __init__(self, player, imgpath):
        self.player = player
        self.image = pygame.image.load(imgpath)
        self.font = BitmapFont('images/placeholder_font.png', 12, 12)
        
    def render(self, surface):
        x = 8

        self.font.draw(surface, 'LIVES ', (800-32)-(3*40)-(6*8), 24)
        
        for life in range(0, self.player.model.lives):
            surface.blit(self.image, ((800-32)-x, 8, 32, 32))
            x += 40
            
        self.font.draw(surface, 'SCORE  ' + str(self.player.model.score), 32, 24)
        
        
        
### FOR TESTING CLASS

if (__name__ == '__main__'):
    
    pygame.init()
    fpsClock = pygame.time.Clock()
    
    surface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Player Test')
    black = pygame.Color(0, 0, 0)
    
    player = PlayerController(0, 400)
    playerView = PlayerView(player, 'images/tank.png')
    playerLivesView = PlayerLivesView(player, 'images/tank.png')
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        player.update(fpsClock.get_time())
        
        surface.fill(black)
        playerView.render(surface)
        playerLivesView.render(surface)
        
        pygame.display.update()
        fpsClock.tick(30)
