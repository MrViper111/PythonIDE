import os

from button.button import Button
from button.defined.filetabbutton import FileTabButton
from common.files import Files


class FileButton(Button):

    def __init__(self, app, x, y, width, label, color, text_color=None, align="left"):
        super().__init__(app, x, y, label, color, text_color, align, width=width)
        self.old_color = self.color

    def on_click(self):
        label = self.label.strip()
        file_content = Files.get_content(os.path.join(self.app.working_path, label))
        parsed_content = Files.parse_content(file_content)
        self.app.textarea.content = parsed_content

        print(self.app.open_files)
        if label not in self.app.open_files:
            self.app.open_files.append(FileTabButton(self.app,
                                                  self.app.file_structure_width + (120 * len(self.app.open_files)),
                                                  self.app.top_bar_height / 2, label))

    def on_hover(self):
        ...

    def handle_hover(self, mouse_x, mouse_y):
        x1 = self.x
        y1 = self.y
        x2 = self.x + self.width
        y2 = self.y + self.height

        self.is_hovered = (x1 <= mouse_x <= x2) and (y1 <= mouse_y <= y2)

        if self.is_hovered:
            self.color = self.app.file_hover_background_color
        else:
            self.color = self.old_color
