import pygame
from os import path



def align_surface(surface, pos, align):
    """Return the rect aligned to the position"""
    rect = surface.get_rect()
    pos = (int(pos[0]), int(pos[1]))
    if align == "nw":
        rect.topleft = pos
    if align == "ne":
        rect.topright = pos
    if align == "sw":
        rect.bottomleft = pos
    if align == "se":
        rect.bottomright = pos
    if align == "n":
        rect.midtop = pos
    if align == "s":
        rect.midbottom = pos
    if align == "e":
        rect.midright = pos
    if align == "w":
        rect.midleft = pos
    if align == "center":
        rect.center = pos
    return rect

def align_rect(rect, pos, align):
    """Return the rect aligned to the position"""
    pos = (int(pos[0]), int(pos[1]))
    if align == "nw":
        rect.topleft = pos
    if align == "ne":
        rect.topright = pos
    if align == "sw":
        rect.bottomleft = pos
    if align == "se":
        rect.bottomright = pos
    if align == "n":
        rect.midtop = pos
    if align == "s":
        rect.midbottom = pos
    if align == "e":
        rect.midright = pos
    if align == "w":
        rect.midleft = pos
    if align == "center":
        rect.center = pos
    return rect

def compute_surface(rect, color=None, border_size=(0, 0), border_color=None, align="center", return_rect=False):
    """Return a surface and its rectangle filled with color and border_color"""

    # WIP: Check align bugs

    # Transparent surface
    surface = pygame.Surface([rect[2], rect[3]], pygame.SRCALPHA, 32)
    surface.convert_alpha()

    # Draw rect
    if color is not None:
        # Fill a surface with border_color
        if border_color is not None:
            surface.fill(border_color)

        # Fill the inside with color
        surface_in_rect = [border_size[0], border_size[1], rect[2] - 2 * border_size[0], rect[3] - 2 * border_size[1]]
        pygame.draw.rect(surface, color, surface_in_rect)

    # Draw border
    elif border_color is not None:
        pygame.draw.rect(surface, border_color, rect, border_size[0])

    # Return surface (& rect)
    if return_rect:
        surface_out_rect = align_surface(surface, (rect[0], rect[1]), align)
        return surface, surface_out_rect
    return surface



"""
    Class Initialization
"""
def init_class(self, game, dict, data, parent, key):
    """Initialization: game, main, dict, data"""
    self.game = game
    self.main = self.game.main
    self.dict = dict
    self.data = self.dict[data]
    self.parent = parent
    self.item = key
    self.settings = self.dict["settings"]

    """Load: item_dict
    Call each function in init_functions to load the dict for each item
    """
    self.item_dict = {}
    self.item_list = []
    if key is None:
        for item in self.data:
            dict = {}
            data = self.data[item]
            settings = self.settings[data["settings"]]
            for function in self.settings["init_functions"]:
                dict = function(self, dict, data, settings)
            self.item_dict[item] = dict
            self.item_list.append(item)
    else:
        pass



def load_interface(self, dict, data, settings):
    """Load the surface and surface_rect"""
    if "image" in data and data["image"] is not None:
        # Image
        dict["surface"] = self.game.graphic_dict[data["image"]]
    else:
        # Box
        rect = [data["position"][0], data["position"][1], settings["size"][0], settings["size"][1]]
        dict["surface"] = compute_surface(rect, settings["color"], settings["border_size"], settings["border_color"], settings["align"])
    dict["surface_rect"] = align_surface_rect(dict["surface"], (data["position"][0], data["position"][1]), settings["align"])
    return dict


def load_button(self, dict, data, settings):
    """Load the surface for each state and surface_rect"""
    if "image" in data and data["image"] is not None:
        # Image
        image_active, image_inactive = data["image"]
        dict["surface_active"] = self.game.graphic_dict[image_active]
        dict["surface_inactive"] = self.game.graphic_dict[image_inactive]
    else:
        # Box
        rect = [data["position"][0], data["position"][1], settings["size"][0], settings["size"][1]]
        dict["surface_active"] = compute_surface(rect, settings["color"][0], settings["border_size"], settings["border_color"], settings["align"])
        dict["surface_inactive"] = compute_surface(rect, settings["color"][1], settings["border_size"], settings["border_color"], settings["align"])
    dict["surface"] = dict["surface_inactive"]
    dict["surface_rect"] = align_surface_rect(dict["surface"], (data["position"][0], data["position"][1]), settings["align"])
    return dict


def load_text(self, dict, data, settings):
    """Load all text parameters"""
    if "text" in data:
        dict["text"] = dict["text_check"] = data["text"]
        dict["text_pos"] = self.game.compute_text_pos(dict["surface_rect"])
        dict["text_font"] = self.game.font_dict[settings["text_font"]]
        dict["text_color"] = settings["text_color"]
        dict["text_align"] = settings["text_align"]
        dict["text_surface"], dict["text_surface_rect"] = self.game.compute_text(dict["text"], dict["text_font"], dict["text_color"], dict["text_pos"], dict["text_align"])
    return dict

def load_sound(self, dict, data, settings):
    """Load all sound parameters"""
    dict["sound_action"] = settings["sound_action"]
    dict["sound_active"] = settings["sound_active"]
    dict["sound_inactive"] = settings["sound_inactive"]
    dict["sound_check"] = False
    return dict

def load_action(self, dict, data, settings):
    """Load all action parameters"""
    dict["argument"] = data["argument"] if "argument" in data else None
    dict["action"] = eval(data["action"]) if "action" in data and data["action"] is not None else None
    return dict



"""
    Class Draw
"""
def draw_surface(self, dict):
    self.game.gameDisplay.blit(dict["surface"], dict["surface_rect"])

def draw_text(self, dict):
    if "text" in dict:
        if dict["text"] != dict["text_check"]:
            dict["text_check"] = dict["text"]
            dict["text_surface"], dict["text_surface_rect"] = self.game.compute_text(dict["text"], dict["text_font"], dict["text_color"], dict["text_pos"], dict["text_align"])

        if dict["text"] is not None:
            self.game.gameDisplay.blit(dict["text_surface"], dict["text_surface_rect"])




















def load_image(image_path, image_dir, color_key=None, scale_size=None):
    if isinstance(image_dir, list):
        images = []
        for image in image_dir:
            image = pygame.image.load(path.join(image_path, image))
            if scale_size is not None:
                image = pygame.transform.scale(image, scale_size)
            images.append(convert_image(image, color_key))
        return images
    else:
        image = pygame.image.load(path.join(image_path, image_dir))
        if scale_size is not None:
            image = pygame.transform.scale(image, scale_size)
        return convert_image(image, color_key)

def convert_image(image, color_key):
    if color_key is not None:
        image = image.convert()
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image