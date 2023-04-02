from Head import *

class Main:
    def __init__(self, game):
        self.game = game
        self.main = game.main = self
        self.dict = copy.deepcopy(main_dict)

    def load(self):
        self.load_dict()
        self.load_class()
        self.load_kaduki_sprite()

    def load_dict(self):
        self.tile_size = self.dict["tile_size"]
        self.player_speed = self.dict["player_speed"]

    def load_class(self):
        self.class_cursor = Cursor(self.game, "default")
        self.class_level = Level(self.game)
        self.class_map = Map(self.game)
        self.class_units = Units(self.game)

    def load_kaduki_sprite(self):
        self.kaduki_dict = kaduki_dict
        for graphic in kaduki_sprite:
            key = graphic.replace(".png", "")
            dict = self.game.graphic_dict[key] = self.kaduki_dict["default"].copy()
            dict["path"] = path.join(self.game.graphic_folder, graphic)
            dict["image"], dict["images"], dict["rect"] = load_graphic(dict)
            unit_dict[key] = {"image": key, "pos": [0, 0]}

    def new(self):
        pass

    # -------------------- #
    def init_title(self):
        self.current_menu = "title"
        self.class_state = s0_title(self.game)
        self.class_map.init("chapter_prologue")

        self.game.setting_music("battle_2")

    def init_level(self, new_game=False):
        if new_game:
            self.new_music()

        self.game.pause_text_surface, self.game.pause_text_rect = self.game.compute_text("Game Paused", self.game.font, RED, (self.game.screen_width // 2, self.game.screen_height // 2), align="center")
        self.current_menu = "level"
        self.class_state = s1_level(self.game)
        self.class_map.init("chapter_prologue")
        self.class_units.init("chapter_prologue")
        self.class_level.init("chapter_prologue")

    def new_music(self):
        music = None
        music_path = self.game.music
        while music_path == self.game.music:
            music = random.choice(["battle_1", "battle_2", "battle_3"])
            music_path = self.game.music_dict[music]
            print(music)
        self.game.setting_music(music)

    # -------------------- #
    def update(self):
        if self.current_menu == "title":
            self.class_map.update()
            self.class_state.update()
        elif self.current_menu == "level":
            self.class_map.update()
            self.class_units.update()
            self.class_state.update()
            self.class_level.update()

    def draw(self):
        if self.current_menu == "title":
            self.class_map.draw()
            self.class_state.draw()
        elif self.current_menu == "level":
            self.class_map.draw()
            self.class_units.draw()
            self.class_state.draw()
            self.class_level.draw()
