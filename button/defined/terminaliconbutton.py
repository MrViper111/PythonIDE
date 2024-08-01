import os
from cmu_graphics import *
import subprocess

from button.button import Button
# from common.asthelper import ASTHelper
from abc import ABC, abstractmethod

from button.defined.filebutton import FileButton
from button.defined.folderbutton import FolderButton
from common.files import Files

# I got the idea on how to implement this from:
# - https://www.dataquest.io/blog/python-subprocess/
# - https://support.apple.com/lt-lt/guide/terminal/trml1003/mac

class TerminalIconButton(Button):

    def __init__(self, app, x, y, icon, size=30, tooltip=None, align=" "):
        super().__init__(app, x, y, "", align=align, tooltip=tooltip, color=None)
        self.icon = icon
        self.size = size

    def on_click(self):
        directory = self.app.working_path
        subprocess.run(["open", "-a", "Terminal", directory])

    def on_hover(self):
        ...

    def handle_hover(self, mouse_x, mouse_y):
        ...

    def draw(self):
        cmu_graphics.drawImage(self.icon, self.x, self.y, width=self.size, height=self.size)
