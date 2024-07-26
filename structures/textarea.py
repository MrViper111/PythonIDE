from cmu_graphics import *

from common.colors import Colors
from common.config import Config, ConfigData
from common.textpointer import TextPointer

import string


# store stuff another way
#


class TextArea:

    x: int
    y: int
    width: int
    height: int
    content: list[list]
    position: int

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.content = [[1]]
        self.position = 0
        self.text_color = Colors.parseRGB(ConfigData.THEME_DATA["text"])
        self.fill_color = Colors.parseRGB(ConfigData.THEME_DATA["text_area"])

    def handle_key_press(self, keys: list[str]):
        tab_size = ConfigData.TAB_SIZE

        if "control" in keys and "backspace" in keys:
            self.content = TextPointer.handle_ctrl_backspace(self.content)
        elif "backspace" in keys:
            self.content = TextPointer.handle_backspace(self.content)
        elif "enter" in keys:
            self.content = TextPointer.handle_enter(self.content)
        elif "up" in keys:
            self.content = TextPointer.shift_pointer(self.content, (-1, 0))
        elif "down" in keys:
            self.content = TextPointer.shift_pointer(self.content, (1, 0))
        elif "left" in keys:
            self.content = TextPointer.shift_pointer(self.content, (0, -1))
        elif "right" in keys:
            self.content = TextPointer.shift_pointer(self.content, (0, 1))
        elif "space" in keys:
            self.content = TextPointer.insert_char(self.content, " ")
        elif "tab" in keys:
            for i in range(tab_size):
                TextPointer.insert_char(self.content, " ")
        elif any(key in char for key in keys for char in string.printable):
            for char in keys:
                self.content = TextPointer.insert_char(self.content, char)
        print(self.content)

    def draw(self):
        cmu_graphics.drawRect(self.x, self.y, self.width, self.height, fill=self.fill_color)

    def draw_content(self):
        x = self.x + 10
        font_size = ConfigData.FONT_SIZE
        font = ConfigData.FONT

        for i, row in enumerate(self.content):
            y = self.y + (20 * i) + 20
            line_content = "".join(str(c) for c in row if c != 1)
            cmu_graphics.drawLabel(line_content, x, y, fill=self.text_color, size=font_size, align="left", font=font)
            cmu_graphics.drawLabel(line_content, x, y, fill=self.text_color, size=font_size, align="left", font=font)
