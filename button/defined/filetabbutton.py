import os

from button.button import Button
from cmu_graphics import *
# from common.asthelper import ASTHelper
from common.colors import Colors
from common.config import ConfigData
from common.files import Files
from common.utils import Utils


class FileTabButton(Button):

    def __init__(self, app, x, y, label, align="left"):
        super().__init__(app, x, y, label, app.background_color, align=align, width=120)
        self.height = app.top_bar_height
        self.close_x = self.x + self.width - 15
        self.saved_x = self.x + 8
        self.is_saved = False

    def on_click(self):
        ...

    def handle_click(self, mouse_x, mouse_y):
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y + self.height

        if x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2:
            if Utils.distance(mouse_x, mouse_y, self.close_x, self.y) < 15:
                app.open_files.remove(self)
            else:
                app.current_file = os.path.join(self.app.working_path, self.label)
                file_content = Files.get_content(app.current_file)
                parsed_content = Files.parse_content(file_content)
                self.app.textarea.content = parsed_content

    def on_hover(self):
        ...

    def handle_hover(self, mouse_x, mouse_y):
        ...

    def draw(self):
        cmu_graphics.drawRect(self.x, self.y, self.width, self.height, fill=self.color, align="left",
                              border=Colors.parseRGB(ConfigData.THEME_DATA["separator"]), borderWidth=2)
        cmu_graphics.drawLabel(self.label[:14], self.x + 15, self.y, fill=app.text_color, align="left")
        cmu_graphics.drawCircle(self.saved_x, self.y, 3, fill="red")
        cmu_graphics.drawLabel("x", self.x + self.width - 15, self.y, fill="gray", align="left", size=16)
