from Main import *

class Game:
    # Initialization ----------------------- #
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.init()
        random.seed()
        self.game = self
        self.main = Main(self.game)
        self.load()
        self.new()
        self.main.init_title()
        self.playing = True

    # Load ----------------------- #
    def load(self):
        self.load_dict()
        self.load_folder()
        self.load_settings()
        self.load_resources()
        self.main.load()

    def load_dict(self):
        # Game
        self.game_dict = game_dict
        self.button_dict = button_dict

        # Resources
        self.font_dict = font_dict
        self.graphic_dict = graphic_dict
        self.music_dict = music_dict
        self.sound_dict = sound_dict

    def load_folder(self):
        # Directories
        self.game_folder = path.dirname(__file__)
        self.data_folder = path.join(self.game_folder, "data")
        self.font_folder = path.join(self.data_folder, "font")
        self.graphic_folder = path.join(self.data_folder, "graphic")
        self.music_folder = path.join(self.data_folder, "music")
        self.sound_folder = path.join(self.data_folder, "sound")

    def load_settings(self):
        # Game
        self.project_title = self.game_dict["project_title"]
        self.screen_size = self.screen_width, self.screen_height = self.game_dict["screen_size"]
        self.FPS = self.game_dict["FPS"]
        self.gameDisplay = self.main.gameDisplay = ScaledGame(self.project_title, self.screen_size, self.FPS)

        # Volume
        self.default_music_volume = self.music_volume = self.game_dict["default_music_volume"]
        self.default_sound_volume = self.sound_volume = self.game_dict["default_sound_volume"]
        pygame.mixer.music.set_volume(self.default_music_volume/100)

        # Key
        self.key_delay, self.key_interval = self.game_dict["key_repeat"]
        pygame.key.set_repeat(self.key_delay, self.key_interval)

    def load_resources(self):
        # Font
        for font in self.font_dict:
            font_ttf, font_size = self.font_dict[font]["ttf"], self.font_dict[font]["size"]
            if font_ttf is not None:
                font_ttf = path.join(self.font_folder, font_ttf)
            self.font_dict[font] = pygame.font.Font(font_ttf, font_size)

        # Graphic
        for graphic in self.graphic_dict:
            dict = self.graphic_dict[graphic]
            dict["path"] = path.join(self.graphic_folder, self.graphic_dict[graphic]["path"])
            dict["image"], dict["images"], dict["rect"] = load_graphic(dict)

        # Music
        for music in self.music_dict:
            if self.music_dict[music] is not None:
                self.music_dict[music] = path.join(self.music_folder, self.music_dict[music])

        # Sound
        for sound in self.sound_dict:
            self.sound_dict[sound] = pygame.mixer.Sound(path.join(self.sound_folder, self.sound_dict[sound]))
            self.sound_dict[sound].set_volume(self.sound_volume / 100)

    # New ----------------------- #
    def new(self):
        self.new_resources()
        self.new_camera()
        self.new_pause()
        self.new_debug()
        self.main.new()

    def new_resources(self):
        # Font
        self.font = self.font_dict["default"]

        # Graphic
        self.background_image = None
        self.background_color = None

        # Music
        self.music = None

    def new_camera(self):
        camera_border_rect_test = [-320, 320, -180, 180]
        self.camera = Camera(self.screen_size)
        self.camera.list_add(Player_camera(self, (self.screen_width/2, self.screen_height/2), camera_border_rect_test))
        self.camera.list_add(Player_camera(self, (0, 0), camera_border_rect_test))
        self.camera.initialize()

    def new_pause(self):
        # Pause game
        self.paused = False
        self.paused_check = False

        # Pause button
        self.pause_button = None

        # Pause screen
        self.pause_text_surface, self.pause_text_rect = self.compute_text("Game Paused", self.font, RED, (self.screen_width // 2, self.screen_height // 2), align="center")
        self.dim_screen = pygame.Surface(self.gameDisplay.get_size()).convert_alpha()
        self.dim_screen.fill((100, 100, 100, 120))

    def new_debug(self):
        self.debug_mode = True
        self.debug_check = False
        self.debug_color = CYAN

    # Game Loop ----------------------- #
    def run(self):
        while self.playing:
            self.dt = self.main.dt = self.gameDisplay.clock.tick(self.FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            # Continue to update and draw pause button
            elif self.pause_button is not None:
                self.pause_button.update()
            self.draw()
        self.quit_game()

    def events(self):
        """Click: None, Left, Middle, Right, Scroll Up, Scroll Down"""
        self.click = self.main.click = [None, False, False, False, False, False]

        """Events"""
        self.event = pygame.event.get()
        for event in self.event:
            # Rescale mouse position to screen size
            self.mouse = self.main.mouse = pygame.mouse.get_pos()
            if self.gameDisplay.factor_w != 1 or self.gameDisplay.factor_h != 1:
                mouse_w = int((self.mouse[0] - self.gameDisplay.game_gap[0]) / self.gameDisplay.factor_w)
                mouse_h = int(self.mouse[1] / self.gameDisplay.factor_h)
                self.mouse = self.main.mouse = (mouse_w, mouse_h)

            # Rescale mouse position to camera
            self.mouse_camera = self.main.mouse_camera = (self.mouse[0] + self.camera.offset.x, self.mouse[1] + self.camera.offset.y)

            # Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 1 <= event.button <= 5:
                    self.click[event.button] = True

            # Keyboard
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit_game()
                elif event.key == pygame.K_p:
                    self.paused_check = self.pause_game(self.paused_check)
                elif event.key == pygame.K_h:
                    self.debug_check = self.debug_game(self.debug_check)
                elif event.key == pygame.K_1:
                    self.camera.method = self.camera.follow
                elif event.key == pygame.K_2:
                    self.camera.method = self.camera.border
                elif event.key == pygame.K_3:
                    self.camera.method = self.camera.auto
                elif event.key == pygame.K_4:
                    self.camera.list_next()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    self.paused_check = False
                elif event.key == pygame.K_h:
                    self.debug_check = False

            # Quit Game (X Button)
            if event.type == pygame.QUIT:
                self.quit_game()

    @staticmethod
    def quit_game():
        pygame.quit()
        quit()

    @staticmethod
    def play_sound(sound, check=False):
        """Play a sound and prevents repetition by returning True"""
        if sound is not None and not check:
            pygame.mixer.Sound.play(sound)
            return True

    # Update ----------------------- #
    def update(self):
        self.main.update()
        self.camera.update()
        self.gameDisplay.update(self.event)

    # Draw ----------------------- #
    def draw(self):
        self.draw_background()
        self.draw_debug_camera()
        self.main.draw()
        self.draw_pause()
        self.gameDisplay.draw()

    def draw_background(self):
        if self.background_color is not None:
            self.gameDisplay.fill(self.background_color)
        if self.background_image is not None:
            self.gameDisplay.blit(self.background_image, (0, 0))

    def draw_debug_camera(self):
        # Test moving camera (Debug WIP)
        rect = [0, 0, self.screen_width, self.screen_height]
        rect[0], rect[1] = self.compute_camera_offset(rect)
        pygame.draw.rect(self.gameDisplay, CYAN, rect)

        # Draw player (Debug WIP)
        if self.debug_mode:
            self.camera.draw()

    def draw_pause(self):
        if self.paused:
            self.gameDisplay.blit(self.dim_screen, (0, 0))
            self.gameDisplay.blit(self.pause_text_surface, self.pause_text_rect)
            self.pause_button.draw()

    # Setting ----------------------- #
    def setting_background(self, background):
        """Update the background"""
        if background in self.graphic_dict:
            background = self.graphic_dict[background]
            if background["color"] is not None:
                self.background_color = background["color"]
            if background["image"] is not None:
                self.background_image = load_image(self.graphic_folder, background["image"])

    def setting_music(self, music):
        """Update the music"""
        if music in self.music_dict:
            music = self.music_dict[music]
            if self.music != music and music is not None:
                self.music = music
                pygame.mixer.music.load(self.music)
                pygame.mixer.music.play(-1)

    def setting_volume_music(self, dv=0):
        """Update the music volume by dv (from 0 to 100)"""
        self.music_volume = min(max(0, self.music_volume + dv), 100)
        pygame.mixer.music.set_volume(self.music_volume/100)

    # Compute ----------------------- #
    def compute_text(self, text, font, color, pos, align="nw"):
        """Return a surface and its rectangle with text drawn on it"""
        if text is not None and font is not None:
            text = str(text)
            text_surface = font.render(text, True, color)
            text_surface_rect = align_surface(text_surface, pos, align)
            return text_surface, text_surface_rect
        return None, None

    @staticmethod
    def compute_text_pos(rect):
        """Return text position centered in the rectangle"""
        return [rect[0] + rect[2] // 2, rect[1] + rect[3] // 2]

    def compute_camera_offset(self, item):
        """Returns the position offset from the camera position"""
        return int(item[0] - self.camera.offset.x), int(item[1] - self.camera.offset.y)

    # Button ----------------------- #
    def pause_game(self, paused_check=False):
        """Pause the game: self.paused_check = self.pause_game(self.paused_check) to avoid repetition when holding pause shortcut"""
        if not paused_check:
            self.paused = not self.paused
            if self.paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
        return True

    def debug_game(self, debug_check=False):
        if not debug_check:
            self.debug_mode = not self.debug_mode
        return True



m = Game()
while True:
    m.run()
