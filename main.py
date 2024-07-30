from cmu_graphics import *

from button.defined.filebutton import FileButton
from button.defined.filetabbutton import FileTabButton
from button.defined.folderbutton import FolderButton
from button.defined.iconbutton import IconButton
from common.colors import Colors
# from common.asthelper import AstVisitor, ASTHelper
from common.config import ConfigData, Config
from common.files import Files
from common.icons import Icons
from structures.textarea import TextArea

import os

from structures.textbox import Textbox
from structures.tooltip import Tooltip


def onAppStart(app):
    # config app
    app.stepsPerSecond = 0.0001

    # colors
    app.background_color = Colors.parseRGB(ConfigData.THEME_DATA["background"])
    app.sidebar_background_color = Colors.parseRGB(ConfigData.THEME_DATA["sidebar_background"])
    app.separator_color = Colors.parseRGB(ConfigData.THEME_DATA["separator"])
    app.text_color = Colors.parseRGB(ConfigData.THEME_DATA["text"])
    app.text_area_color = Colors.parseRGB(ConfigData.THEME_DATA["text_area"])
    app.select_bar_color = Colors.parseRGB(ConfigData.THEME_DATA["select_bar"])
    app.tooltip_background_color = Colors.parseRGB(ConfigData.THEME_DATA["tooltip_background"])
    app.button_background_color = Colors.parseRGB(ConfigData.THEME_DATA["button_background"])
    app.file_hover_background_color = Colors.parseRGB(ConfigData.THEME_DATA["file_hover_background"])

    # window sections
    app.top_bar_height = 35
    app.bottom_bar_height = 25
    app.sidebar_width = app.width * 0.06
    app.scroll_bar_width_real = 15
    app.file_structure_width = app.width * 0.23
    app.line_numbers_width_real = 30
    app.textarea_x = app.file_structure_width + app.line_numbers_width_real
    app.textarea_y = app.top_bar_height
    app.textarea_width = app.width - app.scroll_bar_width_real
    app.textarea_height = app.height - app.bottom_bar_height
    app.default_icon_width = 30

    app.textarea = TextArea(app.textarea_x, app.textarea_y, app.textarea_width, app.textarea_height)

    # other
    app.working_path = "."
    app.open_files = []
    print(app.width - app.scroll_bar_width_real - app.default_icon_width)
    app.buttons = [
        IconButton(app, app.width - app.scroll_bar_width_real - app.default_icon_width, 4,
                   Icons.RUN, tooltip=Tooltip("Run")),
        IconButton(app, (app.sidebar_width / 2) - app.default_icon_width / 2, 10, Icons.FILE),
        IconButton(app, (app.sidebar_width - app.default_icon_width) / 2,
                   app.height - (app.default_icon_width * 1.5) * 2,
                   Icons.TERMINAL),
        IconButton(app, (app.sidebar_width - app.default_icon_width) / 2, app.height - app.default_icon_width * 1.5,
                   Icons.SETTINGS),
    ]
    app.file_buttons = []
    app.special_tokens = {"func": set(), "var": set()}

    for i, file in enumerate(os.listdir(app.working_path)):
        if os.path.isfile(file):
            app.file_buttons.append(FileButton(app, app.sidebar_width + 18, 40 + 25 * i, app.file_structure_width * 0.6,
                                               f" {file}", app.background_color))
            continue
        app.file_buttons.append(FolderButton(app, app.sidebar_width + 18, 40 + 25 * i, app.file_structure_width * 0.6,
                                             f"> {file}", app.background_color))


