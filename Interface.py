import pygame
from Function import *
from Settings import *

class Interface:
    def __init__(self, game, dict, data, parent=None, key=None):
        init_class(self, game, dict, data, parent, key)

    def update(self):
        pass

    def draw(self):
        for item in self.item_dict:
            dict = self.item_dict[item]
            draw_surface(self, dict)
            draw_text(self, dict)

