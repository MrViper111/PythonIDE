from cmu_graphics import *

from common.colors import Colors
from common.config import ConfigData
from common.files import Files
from common.textpointer import TextPointer
from common.asthelper import *

import string


class TextArea:

    x: int
    y: int
    width: int
    height: int
    content: list[list]
    position: int

    def __init__(self, app, x, y, width, height):
        self.app = app
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.content = [[1]]
        self.token_content = []
        self.position = 0
        self.text_color = Colors.parseRGB(ConfigData.THEME_DATA["text"])
        self.fill_color = Colors.parseRGB(ConfigData.THEME_DATA["text_area"])
        self.is_selected = False
        self.token_content = []

    def handle_key_press(self, keys: list[str]):
        if not self.is_selected:
            return

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

        code = Files.rebuild_content(self.content)
        self.token_content = parse_code_to_tokens(self.app, code, ConfigData.HIGHLIGTING)

    def handle_click(self, app, mouse_x, mouse_y):
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y + self.height

        if not (x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2):
            self.is_selected = False
            return

        self.is_selected = True
        char_width = ConfigData.FONT_SIZE * 0.6
        starting_x = mouse_x - 10 - app.line_numbers_width_real - app.file_structure_width
        starting_y = mouse_y - 20 - app.top_bar_height

        # idea to use min here came from Evan
        num_rows = len(self.content)
        selected_row = int(min(rounded(starting_y / 20), num_rows - 1))
        num_cols = len(self.content[selected_row])
        selected_col = int(min(rounded(starting_x / char_width), num_cols))

        current_row = 0
        current_col = 0
        for i, row in enumerate(self.content):
            if 1 in row:
                current_row = i
                current_col = row.index(1)

        TextPointer.move_cursor(self.content, current_row, current_col, selected_row, selected_col)

    def draw(self):
        cmu_graphics.drawRect(self.x, self.y, self.width, self.height, fill=self.fill_color)

    def draw_content(self):
        x = self.x + 10
        font_size = ConfigData.FONT_SIZE
        font = ConfigData.FONT

        line_height = 20
        char_width = ConfigData.FONT_SIZE * 0.6

        if not app.code_is_invalid:
            for line_idx, line in enumerate(self.token_content):
                x = app.file_structure_width + app.line_numbers_width_real + 10
                y = line_idx * line_height + app.top_bar_height + 20
                for token in line:
                    cmu_graphics.drawLabel(token.label, x, y, align="left", font=font, fill=token.color, size=font_size)
                    cmu_graphics.drawLabel(token.label, x, y, align="left", font=font, fill=token.color, size=font_size)
                    x += len(token.label) * char_width
        else:
            for i, row in enumerate(self.content):
                y = self.y + (20 * i) + 20
                line_content = "".join(str(c) for c in row if c != 1)
                cmu_graphics.drawLabel(line_content, x, y, fill=self.text_color, size=font_size, align="left", font=font)
                cmu_graphics.drawLabel(line_content, x, y, fill=self.text_color, size=font_size, align="left", font=font)
