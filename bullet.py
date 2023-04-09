import pygame, os, sys
from pygame.locals import *


### GIVES SINGLE BULLET TO PLAYER

class BulletModel(object):
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def update(self, delta):
        self.y = self.y + delta
        

# manages update for each bullet

class BulletController(object):
    
    def __init__(self, speed): ## creates blank array of bullet objects
        self.countdown = 0
        self.bullets = []
        self.speed = speed
        
    def clear(self): ## clear the bullet list
        self.bullets[:] = []
    
    def canFire(self): # if countdown expired and < 3 bullets active
        return self.countdown == 0 and len(self.bullets) < 3
        
    def addBullet(self, x, y): # bullet added, countdown to 1
        self.bullets.append(BulletModel(x,y))
        self.countdown = 1000
        
    def removeBullet(self, bullet): # remove bullet if kill or off screen
        self.bullets.remove(bullet)
        
    def update(self, gameTime): 
        
        killList = []
        
        if (self.countdown > 0):
            self.countdown = self.countdown - gameTime
        else:
            self.countdown = 0
        
        for b in self.bullets:
            b.update(self.speed * (gameTime / 1000.0) )
            if (b.y < 0):
                killList.append(b)
                
        for b in killList:
            self.removeBullet(b)
            
            
class BulletView(object):
    def __init__(self, bulletController, imgpath):
        self.BulletController = bulletController
        self.image = pygame.image.load(imgpath)
        
    def render(self, surface):
        for b in self.BulletController.bullets:
            surface.blit(self.image, (b.x, b.y, 8, 8))
    
