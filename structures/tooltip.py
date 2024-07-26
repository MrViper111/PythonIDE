from cmu_graphics import *


class Tooltip:

    text: str
    opacity: int

    def __init__(self, text, opacity=50):
        self.text = text
        self.opacity = opacity

    def draw(self, x, y):
        cmu_graphics.drawRect(x, y, len(self.text) * 10, 20, opacity=self.opacity, align="center")
        cmu_graphics.drawLabel(self.text, x, y, fill="white")
