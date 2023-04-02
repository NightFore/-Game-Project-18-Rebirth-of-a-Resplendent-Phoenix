import pygame
import random
from Button import *
from Class import *

class s0_title:
    def __init__(self, game):
        self.game, self.main = game, game.main
        self.buttons = Buttons(self.game, self.game.button_dict, "title", self)

    def get_keys(self):
        for event in self.game.event:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_z:
                    self.buttons.compute_button_index(-1)
                if event.key == pygame.K_s:
                    self.buttons.compute_button_index(1)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if self.buttons.current_button is not None:
                        self.buttons.current_button.compute_action()

    def update(self):
        self.get_keys()
        self.buttons.update()

    def draw(self):
        self.buttons.draw()

class s1_level:
    def __init__(self, game):
        self.game, self.main = game, game.main
        self.buttons = Buttons(self.game, self.game.button_dict, "level", self)

    def update(self):
        self.buttons.update()

    def draw(self):
        self.buttons.draw()
