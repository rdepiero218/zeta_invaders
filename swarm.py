import pygame, os, sys
from pygame.locals import *

from bullet import *


class InvaderModel(object):
    def __init__(self, x, y, alientype):
        self.x = x
        self.y = y
        self.alientype = alientype
        self.animframe = 0

    def flipframe(self):
        if self.animframe == 0:
            self.animframe = 1
        else:
            self.animframe = 0

    def hit(self, x, y, width, height):
        return (
            x >= self.x
            and y >= self.y
            and x + width <= self.x + 32
            and y + height <= self.y + 32
        )


class SwarmController(object):
    def __init__(self, scrwidth, offsety, initialframeticks):

        self.currentframecount = initialframeticks
        self.framecount = initialframeticks

        self.invaders = []
        self.sx = -8

        self.movedown = False
        self.alienslanded = False

        self.bullets = BulletController(200)  # pixels per sec
        self.alienShooter = 3  # each 3d alien to start with, fires
        self.bulletDropTime = 2500
        self.shootTimer = (
            self.bulletDropTime
        )  # each bullet is fired in this ms interval

        self.currentShooter = 0  # current shooting alien

        # OG version
        # for y in range(7):
        # 	for x in range(10):
        # 		invader = InvaderModel(160 + (x *48) + 8, (y *32) + offsety, y % 3)
        # 		self.invaders.append(invader)
        self.init_rows = 5
        self.init_cols = 11

        for y in range(self.init_rows):
            if y == 0:
                for x in range(self.init_cols):
                    invader = InvaderModel(160 + (x * 48) + 8, (y * 32) + offsety, 0)
                    self.invaders.append(invader)
            if y > 0 and y < 3:
                for x in range(self.init_cols):
                    invader = InvaderModel(160 + (x * 48) + 8, (y * 32) + offsety, 1)
                    self.invaders.append(invader)
            if y >= 3:
                for x in range(self.init_cols):
                    invader = InvaderModel(160 + (x * 48) + 8, (y * 32) + offsety, 2)
                    self.invaders.append(invader)

    def reset(self, offsety, ticks):
        self.invaders = []
        self.currentframecount = ticks
        self.framecount = ticks

        for y in range(self.init_rows):
            if y == 0:
                for x in range(self.init_cols):
                    invader = InvaderModel(160 + (x * 48) + 8, (y * 32) + offsety, 0)
                    self.invaders.append(invader)
            if y > 0 and y < 3:
                for x in range(self.init_cols):
                    invader = InvaderModel(160 + (x * 48) + 8, (y * 32) + offsety, 1)
                    self.invaders.append(invader)
            if y >= 3:
                for x in range(self.init_cols):
                    invader = InvaderModel(160 + (x * 48) + 8, (y * 32) + offsety, 2)
                    self.invaders.append(invader)

    def update(self, gameTime):
        self.bullets.update(gameTime)
        self.framecount -= gameTime
        movesideways = True

        if self.framecount < 0:
            if self.movedown:
                self.movedown = False
                movesideways = False
                self.sx *= -1
                self.bulletDropTime -= 250
                if self.bulletDropTime < 1000:
                    self.bulletDropTime = 1000
                self.currentframecount -= 100

                if self.currentframecount < 200:  # clamp speed of aliens to 200 ms
                    self.currentframecount = 200

                for i in self.invaders:
                    i.y += 32

            self.framecount = self.currentframecount + self.framecount
            for i in self.invaders:
                i.flipframe()

            if movesideways:
                for i in self.invaders:
                    i.x += self.sx

            x, y, width, height = self.getarea()
            ## check get area
            print("x=", x, "y=", y, "width=", width, "height=", height)

            if (x <= 0 and self.sx < 0) or (x + width >= 800 and self.sx > 0):
                self.movedown = True

        self.shootTimer -= gameTime
        if self.shootTimer <= 0:
            self.shootTimer += self.bulletDropTime  # reset the timer
            self.currentShooter += self.alienShooter

            self.currentShooter = self.currentShooter % len(self.invaders)

            shooter = self.invaders[self.currentShooter]

            x = shooter.x + 9  # bullet is 8 pixels
            y = shooter.y + 16

            self.bullets.addBullet(x, y)

    def getarea(self):
        leftmost = 2000
        rightmost = -2000
        topmost = -2000
        bottommost = 2000

        for i in self.invaders:
            if i.x < leftmost:
                leftmost = i.x

            if i.x > rightmost:
                rightmost = i.x

            if i.y < bottommost:
                bottommost = i.y

            if i.y > topmost:
                topmost = i.y

            width = (rightmost - leftmost) + 32
            height = (topmost - bottommost) + 32

            return (leftmost, bottommost, width, height)


class InvaderView:
    def __init__(self, swarm, imgpath):
        self.image = pygame.image.load(imgpath)
        self.swarm = swarm

    def render(self, surface):
        for i in self.swarm.invaders:
            surface.blit(
                self.image,
                (i.x, i.y, 32, 32),
                (i.animframe * 32, 32 * i.alientype, 32, 32),
            )
