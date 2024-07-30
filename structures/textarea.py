from cmu_graphics import *

from common.colors import Colors
from common.config import ConfigData
from common.files import Files
from common.textpointer import TextPointer
from common.astheleper import *

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
        self.token_content = []
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

        code = Files.rebuild_content(self.content)
        token_content = parse_code_to_tokens(code, {
            "keywords": "orange",
            "variables": "lightBlue",
            "functions": "yellow",
            "strings": "lightGreen"
        })

        # for line in token_content:
        #     for token in line:
        #         if token.label.isspace():
        #             continue
        #
        #         token.label = token.label.strip()

        print(token_content)

        line_height = 20
        char_width = ConfigData.FONT_SIZE * 0.6

        for line_idx, line in enumerate(token_content):
            x = app.file_structure_width + app.line_numbers_width_real + 10
            y = line_idx * line_height + app.top_bar_height + 20
            for token in line:
                cmu_graphics.drawLabel(token.label, x, y, align="left", font=font, fill=token.color, size=font_size)
                cmu_graphics.drawLabel(token.label, x, y, align="left", font=font, fill=token.color, size=font_size)
                x += len(token.label) * char_width

        # for i, row in enumerate(self.content):
        #     y = self.y + (20 * i) + 20
        #     line_content = "".join(str(c) for c in row if c != 1)
        #     cmu_graphics.drawLabel(line_content, x, y, fill=self.text_color, size=font_size, align="left", font=font)
        #     cmu_graphics.drawLabel(line_content, x, y, fill=self.text_color, size=font_size, align="left", font=font)
