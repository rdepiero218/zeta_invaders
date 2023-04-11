import pygame, os, sys
from pygame.locals import *
from bitmapfont import *
from raspigame import *


class MainMenuState(GameState):
    def __init__(self, game):
        super(MainMenuState, self).__init__(game)
        self.playGameState = None
        self.font = BitmapFont("images/placeholder_font.png", 12, 12)
        self.index = 0
        self.inputTick = 0
        self.menuItems = ["Start Game", "Quit"]

    def setPlayState(self, state):
        self.playGameState = state

    def update(self, gameTime):
        keys = pygame.key.get_pressed()
        if (keys[K_UP] or keys[K_DOWN]) and self.inputTick == 0:
            self.inputtick = 250

            if keys[K_UP]:
                self.index -= 1
                if self.index < 0:
                    self.index = len(self.menuItems) - 1
            if keys[K_DOWN]:
                self.index += 1
                if self.index == len(self.menuItems):
                    self.index = 0
        elif self.inputTick > 0:
            self.inputTick -= gameTime
        if self.inputTick < 0:
            self.inputTick = 0

        if keys[K_SPACE]:
            if self.index == 1:
                self.game.changeState(None)  # EXIT THE GAME
            elif self.index == 0:
                self.game.changeState(self.playGameState)

    def draw(self, surface):
        self.font.center(surface, "ZETA INVADERS", 48)

        count = 0
        y = surface.get_rect().height - len(self.menuItems) * 50

        for item in self.menuItems:
            itemText = "   "

            if count == self.index:
                itemText = "> "

            itemText += item
            self.font.draw(surface, itemText, 300, y)
            y += 24
            count += 1
