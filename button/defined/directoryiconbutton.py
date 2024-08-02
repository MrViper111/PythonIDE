import os
from cmu_graphics import *

from button.button import Button
# from common.asthelper import ASTHelper
from abc import ABC, abstractmethod

from button.defined.filebutton import FileButton
from button.defined.folderbutton import FolderButton
from common.files import Files


class DirectoryIconButton(Button):

    def __init__(self, app, x, y, icon, size=30, tooltip=None, align=" "):
        super().__init__(app, x, y, "", align=align, tooltip=tooltip, color=None)
        self.icon = icon
        self.size = size

    def on_click(self):
        new_directory = self.app.getTextInput("Enter directory")

        if not new_directory:
            return

        self.app.working_path = new_directory

        self.app.file_buttons.clear()
        clean_ls = [file for file in os.listdir(app.working_path) if not file.startswith(".")]
        try:
            for i, file in enumerate(clean_ls):
                if os.path.isfile(file):
                    app.file_buttons.append(FileButton(app, app.sidebar_width + 18, 40 + 25 * i, app.file_structure_width * 0.6,
                                                    f" {file}", app.background_color))
                else:
                    app.file_buttons.append(FolderButton(app, app.sidebar_width + 18, 40 + 25 * i, app.file_structure_width * 0.6,
                                                    f"> {file}", app.background_color))
        except:
            return

    def on_hover(self):
        ...

    def handle_hover(self, mouse_x, mouse_y):
        ...

    def draw(self):
        cmu_graphics.drawImage(self.icon, self.x, self.y, width=self.size, height=self.size)
