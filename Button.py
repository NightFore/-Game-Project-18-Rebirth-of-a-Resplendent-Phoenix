import pygame
from Function import *
from Settings import *
import copy

class Buttons:
    def __init__(self, game, data, key, parent=None):
        # Initialization
        self.game, self.main = game, game.main
        self.data, self.key, self.parent = data, key, parent
        self.dict = copy.deepcopy(self.data[self.key])
        self.settings = self.data["settings"]

        # Load items
        self.item_list = []
        for item in self.dict:
            item_data = self.dict
            item_key = item
            self.item_list.append(Button(self.game, item_data, item_key, self.settings, self.parent))

        # Pause Button
        for item in self.dict:
            if item == "pause":
                self.pause_button = item

        # Key navigation
        self.button_index = 0
        self.current_button = self.item_list[self.button_index]

    def compute_button_index(self, d_index=0):
        self.button_index = (self.button_index + d_index + len(self.item_list)) % len(self.item_list)
        self.current_button = self.item_list[self.button_index]
        return self.current_button

    def update(self):
        for item in self.item_list:
            item.update()

        # Selected button
        self.current_button.surface = self.current_button.surface_active

    def draw(self):
        for item in self.item_list:
            item.draw()


class Button:
    def __init__(self, game, data, key, settings, parent=None):
        """Initialization"""
        self.game, self.main = game, game.main
        self.data, self.key, self.parent = data, key, parent
        self.dict = copy.deepcopy(self.data[self.key])

        """Load"""
        self.settings = settings[self.dict["settings"]]
        self.load_button()
        self.load_text()
        self.load_sound()
        self.load_action()

    def load_button(self):
        """Load all button parameters"""
        # Rect
        pos = self.dict["position"]
        size = self.settings["size"]
        rect = pygame.Rect(pos[0], pos[1], size[0], size[1])

        # Surface
        color = self.settings["color"]
        border_size = self.settings["border_size"]
        border_color = self.settings["border_color"]
        align = self.settings["align"]
        self.surface_active = compute_surface(rect, color[0], border_size, border_color, align)
        self.surface_inactive = compute_surface(rect, color[1], border_size, border_color, align)
        self.surface = self.surface_inactive

        # Align
        self.surface_rect = align_surface(self.surface, pos, align)

        # State: active / inactive
        self.state = False

    def load_text(self):
        """Load all text parameters"""
        if "text" in self.dict:
            self.text_pos = self.game.compute_text_pos(self.surface_rect)
            self.text_font = self.game.font_dict[self.settings["text_font"]]
            self.text_color = self.settings["text_color"]
            self.text_align = self.settings["text_align"]
            self.text = self.text_check = self.dict["text"]
            self.text_surface, self.text_surface_rect = self.game.compute_text(self.text, self.text_font, self.text_color, self.text_pos, self.text_align)
        else:
            self.text = self.text_check = None

    def load_sound(self):
        """Load all sound parameters"""
        self.sound_action = self.settings["sound_action"]
        self.sound_active = self.settings["sound_active"]
        self.sound_inactive = self.settings["sound_inactive"]
        self.sound_check = False

    def load_action(self):
        """Load all action parameters"""
        if "argument" in self.dict:
            self.argument = self.dict["argument"]
        else:
            self.argument = None

        if "action" in self.dict and self.dict["action"] is not None:
            self.action = eval(self.dict["action"])
        else:
            self.action = None

    def compute_active(self, active):
        # Active
        if active:
            self.surface = self.surface_active
            self.sound_check = self.game.play_sound(self.sound_active, self.sound_check)

        # Inactive
        else:
            self.surface = self.surface_inactive
            self.sound_check = self.game.play_sound(self.sound_inactive, self.sound_check)

    def compute_action(self):
        self.game.play_sound(self.sound_action)
        if self.action is not None:
            if self.argument is not None:
                self.action(self.argument)
            else:
                self.action()

    def update_mouse(self):
        if self.surface_rect.collidepoint(self.game.mouse):
            if self.game.click[1]:
                self.compute_action()
            self.compute_active(True)
        else:
            self.compute_active(False)

    def update_text(self):
        if self.text != self.text_check:
            self.text_check = self.text
            self.text_surface, self.text_surface_rect = self.game.compute_text(self.text, self.text_font, self.text_color, self.text_pos, self.text_align)

    def draw_button(self):
        self.game.gameDisplay.blit(self.surface, self.surface_rect)

    def draw_text(self):
        if self.text is not None:
            self.game.gameDisplay.blit(self.text_surface, self.text_surface_rect)

    def update(self):
        self.update_mouse()
        self.update_text()

    def draw(self):
        self.draw_button()
        self.draw_text()
