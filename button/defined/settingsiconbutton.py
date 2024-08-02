import os

from button.button import Button
from button.defined.filetabbutton import FileTabButton
from common.files import Files
from common.config import ConfigData
from common.asthelper import *


class SettingsIconButton(Button):

    def __init__(self, app, x, y, icon, size=30, tooltip=None, align="left"):
        super().__init__(app, x, y, "", align=align, tooltip=tooltip, color=None)
        self.icon = icon
        self.size = size

    def on_click(self):
        label = self.label.strip()
        self.app.current_file = "config.json"
        file_content = Files.get_content(self.app.current_file)
        parsed_content = Files.parse_content(file_content)
        self.app.textarea.content = parsed_content

        code = Files.rebuild_content(self.app.textarea.content)
        self.app.textarea.token_content = parse_code_to_tokens(self.app, code, ConfigData.HIGHLIGTING)

    def on_hover(self):
        ...

    def handle_hover(self, mouse_x, mouse_y):
        ...

