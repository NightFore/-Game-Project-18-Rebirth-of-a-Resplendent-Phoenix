import pygame
import copy
from Dict import *
from Function import *

class Graphic:
    def __init__(self, game, key):
        self.game, self.main = game, game.main
        self.dict = graphic_dict[key]
        self.load()
        self.new()

    def load(self):
        # Image
        self.image = self.dict["image"].copy()
        self.images = []
        for image in self.dict["images"]:
            self.images.append(image.copy())
        self.rect = self.dict["rect"]
        self.align = self.dict["align"]
        self.size_scaled = self.dict["size_scaled"]

        # Animation
        self.animation = self.dict["animation"]
        if self.animation:
            self.loop = self.dict["loop"]
            self.loop_reverse = self.dict["loop_reverse"]
            self.loop_delay = self.dict["loop_delay"]
            self.frame_speed = self.dict["frame_speed"]

    def new(self):
        # Position
        self.pos = [0, 0]
        self.offset = [0, 0]

        # Image
        self.current_image = self.image
        if self.images:
            self.index_image = 0
            self.index_table = 0
            self.length_table = len(self.images[self.index_table])
            self.update_image()

        # Animation
        if self.animation:
            # Time
            self.current_time = 0
            self.delay_time = 0

            # Animation
            self.animation_time = self.frame_speed / self.game.FPS
            self.loop_delay_time = self.loop_delay / self.game.FPS

            # Index (Next frame)
            self.index_next = 1

    def compute_pos(self, x=None, y=None, offset=None):
        """
        Update the rect position given x and y value
        """
        if x is not None:
            self.pos[0] = x
        if y is not None:
            self.pos[1] = y
        if offset is not None:
            self.offset = offset
        pos_x = self.pos[0] + self.offset[0]
        pos_y = self.pos[1] + self.offset[1]
        self.rect = align_surface(self.current_image, (pos_x, pos_y), self.align)

    def compute_pos_scaled(self, x=None, y=None, offset=None):
        """
        Update the rect position given x and y value multiplied by the image size
        """
        if x is not None:
            self.pos[0] = x
        if y is not None:
            self.pos[1] = y
        if offset is not None:
            self.offset = offset
        pos_x = self.pos[0] * self.size_scaled[0] + self.offset[0]
        pos_y = self.pos[1] * self.size_scaled[1] + self.offset[1]
        self.rect = align_surface(self.current_image, (pos_x, pos_y), self.align)

    def compute_rot(self, rot=0):
        for index in range(len(self.images[0])):
            self.images[0][index] = pygame.transform.rotate(self.images[0][index], rot)
        self.update_image()

    def next_image(self):
        # Index
        self.index_image += self.index_next

        # Loop
        if not self.loop_reverse and self.index_image == self.length_table:
            self.index_image %= self.length_table
            self.delay_time = self.loop_delay_time
        elif self.loop_reverse and self.index_image in (0, self.length_table - 1):
            self.index_next = -self.index_next
            self.delay_time = self.loop_delay_time

        self.update_image()

    def update_image(self):
        self.current_image = self.images[self.index_table][self.index_image]

    def update_animation(self):
        if self.animation:
            # Time dependent
            self.update_time()

    def update_time(self):
        # Loop delay
        if self.delay_time >= 0:
            self.delay_time -= self.dt

        # Frame animation
        else:
            self.current_time += self.dt
            if self.current_time >= self.animation_time:
                self.current_time -= self.animation_time
                self.next_image()

    def update(self):
        self.dt = self.game.dt
        self.update_animation()

    def draw(self):
        self.game.gameDisplay.blit(self.current_image, self.rect)

    def draw_surface(self, surface):
        surface.blit(self.current_image, self.rect)

def load_graphic(dict):
    path = dict["path"]
    size_scaled = dict["size_scaled"]
    color_key = dict["color_key"]
    align = dict["align"]
    image = pygame.image.load(path)

    # Images
    if dict["image_tables"]:
        images = load_images(dict, image, size_scaled, color_key)
    else:
        images = []

    # Image
    image = load_image(image, size_scaled, color_key)
    rect = align_surface(image, [0, 0], align)

    return image, images, rect

def load_image(image, size_scaled, color_key):
    # Convert / Scale / Color key
    image = pygame.Surface.convert_alpha(image)
    image = pygame.transform.scale(image, size_scaled)
    image.set_colorkey(color_key)
    return image

def load_images(dict, image, size_scaled, color_key):
    """
    image_tables = [image_table, image_table, image_table]
        image_table = [index_offset_x, index_offset_y, length_x, length_y] = length number of images
    image_size = [width, height]
    image_offset = [offset_x, offset_y]
    """
    image_tables = dict["image_tables"]
    image_size = dict["image_size"]
    image_offset = dict["image_offset"]

    images = []
    for index_table, table in enumerate(image_tables):
        # Offset
        table_offset_x = table[0] * image_size[0]
        table_offset_y = table[1] * image_size[1]
        image_table = []
        for index_y in range(table[3]):
            for index_x in range(table[2]):
                # Subsurface
                pos_sub_x = index_x * image_size[0] + (image_offset[0] + table_offset_x)
                pos_sub_y = index_y * image_size[1] + (image_offset[1] + table_offset_y)
                rect_sub = (pos_sub_x, pos_sub_y, image_size[0], image_size[1])

                # Process
                image_sub = image.subsurface(rect_sub)
                image_sub = load_image(image_sub, size_scaled, color_key)
                image_table.append(image_sub)
        images.append(image_table)
    return images