def redrawAll(app):
    # drawing background
    cmu_graphics.drawRect(0, 0, app.width, app.height, fill=app.background_color)

    # drawing textarea
    app.textarea.width = app.width - app.scroll_bar_width_real
    app.textarea.height = app.height - app.bottom_bar_height
    app.textarea.draw()
    app.textarea.draw_content()

    # drawing text selector
    selector_location_x = 0
    selector_location_y = 0
    for i, line in enumerate(app.textarea.content):
        if 1 in line:
            selector_location_y = i
            selector_location_x = line.index(1)

    starting_selector_offset_x = app.file_structure_width + app.line_numbers_width_real  # all chars print after 10
    starting_selector_offset_y = app.top_bar_height + 20  # 20 is CONSTANT offset for textareas

    cmu_graphics.drawLine(
        starting_selector_offset_x + 10 + (ConfigData.FONT_SIZE * 0.6) * selector_location_x,
        starting_selector_offset_y + selector_location_y * 20 + 10,
        starting_selector_offset_x + 10 + (ConfigData.FONT_SIZE * 0.6) * selector_location_x,
        starting_selector_offset_y + selector_location_y * 20 - 10,
        fill=app.select_bar_color
    )

    # sidebar
    cmu_graphics.drawRect(0, 0, app.sidebar_width, app.height, fill=app.sidebar_background_color)
    cmu_graphics.drawLine(app.sidebar_width, 0, app.sidebar_width, app.height, fill=app.separator_color)

    # directory structure
    cmu_graphics.drawLabel("Directory Structure", (app.sidebar_width + app.file_structure_width) // 2, 20,
                           fill=app.text_color, bold=True, size=15)
    cmu_graphics.drawLine(app.file_structure_width, 0, app.file_structure_width, app.height, fill=app.separator_color)

    # line numbers
    cmu_graphics.drawRect(app.file_structure_width, app.top_bar_height,
                          app.line_numbers_width_real, app.width - app.bottom_bar_height, fill=app.text_area_color)
    cmu_graphics.drawLine(app.file_structure_width + app.line_numbers_width_real, app.top_bar_height,
                          app.file_structure_width + app.line_numbers_width_real, app.height - app.bottom_bar_height,
                          fill=app.separator_color)
    for i, line in enumerate(app.textarea.content):
        cmu_graphics.drawLabel(i + 1, app.file_structure_width + app.line_numbers_width_real - 7,
                               20 + app.top_bar_height + 20 * i, fill=app.text_color, font=ConfigData.FONT,
                               align="right")

    # bottom bar
    cmu_graphics.drawRect(app.file_structure_width, app.height - app.bottom_bar_height,
                          app.width - app.scroll_bar_width_real, app.bottom_bar_height, fill=app.background_color)
    cmu_graphics.drawLabel(f"Working directory: {app.working_path}", app.file_structure_width + 6,
                           app.height - app.bottom_bar_height / 2, fill=app.text_color, align="left")

    # drawing buttons
    for button in app.buttons:
        button.draw()

        if button.tooltip and button.is_hovered:
            button.draw_tooltip()

    for button in app.file_buttons:
        button.draw()

    print(app.open_files)
    for button in app.open_files:
        button.draw()

    # textbox = Textbox(app, 20, 200, "Enter name...", 90)
    # textbox.draw()


def onMousePress(app, mouseX, mouseY):
    # app.select_bar.handle_click(app, mouseX, mouseY)

    for button in app.buttons:
        button.handle_click(mouseX, mouseY)

    for file_tab_button in app.open_files:
        file_tab_button.handle_click(mouseX, mouseY)

    for button in app.file_buttons:
        button.handle_click(mouseX, mouseY)


def onMouseMove(app, mouseX, mouseY):
    for button in app.buttons:
        button.handle_hover(mouseX, mouseY)

    for button in app.file_buttons:
        button.handle_hover(mouseX, mouseY)


def onKeyPress(app, key):
    app.textarea.handle_key_press([key])

    # ast_rep = ASTHelper.get_ast_rep(Files.rebuild_content(app.textarea.content))
    # app.special_tokens = ASTHelper.load_ast_data(ast_rep)
    # print(app.special_tokens)


runApp(ConfigData.WINDOW_WIDTH, ConfigData.WINDOW_HEIGHT)
