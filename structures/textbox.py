from cmu_graphics import *

from common.colors import Colors
from common.config import ConfigData


class Textbox:

    x: int
    y: int
    placeholder: str
    width: int
    content: str

    def __init__(self, app, x, y, placeholder, width):
        self.x = x
        self.y = y
        self.placeholder = placeholder
        self.width = width
        self.height = 30
        self.content = ""
        self.selected = False

    def draw(self):
        color = Colors.parseRGB(ConfigData.THEME_DATA["text_area"])
        cmu_graphics.drawRect(self.x, self.y, self.width, self.height, fill=color)
        cmu_graphics.drawLabel(self.placeholder, self.x + 6, self.y + self.height / 2, fill="gray", align="left")
