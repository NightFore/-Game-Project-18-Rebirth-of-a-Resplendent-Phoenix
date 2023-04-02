import pygame
from Function import *
from Settings import *

main_dict = {
    "tile_size": (32, 32), "player_speed": 300,
    "night_color": (30, 43, 88), "night_transparency": 100
}

game_dict = {
    "project_title": "Rebirth of a Resplendent Phoenix", "screen_size": (1280, 960), "FPS": 60,
    "default_music_volume": 5, "default_sound_volume": 75,
    "key_repeat": (100, 30),
}

font_dict = {
    "default": {"ttf": None, "size": 100},
    "LiberationSerif": {"ttf": "LiberationSerif-Regular.ttf", "size": 40},
    "LiberationSerif_30": {"ttf": "LiberationSerif-Regular.ttf", "size": 30}
}

graphic_dict = {
    "Test": {
        "path": "sprite_Aekashics_Phoenix.png",
        "size_scaled": [128, 128], "color_key": None, "align": "nw",
        "image_tables": [[0, 0, 3, 1], [3, 0, 3, 1], [6, 0, 3, 1],
                         [0, 1, 3, 1], [3, 1, 3, 1], [6, 1, 3, 1]],
        "image_size": [384, 384], "image_offset": [0, 0],
        "animation": True, "loop": True, "loop_reverse": False, "loop_delay": 0, "frame_speed": 4,
    },
    "tile_grass_1": {
        "path": "grass.png",
        "size_scaled": [32, 32], "color_key": None, "align": "nw",
        "image_tables": [[0, 4, 1, 1]],
        "image_size": [32, 32], "image_offset": [0, 0],
        "animation": False,
    },
    "sprite_phoenix": {
        "path": "sprite_Aekashics_Phoenix.png",
        "size_scaled": [128, 128], "color_key": None, "align": "center",
        "image_tables": [[0, 0, 3, 1]],
        "image_size": [384, 384], "image_offset": [0, 0],
        "animation": True, "loop": True, "loop_reverse": True, "loop_delay": 0, "frame_speed": 10,
    },
    "portrait_phoenix": {
        "path": "sprite_Aekashics_Phoenix.png",
        "size_scaled": [96, 96], "color_key": None, "align": "nw",
        "image_tables": [[0, 1, 1, 1]],
        "image_size": [384, 384], "image_offset": [0, 0],
        "animation": False
    },
    "sprite_sun_goddess": {
        "path": "sprite_Aekashics_Sun_Goddess.png",
        "size_scaled": [128, 128], "color_key": None, "align": "center",
        "image_tables": [[0, 0, 4, 1]],
        "image_size": [384, 384], "image_offset": [0, 0],
        "animation": True, "loop": True, "loop_reverse": True, "loop_delay": 0, "frame_speed": 10,
    },
    "sprite_vi1": {
        "path": "sprite_Aekashics_Vi1_1.png",
        "size_scaled": [128, 128], "color_key": None, "align": "center",
        "image_tables": [[0, 0, 9, 6]],
        "image_size": [256, 256], "image_offset": [0, 0],
        "animation": True, "loop": True, "loop_reverse": True, "loop_delay": 0, "frame_speed": 10,
    },
    "sprite_enemy": {
        "path": "sprite_pipoya_enemy_15_1.png",
        "size_scaled": [32, 32], "color_key": None, "align": "center",
        "image_tables": [[0, 0, 3, 1], [0, 1, 3, 1], [0, 2, 3, 1], [0, 3, 3, 1]],
        "image_size": [32, 32], "image_offset": [0, 0],
        "animation": True, "loop": True, "loop_reverse": True, "loop_delay": 0, "frame_speed": 10,
    },
    "sprite_ghost_blue": {
        "path": "sprite_pipoya_enemy_15_2.png",
        "size_scaled": [32, 32], "color_key": None, "align": "center",
        "image_tables": [[0, 0, 3, 1], [0, 1, 3, 1], [0, 2, 3, 1], [0, 3, 3, 1]],
        "image_size": [32, 32], "image_offset": [0, 0],
        "animation": True, "loop": True, "loop_reverse": True, "loop_delay": 0, "frame_speed": 10,
    },
    "sprite_ghost_red": {
        "path": "sprite_pipoya_enemy_15_3.png",
        "size_scaled": [32, 32], "color_key": None, "align": "center",
        "image_tables": [[0, 0, 3, 1], [0, 1, 3, 1], [0, 2, 3, 1], [0, 3, 3, 1]],
        "image_size": [32, 32], "image_offset": [0, 0],
        "animation": True, "loop": True, "loop_reverse": True, "loop_delay": 0, "frame_speed": 10,
    },
    "sprite_grave": {
        "path": "tile_pipoya_base_chip.png",
        "size_scaled": [32, 32], "color_key": None, "align": "center",
        "image_tables": [[3, 8, 1, 1]],
        "image_size": [32, 32], "image_offset": [0, 0],
        "animation": False,
    },
    "effect_gate": {
        "path": "effect_pipoya_gate01a.png",
        "size_scaled": [240, 240], "color_key": None, "align": "center",
        "image_tables": [[0, 0, 5, 3]],
        "image_size": [480, 480], "image_offset": [0, 0],
        "animation": True, "loop": True, "loop_reverse": False, "loop_delay": 0, "frame_speed": 4,
    },
    "effect_energy_ball": {
        "path": "effect_Pimen_energy_ball_128x128.png",
        "size_scaled": [64, 64], "color_key": None, "align": "center",
        "image_tables": [[0, 0, 9, 1]],
        "image_size": [128, 128], "image_offset": [0, 0],
        "animation": True, "loop": True, "loop_reverse": False, "loop_delay": 0, "frame_speed": 4,
    },
    "heart": {
        "path": "item_beyonderboy_heart.png",
        "size_scaled": [32, 32], "color_key": None, "align": "center",
        "image_tables": None,
        "animation": False
    },
    "portrait_ally": {
        "path": "sprite_Kaduki_Actor63_default.png",
        "size_scaled": [32, 32], "color_key": None, "align": "center",
        "image_tables": [[0, 0, 1, 1]],
        "image_size": [32, 32], "image_offset": [0, 0],
        "animation": False,
    },
    "portrait_enemy": {
        "path": "sprite_pipoya_enemy_15_1.png",
        "size_scaled": [32, 32], "color_key": None, "align": "center",
        "image_tables": [[0, 0, 1, 1]],
        "image_size": [32, 32], "image_offset": [0, 0],
        "animation": False,
    },
    "portrait_grave": {
        "path": "tile_pipoya_base_chip.png",
        "size_scaled": [32, 32], "color_key": None, "align": "center",
        "image_tables": [[3, 8, 1, 1]],
        "image_size": [32, 32], "image_offset": [0, 0],
        "animation": False,
    },

}

