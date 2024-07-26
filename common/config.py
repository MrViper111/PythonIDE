import json
import os


class Config:

    CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")

    @staticmethod
    def load():
        with open(Config.CONFIG_PATH, "r") as file:
            return json.load(file)


class ConfigData:
    DATA = Config.load()

    WINDOW_TITLE = DATA["window"]["title"]
    WINDOW_HEIGHT = DATA["window"]["height"]
    WINDOW_WIDTH = DATA["window"]["width"]

    TAB_SIZE = DATA["editor"]["tab_size"]
    DOUBLE_WRITE = DATA["editor"]["double_write"]

    THEME = DATA["style"]["theme"]
    FONT = DATA["style"]["font"]
    FONT_SIZE = DATA["style"]["font_size"]
    THEMES = DATA["style"]["themes"]
    THEME_DATA = THEMES[THEME]
