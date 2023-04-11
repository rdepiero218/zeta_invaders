import pygame, os, sys
from pygame.locals import *


class GameState(object):
    def __init__(self, game):
        self.game = game

    def onEnter(self, previousState):
        pass

    def onExit(self):
        pass

    def update(self, gameTime):
        pass

    def draw(self, surface):
        pass


class RaspberryPiGame(object):
    # INITIALIZE CLASS
    def __init__(self, gameName, width, height):
        pygame.init()
        pygame.display.set_caption(gameName)

        self.fpsClock = pygame.time.Clock()
        self.mainwindow = pygame.display.set_mode((width, height))
        self.background = pygame.Color(0, 0, 0)
        self.currentState = None

    # CHANGE CURRENT STATE If newState is 'None' game terminates
    def changeState(self, newState):
        if self.currentState != None:
            self.currentState.onExit()

        if newState == None:
            pygame.quit()
            sys.exit()

        oldState = self.currentState
        self.currentState = newState
        newState.onEnter(oldState)

    # Run the game
    def run(self, initialState):
        self.changeState(initialState)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            gameTime = self.fpsClock.get_time()

            if self.currentState != None:
                self.currentState.update(gameTime)

            self.mainwindow.fill(self.background)
            if self.currentState != None:
                self.currentState.draw(self.mainwindow)

            pygame.display.update()
            self.fpsClock.tick(30)