music_dict = {
    "default": None,
    "battle_1": "MaouDamashii_Neorock16_Battle_The_Hunt_is_On.mp3",
    "battle_2": "MaouDamashii_Neorock49_Battle_Heroic_Entrance.mp3",
    "battle_3": "MaouDamashii_Neorock55_Battle_Running_Through_the_Hills.mp3"
}

sound_dict = {
}

cursor_dict = {
    "default": {
        "cursor_size": (32, 32), "cursor_size_border": [5, 5], "cursor_align": "nw",
        "cursor_color": RED, "cursor_color_border": LIGHTBLUE,
    }
}

button_dict = {
    "settings": {
        "init_functions": {load_button, load_text, load_sound, load_action},
        "default": {
            "size": [280, 50], "color": [DARK_SKY_BLUE, LIGHT_SKY_BLUE], "align": "nw",
            "border_size": [5, 5], "border_color": BLACK,
            "text_font": "LiberationSerif", "text_color": WHITE, "text_align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None},
        "center": {
            "size": [280, 50], "color": [DARK_SKY_BLUE, LIGHT_SKY_BLUE], "align": "center",
            "border_size": [5, 5], "border_color": BLACK,
            "text_font": "LiberationSerif", "text_color": WHITE, "text_align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None},
        "icon": {
            "size": [50, 50], "color": [DARK_SKY_BLUE, LIGHT_SKY_BLUE], "align": "nw",
            "border_size": [5, 5], "border_color": BLACK,
            "text_font": "LiberationSerif", "text_color": WHITE, "text_align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None},
        "icon_center": {
            "size": [50, 50], "color": [DARK_SKY_BLUE, LIGHT_SKY_BLUE], "align": "center",
            "border_size": [5, 5], "border_color": BLACK,
            "text_font": "LiberationSerif", "text_color": WHITE, "text_align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None},
        "image": {
            "align": "center",
            "text_font": "LiberationSerif", "text_color": WHITE, "text_align": "center",
            "sound_action": None, "sound_active": None, "sound_inactive": None}
    },
    "title": {
        "new_game": {"settings": "default", "position": [10, 50], "text": "New Game", "action": "self.main.init_level"},
        "volume_up": {"settings": "default", "position": [10, 120], "text": "Volume +", "argument": +5, "action": "self.game.setting_volume_music"},
        "volume_down": {"settings": "default", "position": [10, 190], "text": "Volume -", "argument": -5, "action": "self.game.setting_volume_music"},
        "new_music": {"settings": "default", "position": [10, 260], "text": "Change Music", "action": "self.main.new_music"},
        "fullscreen": {"settings": "default", "position": [10, 330], "text": "Fullscreen", "action": "self.game.gameDisplay.fullscreen"},
        "quit_game": {"settings": "default", "position": [10, 400], "text": "Quit Game", "action": "self.game.quit_game"},
    },
    "level": {
        "new_music": {"settings": "icon_center", "position": [1210, 905], "text": "♫", "action": "self.main.new_music"},
    },
    "new_game": {
        "new_game": {"settings": "center", "position": [640, 600], "text": "New Game", "argument": True, "action": "self.main.init_level"},
    }
}

level_dict = {
    "chapter_prologue": {
        "map": 30 * [40 * [0]],
        "music": {
            "preparation": None,
            "map": None,
            "battle": "battle",
        },
        "units": [
            {"type": "gate"},
        ],
        "win": "Rout"
    },
}

unit_dict = {
    "player": {
        "image": "sprite_phoenix",
        "pos": [640, 480]
    },
    "gate": {
        "image": "effect_gate",
        "pos": [640, 480], "hit_rect": [120, 120]
    },
    "ghost_black": {
        "image": "sprite_enemy", "pos": [0, 0], "health": 1
    },
    "ghost_red": {
        "image": "sprite_ghost_red", "pos": [0, 0], "health": 2
    },
    "ghost_blue": {
        "image": "sprite_ghost_blue", "pos": [0, 0], "health": 3
    },
    "sprite_vi1": {
        "image": "sprite_vi1", "pos": [0, 0]
    },
}

effect_dict = {
    "line_of_fire": {
        "image": "effect_line_of_fire",
        "speed": 300
    },
    "energy_ball": {
        "image": "effect_energy_ball",
        "speed": 400
    }
}

item_dict = {
    "heart": {
        "image": "heart",
        "speed": 300
    },
}

kaduki_dict = {
    "default": {
        "path": "placeholder",
        "size_scaled": [48, 48], "color_key": None, "align": "center",
        "image_tables": [[0, 0, 3, 1], [0, 1, 3, 1], [0, 2, 3, 1], [0, 3, 3, 1]],
        "image_size": [32, 32], "image_offset": [0, 0],
        "animation": True, "loop": True, "loop_reverse": False, "loop_delay": 0, "frame_speed": 4,
    },
}

kaduki_sprite = [
    "sprite_Kaduki_abe_default.png",
    "sprite_Kaduki_Actor4_default.png",
    "sprite_Kaduki_Actor5_default.png",
    "sprite_Kaduki_Actor6_default.png",
    "sprite_Kaduki_Actor7_default.png",
    "sprite_Kaduki_Actor8_default.png",
    "sprite_Kaduki_Actor9_default.png",
    "sprite_Kaduki_Actor10_default.png",
    "sprite_Kaduki_Actor11_default.png",
    "sprite_Kaduki_Actor12_default.png",
    "sprite_Kaduki_Actor13b_default.png",
    "sprite_Kaduki_Actor14_default.png",
    "sprite_Kaduki_Actor15_default.png",
    "sprite_Kaduki_Actor16_default.png",
    "sprite_Kaduki_Actor18_default.png",
    "sprite_Kaduki_Actor19_default.png",
    "sprite_Kaduki_Actor20_default.png",
    "sprite_Kaduki_Actor21_default.png",
    "sprite_Kaduki_Actor22_default.png",
    "sprite_Kaduki_Actor23_default.png",
    "sprite_Kaduki_Actor26_default.png",
    "sprite_Kaduki_Actor27_default.png",
    "sprite_Kaduki_Actor28_default.png",
    "sprite_Kaduki_Actor29_default.png",
    "sprite_Kaduki_Actor30_default.png",
    "sprite_Kaduki_Actor31_default.png",
    "sprite_Kaduki_Actor32_default.png",
    "sprite_Kaduki_Actor33_default.png",
    "sprite_Kaduki_Actor34_default.png",
    "sprite_Kaduki_Actor36_default.png",
    "sprite_Kaduki_Actor37_default.png",
    "sprite_Kaduki_Actor38_default.png",
    "sprite_Kaduki_Actor39_default.png",
    "sprite_Kaduki_Actor40_default.png",
    "sprite_Kaduki_Actor41_default.png",
    "sprite_Kaduki_Actor42_default.png",
    "sprite_Kaduki_Actor43_default.png",
    "sprite_Kaduki_Actor44_default.png",
    "sprite_Kaduki_Actor45_default.png",
    "sprite_Kaduki_Actor46_default.png",
    "sprite_Kaduki_Actor50_default.png",
    "sprite_Kaduki_Actor55_default.png",
    "sprite_Kaduki_Actor57_default.png",
    "sprite_Kaduki_Actor58_default.png",
    "sprite_Kaduki_Actor59_default.png",
    "sprite_Kaduki_Actor60_default.png",
    "sprite_Kaduki_Actor61_default.png",
    "sprite_Kaduki_Actor62_default.png",
    "sprite_Kaduki_Actor63_default.png",
    "sprite_Kaduki_Actor64a_default.png",
    "sprite_Kaduki_Actor64b_default.png",
    "sprite_Kaduki_Actor66_default.png",
    "sprite_Kaduki_Actor68_default.png",
    "sprite_Kaduki_Actor69_default.png",
    "sprite_Kaduki_Actor69ex_default.png",
    "sprite_Kaduki_Actor70_default.png",
    "sprite_Kaduki_Actor71_default.png",
    "sprite_Kaduki_Actor72_default.png",
    "sprite_Kaduki_Actor73_default.png",
    "sprite_Kaduki_Actor74_default.png",
    "sprite_Kaduki_Actor75_default.png",
    "sprite_Kaduki_Actor76_default.png",
    "sprite_Kaduki_Actor78_default.png",
    "sprite_Kaduki_Actor79_default.png",
    "sprite_Kaduki_Actor80_default.png",
    "sprite_Kaduki_Actor83_default.png",
    "sprite_Kaduki_Actor84_default.png",
    "sprite_Kaduki_Actor85_default.png",
    "sprite_Kaduki_Actor86_default.png",
    "sprite_Kaduki_Actor87_default.png",
    "sprite_Kaduki_Actor88_default.png",
    "sprite_Kaduki_Actor89_default.png",
    "sprite_Kaduki_Actor90_default.png",
    "sprite_Kaduki_Actor91_default.png",
    "sprite_Kaduki_Actor94_default.png",
    "sprite_Kaduki_Actor95_default.png",
    "sprite_Kaduki_Actor96_default.png",
    "sprite_Kaduki_Actor97_default.png",
    "sprite_Kaduki_Actor98_default.png",
    "sprite_Kaduki_Actor99_default.png",
    "sprite_Kaduki_Actor100_default.png",
    "sprite_Kaduki_Actor101_default.png",
    "sprite_Kaduki_Actor102_default.png",
    "sprite_Kaduki_Actor102b_default.png",
    "sprite_Kaduki_Actor103_default.png",
    "sprite_Kaduki_Actor104_default.png",
    "sprite_Kaduki_Actor106_default.png",
    "sprite_Kaduki_Actor107_default.png",
    "sprite_Kaduki_Actor108_default.png",
    "sprite_Kaduki_Actor109_default.png",
    "sprite_Kaduki_Actor110_default.png",
    "sprite_Kaduki_Actor111_default.png",
    "sprite_Kaduki_Actor112_default.png",
    "sprite_Kaduki_Actor113_default.png",
    "sprite_Kaduki_Actor114_default.png",
    "sprite_Kaduki_Actor115_default.png",
    "sprite_Kaduki_Actor117_default.png",
    "sprite_Kaduki_Actor120_default.png",
    "sprite_Kaduki_Actor121_default.png",
    "sprite_Kaduki_Actor122_default.png",
    "sprite_Kaduki_Actor125_default.png",
    "sprite_Kaduki_Actor130_default.png",
    "sprite_Kaduki_Actor131_default.png",
    "sprite_Kaduki_Actor132a_default.png",
    "sprite_Kaduki_Actor132b_default.png",
    "sprite_Kaduki_Actor134_default.png",
    "sprite_Kaduki_Actor137_default.png",
    "sprite_Kaduki_Actor138_default.png",
    "sprite_Kaduki_Actor139_default.png",
    "sprite_Kaduki_Actor140_default.png",
    "sprite_Kaduki_Actor141_default.png",
    "sprite_Kaduki_Actor142_default.png",
    "sprite_Kaduki_Actor143_default.png",
    "sprite_Kaduki_Actor144_default.png",
    "sprite_Kaduki_etc1_default.png"]

interface_dict = {
    "heart": {"image": "heart", "pos": [120, 45]}
}