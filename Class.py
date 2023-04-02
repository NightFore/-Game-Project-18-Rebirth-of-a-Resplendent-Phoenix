import pygame
import copy
import random
from Dict import *
from Graphic import *
from Button import *
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, game, key, group):
        self.game, self.main = game, game.main
        self.dict = unit_dict[key]
        pygame.sprite.Sprite.__init__(self, group)
        self.load()
        self.new()
        self.init_graphic_flip()

    def load(self):
        self.graphic = Graphic(self.game, self.dict["image"])
        self.rect = self.graphic.rect
        self.pos = vec(self.game.screen_width // 2, self.game.screen_height // 2)
        self.vel = vec(0, 0)

        self.level = 1
        self.experience = 0
        self.attack = {
            "energy_ball": {
                "effect": "sprite_energy_ball", "cooldown": 1, "last_attack": 0, "damage": 1
            },
        }
        self.cooldown_current = 0
        self.cooldown_loop = 0.10
        self.cooldown_special_current = 0
        self.cooldown_special_loop = 0.05
        self.health_max = 6
        self.health_current = self.health_max
        self.mana_max = 10
        self.mana_current = 0
        self.mana_rate = 0.5
        self.special_max = 25
        self.special_current = 0
        self.special_rate = 2

    def new(self):
        self.all_interfaces = pygame.sprite.Group()

        self.killed_mob = 0
        self.killed_enemy = 0
        self.killed_grave = 0
        self.total_time = 0
        self.current_level = 1

        # Time
        self.time_box = Interface_surf(self.game, self.all_interfaces)
        self.time_box.compute_all([0, 0, 1280, 25])
        self.total_time_box = Interface_surf(self.game, self.all_interfaces)
        self.total_time_box.compute_all([515, 25, 250, 50])
        self.level_box = Interface_surf(self.game, self.all_interfaces)
        self.level_box.compute_all([540, 75, 200, 50])

        # Player
        self.portrait_box = Interface_surf(self.game, self.all_interfaces)
        self.portrait_box.compute_all([0, 25, 100, 100])
        self.portrait = Interface(self.game, self.all_interfaces, "portrait_phoenix")
        self.portrait.graphic.compute_pos(1, 10)
        self.portrait.graphic.current_image = pygame.transform.flip(self.portrait.graphic.current_image, True, False)
        self.health_box = Interface_surf(self.game, self.all_interfaces)
        self.health_box.compute_all([100, 25, 218, 42])

        # Ally
        self.ally_box = Interface_surf(self.game, self.all_interfaces)
        self.ally_box.align = "center"
        self.ally_box.compute_all([1055, 50, 50, 50])
        self.ally_count_box = Interface_surf(self.game, self.all_interfaces)
        self.ally_count_box.align = "center"
        self.ally_count_box.compute_all([1180, 50, 200, 50])
        self.ally_portrait = Interface(self.game, self.all_interfaces, "portrait_ally")
        self.ally_portrait.graphic.align = "center"
        self.ally_portrait.graphic.compute_pos(1055, 50)

        # Enemy
        self.enemy_box = Interface_surf(self.game, self.all_interfaces)
        self.enemy_box.align = "center"
        self.enemy_box.compute_all([1055, 100, 50, 50])
        self.enemy_count_box = Interface_surf(self.game, self.all_interfaces)
        self.enemy_count_box.align = "center"
        self.enemy_count_box.compute_all([1180, 100, 200, 50])
        self.enemy_portrait = Interface(self.game, self.all_interfaces, "portrait_enemy")
        self.enemy_portrait.graphic.align = "center"
        self.enemy_portrait.graphic.compute_pos(1055, 100)

        # Grave
        self.grave_box = Interface_surf(self.game, self.all_interfaces)
        self.grave_box.align = "center"
        self.grave_box.compute_all([1055, 150, 50, 50])
        self.grave_count = Interface_surf(self.game, self.all_interfaces)
        self.grave_count.align = "center"
        self.grave_count.compute_all([1180, 150, 200, 50])
        self.grave_portrait = Interface(self.game, self.all_interfaces, "portrait_grave")
        self.grave_portrait.graphic.align = "center"
        self.grave_portrait.graphic.compute_pos(1055, 150)

        # Attack
        self.cooldown_box = Interface_surf(self.game, self.all_interfaces)
        self.cooldown_box.align = "center"
        self.cooldown_box.compute_all([265, 905, 50, 50])
        self.mana_box = Interface_surf(self.game, self.all_interfaces)
        self.mana_box.align = "center"
        self.mana_box.compute_all([440, 905, 300, 50])
        self.special_box = Interface_surf(self.game, self.all_interfaces)
        self.special_box.align = "center"
        self.special_box.compute_all([840, 905, 300, 50])

        # Heart
        self.all_hearts = pygame.sprite.Group()
        for index in range(self.health_current):
            heart = Interface(self.game, self.all_hearts, "heart")
            pos = interface_dict["heart"]["pos"]
            heart.graphic.compute_pos(pos[0] + 35*index, pos[1])


        # Text
        self.font = None
        self.color = WHITE
        self.font = self.game.font_dict["LiberationSerif_30"]

    def init_graphic_flip(self):
        images = []
        for image in self.graphic.images[0]:
            images.append(pygame.transform.flip(image, True, False))
        self.graphic.images.append(images)

    def compute_movement(self, dx, dy):
        self.pos += vec(dx*100, dy*100)

    def update_movement(self):
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

    def update(self):
        if self.pos != self.graphic.pos:
            self.graphic.compute_pos(self.pos[0], self.pos[1])
        self.graphic.update()
        for interface in self.all_interfaces:
            interface.update()
        self.cooldown_current = min(self.cooldown_current + self.game.dt, self.cooldown_loop)
        self.cooldown_special_current = min(self.cooldown_special_current + self.game.dt, self.cooldown_special_loop)
        self.rect = self.graphic.rect.copy()
        self.rect[2] = 60
        self.rect[3] = 60
        self.rect = align_rect(self.rect, (self.rect[0]+55, self.rect[1]+80), "center")

    def draw(self):
        self.graphic.draw()
        for interface in self.all_interfaces:
            interface.draw()

        index = 0
        for health in self.all_hearts:
            index += 1
            if index <= self.health_current:
                health.draw()

        # Time
        self.time_box.inside_width = self.time_box.rect[2] * self.main.class_level.cycle_time / self.main.class_level.loop_cycle_time
        text, text_rect = self.game.compute_text("Total Time: %i" % self.total_time, self.font, self.color, [640, 50], "center")
        self.game.gameDisplay.blit(text, text_rect)
        text, text_rect = self.game.compute_text("Level: %i" % self.current_level, self.font, self.color, [640, 100], "center")
        self.game.gameDisplay.blit(text, text_rect)

        # Killed
        text, text_rect = self.game.compute_text("%i" % self.killed_mob, self.font, self.color, [1180, 50], "center")
        self.game.gameDisplay.blit(text, text_rect)
        text, text_rect = self.game.compute_text("%i" % self.killed_enemy, self.font, self.color, [1180, 100], "center")
        self.game.gameDisplay.blit(text, text_rect)
        text, text_rect = self.game.compute_text("%i" % self.killed_grave, self.font, self.color, [1180, 150], "center")
        self.game.gameDisplay.blit(text, text_rect)

        # Cooldown
        cooldown = self.cooldown_loop - self.cooldown_current
        self.cooldown_box.inside_height = (cooldown * (self.cooldown_box.rect[3] - 2*self.cooldown_box.border_size)) / self.cooldown_loop
        text, text_rect = self.game.compute_text("CD", self.font, self.color, [265, 905], "center")
        self.game.gameDisplay.blit(text, text_rect)

        # Mana
        self.mana_box.inside_width = (self.mana_current * (self.mana_box.rect[2] - 2*self.mana_box.border_size)) / self.mana_max
        text, text_rect = self.game.compute_text("Mana: %i/%i" % (self.mana_current, self.mana_max), self.font, self.color, [440, 905], "center")
        self.game.gameDisplay.blit(text, text_rect)

        # Limit
        self.special_box.inside_width = (self.special_current * self.special_box.rect[2]) / self.special_max
        text, text_rect = self.game.compute_text("Special: %i/%i" % (self.special_current, self.special_max), self.font, self.color, [840, 905], "center")
        self.game.gameDisplay.blit(text, text_rect)

class Interface_surf(pygame.sprite.Sprite):
    def __init__(self, game, group):
        self.game, self.main = game, game.main
        pygame.sprite.Sprite.__init__(self, group)
        self.load()
        self.new()

    def load(self):
        self.color = DARKGREY
        self.border_color = LIGHTSKYGREY
        self.inside_color = LIGHTCYAN
        self.border_size = 2
        # self.font = self.font_liberation
        self.font_color = WHITE
        self.align = "nw"

        self.pos = vec(640, 660)
        self.rect = [self.pos[0], self.pos[1], 280, 40]
        self.size = [self.rect[2], self.rect[3]]
        self.surface = pygame.Surface(self.size)
        self.surface_rect = align_surface(self.surface, (self.rect[0], self.rect[1]), self.align)
        if self.border_color is not None:
            self.surface.fill(self.border_color)
        x, y = self.border_size, self.border_size
        width = self.rect[2] - self.border_size*2
        height = self.rect[3] - self.border_size*2
        pygame.draw.rect(self.surface, self.color, (x, y, width, height))

    def new(self):
        self.inside_width = 0
        self.inside_height = 0

    def compute_all(self, rect):
        self.rect = rect
        self.pos = rect[0], rect[1]
        self.size = rect[2], rect[3]
        self.surface = pygame.Surface(self.size)
        self.surface_rect = align_surface(self.surface, (self.rect[0], self.rect[1]), self.align)
        if self.border_color is not None:
            self.surface.fill(self.border_color)
        x, y = self.border_size, self.border_size
        width = self.rect[2] - self.border_size * 2
        height = self.rect[3] - self.border_size * 2
        pygame.draw.rect(self.surface, self.color, (x, y, width, height))

    def compute_pos(self, x, y):
        """
        Update the rect position given x and y value
        """
        if x is not None:
            self.pos[0] = x
        if y is not None:
            self.pos[1] = y
        pos_x = self.pos[0]
        pos_y = self.pos[1]
        self.surface_rect = align_surface(self.surface, (pos_x, pos_y), self.align)


    def update(self):
        pass

    def draw(self):
        self.game.gameDisplay.blit(self.surface, self.surface_rect)
        x, y = self.border_size, self.border_size
        width = self.rect[2] - self.border_size*2
        height = self.rect[3] - self.border_size*2
        pygame.draw.rect(self.surface, self.color, (x, y, width, height))

        if self.inside_width != 0:
            pygame.draw.rect(self.surface, self.inside_color, (x, y, self.inside_width, height))
        elif self.inside_height != 0:
            pygame.draw.rect(self.surface, self.inside_color, (x, y+height, width, -self.inside_height))




class Interface(pygame.sprite.Sprite):
    def __init__(self, game, group, key):
        self.game, self.main = game, game.main
        self.key = key
        pygame.sprite.Sprite.__init__(self, group)
        self.load()
        self.new()

    def load(self):
        self.graphic = Graphic(self.game, self.key)

    def new(self):
        pass

    def update(self):
        self.dt = self.game.dt
        self.graphic.update()

    def draw(self):
        self.graphic.draw()

class Boss(pygame.sprite.Sprite):
    def __init__(self, game, key, group):
        self.game, self.main = game, game.main
        self.data = unit_dict
        self.key = key
        self.dict = copy.deepcopy(self.data[self.key])
        pygame.sprite.Sprite.__init__(self, group)
        self.load()
        self.new()

    def load(self):
        self.graphic = Graphic(self.game, self.dict["image"])
        self.pos = vec(random.randint(160, 1120), random.randint(160, 800))
        self.graphic.compute_pos(self.pos[0], self.pos[1])
        self.rect = self.graphic.rect

    def new(self):
        self.dt = self.game.dt
        self.delay_attack = 2
        self.last_attack = 0
        self.health_current = 5

    def update(self):
        self.dt = self.game.dt
        self.pos = self.graphic.pos
        self.graphic.update()
        self.update_attack()

    def update_attack(self):
        self.last_attack += self.dt
        if self.last_attack >= self.delay_attack:
            self.last_attack -= self.delay_attack
            effect = Effect(self.game, "energy_ball", self.main.class_level.group_effect_enemy)
            effect.load()
            effect.target_test(self.main.current_player.pos, self.pos)


    def draw(self):
        self.graphic.draw()



class Level:
    def __init__(self, game):
        self.game, self.main = game, game.main
        self.data = level_dict
        self.load()
        self.new()

    def load(self):
        pass

    def new(self):
        self.night_screen = pygame.Surface(self.game.gameDisplay.get_size()).convert_alpha()

    def init(self, level):
        self.game.paused = False
        self.enemy_time = 0
        self.mob_time = 0
        self.spawn_time = 1
        self.total_time = 0
        self.current_level = 1
        self.cycle_time = 0
        self.loop_cycle_time = 10
        self.current_cycle = False

        self.all_sprites = pygame.sprite.Group()
        self.all_players = pygame.sprite.Group()
        self.all_mobs = pygame.sprite.Group()
        self.all_enemies = pygame.sprite.Group()
        self.all_enemies_collide = pygame.sprite.Group()
        self.all_effects = pygame.sprite.Group()
        self.all_effects_enemy = pygame.sprite.Group()
        self.all_graves = pygame.sprite.Group()
        self.all_interfaces = pygame.sprite.Group()
        self.all_bosses = pygame.sprite.Group()
        self.all_items = pygame.sprite.Group()
        self.group_player = self.all_sprites, self.all_players
        self.group_mob = self.all_sprites, self.all_mobs
        self.group_enemy = self.all_sprites, self.all_enemies
        self.group_effect = self.all_sprites, self.all_effects
        self.group_effect_enemy = self.all_sprites, self.all_effects_enemy
        self.group_grave = self.all_sprites, self.all_graves
        self.group_interface = self.all_sprites, self.all_interfaces
        self.group_enemy_collide = self.all_sprites, self.all_enemies_collide
        self.group_boss = self.all_sprites, self.all_bosses
        self.group_item = self.all_sprites, self.all_items
        self.player = self.main.current_player = Player(self.game, "player", self.group_player)

    def line_spawn(self):
        dir = random.randint(1, 4)
        increment = max(32, 192-(32*(self.current_level-1)))
        if dir == 1 or dir == 2:
            number_enemy = 960 // increment
        else:
            number_enemy = 1280 // increment
        offset_center_x = (1280 - (number_enemy-1)*increment) // 2
        offset_center_y = (960 - (number_enemy-1)*increment) // 2
        for index in range(number_enemy):
            enemy = Enemy(self.game, "ghost_blue", self.group_enemy_collide)
            offset_x = offset_center_x + index * increment
            offset_y = offset_center_y + index * increment
            if dir == 1:
                enemy.pos = [50, offset_y]
                enemy.target_destination([1440, offset_y])
            if dir == 2:
                enemy.pos = [1230, offset_y]
                enemy.target_destination([-160, offset_y])
            if dir == 3:
                enemy.pos = [offset_x, 30]
                enemy.target_destination([offset_x, 1010])
            if dir == 4:
                enemy.pos = [offset_x, 930]
                enemy.target_destination([offset_x, -30])
            enemy.random = False

    def get_keys(self):
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        # Movement
        PLAYER_SPEED = 300
        self.vel = vec(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -PLAYER_SPEED
            self.player.graphic.index_table = 0
            self.player.graphic.update_image()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = +PLAYER_SPEED
            self.player.graphic.index_table = 1
            self.player.graphic.update_image()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel.y = +PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071
        self.moving = (self.vel.x != 0 or self.vel.y != 0)
        self.main.current_player.pos += self.vel * self.game.dt

        if self.game.click[1]:
            if self.player.mana_current >= 1 and self.player.cooldown_current >= self.player.cooldown_loop:
                Effect(self.game, "energy_ball", self.group_effect)
                self.player.cooldown_current = 0
                self.player.mana_current -= 1

        if mouse[2]:
            if self.player.special_current >= 1 and self.player.cooldown_special_current >= self.player.cooldown_special_loop:
                Effect(self.game, "energy_ball", self.group_effect)
                self.player.cooldown_special_current = 0
                self.player.special_current -= 1


    def update_cycle(self):
        self.cycle_time = min(self.cycle_time + self.dt, self.loop_cycle_time)
        if self.cycle_time >= self.loop_cycle_time and len(self.all_mobs) == 0 or (self.current_cycle and len(self.all_enemies_collide) == 0):
            self.cycle_time -= self.loop_cycle_time
            self.current_cycle = not self.current_cycle

            if self.current_cycle:
                for enemy in self.all_enemies:
                    enemy.kill()
                    new_enemy = Enemy_chase(self.game, "ghost_red", self.group_enemy_collide)
                    new_enemy.pos = enemy.pos
                for grave in self.all_graves:
                    grave.kill()
                    new_enemy = Enemy_chase(self.game, "ghost_red", self.group_enemy_collide)
                    new_enemy.pos = grave.pos

                for level in range(self.current_level):
                    Boss(self.game, "sprite_vi1", self.group_boss)

            if not self.current_cycle:
                self.current_level += 1
                self.spawn_time = max(0.5, self.spawn_time - 0.1)
                self.player.mana_rate *= 1.1
                self.player.mana_max += 1
                self.player.special_max += 25
                self.line_spawn()

        if self.current_cycle:
            self.player.mana_current = min(self.player.mana_current + 5 * self.player.mana_rate * self.game.dt, self.player.mana_max)
        elif not self.current_cycle:
            self.player.special_current = min(self.player.special_current + 1 * self.dt, self.player.special_max)
            self.player.mana_current = min(self.player.mana_current + self.player.mana_rate * self.game.dt, self.player.mana_max)



    def update_sprite(self):
        for sprite in self.all_sprites:
            sprite.update()

        for effect in self.all_effects:
            enemy_collided = pygame.sprite.spritecollideany(effect, self.all_enemies)
            if enemy_collided:
                effect.kill()
                enemy_collided.health_current -= 1
                if enemy_collided.health_current <= 0:
                    self.player.mana_current = min(self.player.mana_current + 1, self.player.mana_max)
                    self.player.killed_enemy += 1
                    enemy_collided.kill()
            enemy_chase_collided = pygame.sprite.spritecollideany(effect, self.all_enemies_collide)
            if enemy_chase_collided:
                effect.kill()
                enemy_chase_collided.health_current -= 1
                if enemy_chase_collided.health_current <= 0:
                    self.player.mana_current = min(self.player.mana_current + 1, self.player.mana_max)
                    self.player.special_current = min(self.player.special_current + 1, self.player.special_max)
                    self.player.killed_enemy += 1
                    enemy_chase_collided.kill()
            boss_collided = pygame.sprite.spritecollideany(effect, self.all_bosses)
            if boss_collided:
                effect.kill()
                boss_collided.health_current -= 1
                if boss_collided.health_current <= 0:
                    self.player.mana_current = self.player.mana_max
                    item = Item(self.game, "heart", self.group_item)
                    item.graphic.compute_pos(boss_collided.pos[0], boss_collided.pos[1])
                    self.player.killed_enemy += 1
                    item.rect = item.graphic.rect
                    boss_collided.kill()
            mob_collided = pygame.sprite.spritecollideany(effect, self.all_mobs)
            if mob_collided:
                Grave(self.game, mob_collided, self.group_grave)
                self.player.special_current = max(0, self.player.special_current -2)
                self.player.killed_grave += 1
                effect.kill()

        for effect in self.all_effects_enemy:
            collided = pygame.sprite.collide_rect(effect, self.main.current_player)
            if collided:
                effect.kill()
                self.player.health_current -= 1
                if self.player.health_current <= 0:
                    self.game_over()

        for mob in self.all_mobs:
            if pygame.sprite.spritecollideany(mob, self.all_enemies):
                Grave(self.game, mob, self.group_grave)
                self.player.killed_grave += 1
            hit_rect = self.main.current_gate.graphic.rect.copy()
            hit_rect.width = hit_rect.width // 4
            hit_rect.height = hit_rect.height // 4
            hit_rect.x += hit_rect.width * 3/2
            hit_rect.y += hit_rect.height * 3/2
            if mob.rect.colliderect(hit_rect):
                self.player.special_current = min(self.player.special_current + 5, self.player.special_max)
                self.player.killed_mob += 1
                mob.kill()

        for enemy in self.all_enemies_collide:
            collided = pygame.sprite.collide_rect(enemy, self.main.current_player)
            if collided:
                enemy.kill()
                self.player.health_current -= 1
                if self.player.health_current <= 0:
                    self.game_over()

        for item in self.all_items:
            if pygame.sprite.collide_rect(item, self.main.current_player):
                self.player.health_current = min(self.player.health_current + 1, self.player.health_max)
                item.kill()

    def game_over(self):
        self.game.paused = True
        self.game.pause_text_surface, self.game.pause_text_rect = self.game.compute_text("Game Over", self.game.font, RED, (self.game.screen_width // 2, self.game.screen_height // 2), align="center")
        buttons = Buttons(self.game, self.game.button_dict, "new_game", self)
        self.game.pause_button = buttons.item_list[0]


    def update_level(self):
        self.enemy_time = min(self.enemy_time + self.dt, self.spawn_time)
        self.mob_time = min(self.mob_time + self.dt, 3/2*self.spawn_time)
        if not self.current_cycle:
            if self.enemy_time >= self.spawn_time:
                self.enemy_time -= self.spawn_time
                Enemy(self.game, "ghost_black", self.group_enemy)

            if self.mob_time >= 3/2*self.spawn_time:
                self.mob_time -= 3/2*self.spawn_time
                if self.cycle_time < self.loop_cycle_time:
                    type = random.choice(kaduki_sprite).replace(".png", "")
                    Mob(self.game, type, self.group_mob)

    def update(self):
        self.dt = self.game.dt
        self.total_time = self.player.total_time = self.total_time + self.dt
        self.player.current_level = self.current_level
        self.get_keys()
        self.update_sprite()
        self.update_cycle()
        self.update_level()

    def draw_cycle(self):
        if self.current_cycle:
            center = int(self.main.current_player.pos[0]), int(self.main.current_player.pos[1])
            self.night_screen.fill((30, 43, 88, 155))
            # pygame.draw.circle(self.night_screen, (0, 0, 0, 0), center, 240)
            self.game.gameDisplay.blit(self.night_screen, (0, 0))

    def draw_sprite(self):
        for sprite in self.all_sprites:
            sprite.draw()

    def draw(self):
        self.draw_sprite()
        self.draw_cycle()

class Map:
    def __init__(self, game):
        self.game, self.main = game, game.main
        self.data = level_dict
        self.load()
        
    def load(self):
        self.tile_size = self.main.tile_size
        self.tile_grass_1 = Graphic(self.game, "tile_grass_1")

    def init(self, level):
        self.dict = copy.deepcopy(self.data[level])
        self.init_map()
        self.init_settings()
        self.init_surface()

    def init_map(self):
        self.current_map = self.dict["map"]
        self.map_length = [len(self.current_map[0]), len(self.current_map)]
        offset_x = int(self.game.screen_width/2 - self.tile_size[0] * self.map_length[0]/2)
        offset_y = int(self.game.screen_height/2 - self.tile_size[1] * self.map_length[1]/2)
        self.offset = [offset_x, offset_y]

    def init_settings(self):
        self.tile_grass_1.offset = self.offset

    def init_surface(self):
        self.current_surface = pygame.Surface((self.game.screen_width, self.game.screen_height))
        for index_y, tile_line in enumerate(self.current_map):
            for index_x, tile in enumerate(tile_line):
                if tile == 0:
                    self.tile_grass_1.compute_pos_scaled(index_x, index_y)
                    self.tile_grass_1.draw_surface(self.current_surface)

    def compute_path(self, x, y):
        """
        Returns the first possible path to [x, y]
        """
        for new_path in self.current_map:
            if [x, y] == new_path[-1]:
                return new_path

    @staticmethod
    def compute_map_pos(map_path):
        """
        Returns all possible positions in the paths
        """
        map_pos = []
        for new_path in map_path:
            for pos in new_path:
                if pos not in map_pos:
                    map_pos.append(pos)
        return map_pos

    def compute_map_path(self, distance, pos, d_range=1):
        """
        Returns all possible paths to a given distance
        """
        path_new = []
        path_current = path_final = [pos.copy()]
        while distance > 0:
            # Iterate for each path
            for path in path_current:
                x, y = path[-1]

                # Continue the path
                for dx in range(-d_range, d_range + 1):
                    for dy in range(-d_range, d_range + 1):
                        # Check: Maximum range
                        if (dx, dy) != (0, 0) and abs(dx) + abs(dy) <= d_range:
                            pos = [pos_x, pos_y] = [x + dx, y + dy]

                            # Check: Map limit
                            if 0 <= pos_x < len(self.current_map[0]) and 0 <= pos_y < len(self.current_map):
                                new_path = path.copy()

                                # Check: Path
                                if pos not in new_path and self.current_map[pos_y][pos_x] != 1:
                                    new_path.append(pos)
                                    path_new.append(new_path)

            # Add the current path to the final path list
            for path in path_new:
                path_final.append(path)

            # Initialize next loop
            path_current = path_new
            path_new = []
            distance -= 1

        return path_final

    def update(self):
        pass
        # self.tile_grass_1.update()

    def draw(self):
        self.game.gameDisplay.blit(self.current_surface, (0, 0))

class Units:
    def __init__(self, game):
        self.game, self.main = game, game.main
        self.data = level_dict

    def init(self, level):
        self.dict = copy.deepcopy(self.data[level])

        # Unit
        self.all_units = pygame.sprite.Group()
        self.units_dict = self.dict["units"]
        for unit in self.units_dict:
            new_unit = Unit(self.game, unit["type"], self.all_units)
            if unit["type"] == "player":
                self.main.current_player = new_unit
            if unit["type"] == "gate":
                self.main.current_gate = new_unit

    def update(self):
        for unit in self.all_units:
            unit.update()

    def draw(self):
        for unit in self.all_units:
            unit.draw()

class Unit(pygame.sprite.Sprite):
    def __init__(self, game, key, group):
        self.game, self.main = game, game.main
        self.data = unit_dict
        self.key = key
        self.dict = copy.deepcopy(self.data[self.key])
        pygame.sprite.Sprite.__init__(self, group)
        self.load()
        self.new()

    def load(self):
        self.graphic = Graphic(self.game, self.dict["image"])
        self.pos = vec(self.dict["pos"])
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect = self.graphic.rect

    def new(self):
        pass

    def update(self):
        if self.pos != self.graphic.pos:
            self.graphic.compute_pos(self.pos[0], self.pos[1])
            self.rect = self.graphic.rect
        self.graphic.update()

        self.update_movement()

    def compute_movement(self, dx, dy):
        self.pos += vec(dx*100, dy*100)

    def update_movement(self):
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

    def draw(self):
        self.graphic.draw()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, key, group):
        self.game, self.main = game, game.main
        self.data = unit_dict
        self.key = key
        self.dict = copy.deepcopy(self.data[self.key])
        pygame.sprite.Sprite.__init__(self, group)
        self.load()
        self.new()
        self.random_destination()

    def load(self):
        self.graphic = Graphic(self.game, self.dict["image"])
        self.pos = vec(random.randint(160, 1120), random.randint(160, 800))
        self.graphic.compute_pos(self.pos[0], self.pos[1])
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect = self.graphic.rect

    def new(self):
        self.dt = self.game.dt
        self.delay_random = 0
        self.loop_delay_random = 0.5
        self.speed = 50
        if "health" in self.dict:
            self.health_current = self.dict["health"]
        else:
            self.health_current = 1

        self.random = True

    def update(self):
        self.dt = self.game.dt
        if self.pos != self.graphic.pos:
            self.graphic.compute_pos(self.pos[0], self.pos[1])
            self.rect = self.graphic.rect
        self.graphic.update()

        self.random_destination()
        self.update_movement()

    def target_destination(self, target):
        target_dist = vec(target) - self.pos
        self.rot = target_dist.angle_to(vec(1, 0))
        self.vel = vec(1, 0).rotate(-self.rot) * self.speed

    def random_destination(self):
        if self.random:
            self.delay_random += self.dt
            if self.delay_random >= self.loop_delay_random:
                self.delay_random -= self.loop_delay_random
                random_x = self.pos[0] + random.randint(-160, 160)
                random_y = self.pos[1] + random.randint(-160, 160)
                target_dist = vec(random_x, random_y) - self.pos
                self.rot = target_dist.angle_to(vec(1, 0))
                self.vel = vec(1, 0).rotate(-self.rot) * self.speed

    def update_movement(self):
        self.pos += self.vel * self.game.dt

    def draw(self):
        self.graphic.draw()

class Enemy_chase(pygame.sprite.Sprite):
    def __init__(self, game, key, group):
        self.game, self.main = game, game.main
        self.data = unit_dict
        self.key = key
        self.dict = copy.deepcopy(self.data[self.key])
        pygame.sprite.Sprite.__init__(self, group)
        self.load()
        self.new()

    def load(self):
        self.graphic = Graphic(self.game, self.dict["image"])
        self.pos = vec(random.randint(160, 1120), random.randint(160, 800))
        self.graphic.compute_pos(self.pos[0], self.pos[1])
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect = self.graphic.rect

    def new(self):
        self.dt = self.game.dt
        self.delay_random = 0
        self.loop_delay_random = 2
        self.speed = 100
        self.health_current = 2

        self.random = True

    def update(self):
        self.dt = self.game.dt
        if self.pos != self.graphic.pos:
            self.graphic.compute_pos(self.pos[0], self.pos[1])
            self.rect = self.graphic.rect
        self.graphic.update()

        self.chase()
        self.update_movement()

    def chase(self):
        target_dist = vec(self.main.current_player.pos) - self.pos
        self.rot = target_dist.angle_to(vec(1, 0))
        self.vel = vec(1, 0).rotate(-self.rot) * self.speed

    def update_movement(self):
        self.pos += self.vel * self.game.dt

    def draw(self):
        self.graphic.draw()


class Mob(pygame.sprite.Sprite):
    def __init__(self, game, key, group):
        self.game, self.main = game, game.main
        self.data = unit_dict
        self.key = key
        self.dict = copy.deepcopy(self.data[self.key])
        pygame.sprite.Sprite.__init__(self, group)
        self.load()
        self.new()

    def load(self):
        self.graphic = Graphic(self.game, self.dict["image"])
        self.rect = self.graphic.rect

    def new(self):
        random_up = [random.randint(-160, 1440), random.randint(-320, -160)]
        random_left = [random.randint(-320, -160), random.randint(-160, 1080)]
        random_right = [random.randint(1440, 1600), random.randint(-160, 1080)]
        random_down = [random.randint(-160, 1440), random.randint(1080, 1240)]
        random_direction = [random_up, random_left, random_right, random_down]
        self.pos = random.choice(random_direction)
        self.graphic.compute_pos(self.pos[0], self.pos[1])

        self.speed = 100
        target_dist = vec(640, 480) - self.pos
        self.rot = target_dist.angle_to(vec(1, 0))
        self.pos = vec(self.pos)
        self.vel = vec(1, 0).rotate(-self.rot) * self.speed

        if -45 <= self.rot <= 45:
            self.graphic.index_table = 2
        if 45 <= self.rot <= 135:
            self.graphic.index_table = 3
        if 135 <= self.rot <= 180 or -180 <= self.rot <= -135:
            self.graphic.index_table = 1
        if -135 <= self.rot <= -45:
            self.graphic.index_table = 0

        self.graphic.compute_pos(self.pos[0], self.pos[1])

    def update_movement(self):
        self.pos += self.vel * self.game.dt

    def update(self):
        if self.pos != self.graphic.pos:
            self.graphic.compute_pos(self.pos[0], self.pos[1])
            self.rect = self.graphic.rect
        self.graphic.update()

        self.update_movement()

    def draw(self):
        self.graphic.draw()



class Grave(pygame.sprite.Sprite):
    def __init__(self, game, parent, group):
        self.game, self.main = game, game.main
        self.parent = parent
        pygame.sprite.Sprite.__init__(self, group)
        self.load()
        self.new()

    def load(self):
        self.graphic = Graphic(self.game, "sprite_grave")
        self.rect = self.graphic.rect
        self.pos = self.parent.pos
        self.graphic.compute_pos(self.pos[0], self.pos[1])
        self.parent.kill()

    def new(self):
        pass

    def update(self):
        self.graphic.update()

    def draw(self):
        self.graphic.draw()


class Effect(pygame.sprite.Sprite):
    def __init__(self, game, key, group):
        self.game, self.main = game, game.main
        self.data = effect_dict
        self.key = key
        self.dict = copy.deepcopy(self.data[self.key])
        pygame.sprite.Sprite.__init__(self, group)
        self.load()
        self.new()

    def load(self):
        self.graphic = Graphic(self.game, self.dict["image"])
        self.rect = self.graphic.rect
        self.speed = self.dict["speed"]

    def new(self):
        target_dist = self.game.mouse - self.main.current_player.pos
        self.rot = target_dist.angle_to(vec(1, 0))
        self.pos = vec(self.main.current_player.pos)
        self.vel = vec(1, 0).rotate(-self.rot) * self.speed
        self.graphic.compute_rot(self.rot)
        self.graphic.compute_pos(self.pos[0], self.pos[1])
        self.rect = self.graphic.rect.copy()

    def target_test(self, target_1, target_2):
        target_dist = target_1 - target_2
        self.rot = target_dist.angle_to(vec(1, 0))
        self.pos = vec(target_2)
        self.vel = vec(1, 0).rotate(-self.rot) * self.speed
        self.graphic.compute_rot(self.rot)
        self.graphic.compute_pos(self.pos[0], self.pos[1])
        self.rect = self.graphic.rect.copy()

    def update_movement(self):
        self.pos += self.vel * self.game.dt

    def update(self):
        if self.pos != self.graphic.pos:
            self.graphic.compute_pos(self.pos[0], self.pos[1])
            self.rect = self.graphic.rect.copy()
            self.rect[0] = self.rect[0] + self.rect[2]/6
            self.rect[1] = self.rect[1] + self.rect[3]/6
            self.rect[2] = self.rect[2] - self.rect[2]/3
            self.rect[3] = self.rect[3] - self.rect[3]/3
        self.graphic.update()
        self.update_movement()

    def draw(self):
        self.graphic.draw()


class Item(pygame.sprite.Sprite):
    def __init__(self, game, key, group):
        self.game, self.main = game, game.main
        self.data = item_dict
        self.key = key
        self.dict = copy.deepcopy(self.data[self.key])
        pygame.sprite.Sprite.__init__(self, group)
        self.load()
        self.new()

    def load(self):
        self.graphic = Graphic(self.game, self.dict["image"])
        self.rect = self.graphic.rect

    def new(self):
        pass

    def update(self):
        self.graphic.update()

    def draw(self):
        self.graphic.draw()
