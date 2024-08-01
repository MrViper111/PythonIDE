import cmu_graphics
from cmu_graphics import *
from abc import ABC, abstractmethod

from common.colors import Colors
from common.config import Config, ConfigData
from structures.tooltip import Tooltip


class Button(ABC):

    x: int
    y: int
    label: str
    color: list
    align: str
    label_align: str
    width: int
    tooltip: Tooltip
    is_hovered: bool
    image: str

    def __init__(self, app, x, y, label, color, align="center", label_align="center", width=None, tooltip=None, image=None):
        self.app = app
        self.x = x
        self.y = y
        self.label = label
        self.label_align = label_align
        self.color = color
        self.align = align
        self.tooltip = tooltip
        self.image = image
        self.is_hovered = False
        self.height = 25

        if width:
            self.width = width
        else:
            self.width = 20 + len(self.label) * 5

    def handle_click(self, mouse_x, mouse_y):
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y + self.height

        if x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2:
            self.on_click()

    @abstractmethod
    def on_click(self):
        pass

    def handle_hover(self, mouse_x, mouse_y):
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y + self.height

        self.is_hovered = (x1 <= mouse_x <= x2) and (y1 <= mouse_y <= y2)

        if self.is_hovered:
            self.on_hover()

    @abstractmethod
    def on_hover(self):
        pass

    def draw(self):
        cmu_graphics.drawRect(self.x, self.y, self.width, self.height, fill=self.color, align=self.align)

        offset = (self.width / 2) if self.label_align == "left" else 0
        cmu_graphics.drawLabel(self.label, self.x, self.y + self.height//2, fill=app.text_color, align=self.label_align)

    def draw_tooltip(self):
        if not self.tooltip:
            return

        self.tooltip.draw(self.x + self.width + len(self.tooltip.text) * 5.5, self.y + self.height // 2)
