import os
from cmu_graphics import *

from button.button import Button
# from common.asthelper import ASTHelper
from common.files import Files


class IconButton(Button):

    def __init__(self, app, x, y, icon, size=30, tooltip=None, align="center"):
        super().__init__(app, x, y, "", align=align, tooltip=tooltip, color=None)
        self.icon = icon
        self.size = size

    def on_click(self):
        ...

    def on_hover(self):
        ...

    def handle_hover(self, mouse_x, mouse_y):
        ...

    def draw(self):
        cmu_graphics.drawImage(self.icon, self.x, self.y, width=self.size, height=self.size)
        print(self.x, self.y)
