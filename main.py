from button.defined.terminaliconbutton import TerminalIconButton
from cmu_graphics import *

from button.defined.directoryiconbutton import DirectoryIconButton
from button.defined.filebutton import FileButton
from button.defined.folderbutton import FolderButton
from button.defined.iconbutton import IconButton
from button.defined.saveiconbutton import SaveIconButton
from button.defined.settingsiconbutton import SettingsIconButton
from common.colors import Colors
from common.config import ConfigData
from common.files import Files
from common.icons import Icons
from structures.textarea import TextArea

import os


def onAppStart(app):
    # config app
    app.stepsPerSecond = 10
    app.setMaxShapeCount(50000)

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

    app.textarea = TextArea(app, app.textarea_x, app.textarea_y, app.textarea_width, app.textarea_height)

    # other
    app.working_path = "."
    app.current_file = ""
    app.open_files = []
    app.buttons = [ 
        DirectoryIconButton(app, (app.sidebar_width / 2) - app.default_icon_width / 2, 10, Icons.FILE),
        SaveIconButton(app, (app.sidebar_width / 2) - app.default_icon_width / 2, 55, Icons.SAVE),
        TerminalIconButton(app, (app.sidebar_width - app.default_icon_width) / 2,
                           app.height - (app.default_icon_width * 1.5) * 2,
                           Icons.TERMINAL),
        SettingsIconButton(app, (app.sidebar_width - app.default_icon_width) / 2, app.height - app.default_icon_width * 1.5,
                   Icons.SETTINGS),
    ]
    app.file_buttons = []
    app.special_tokens = {"func": set(), "var": set()}
    app.stepsSinceKeyPressed = 0
    app.code_is_invalid = False

    clean_ls = [file for file in os.listdir(app.working_path) if not file.startswith(".")]
    try:
        for i, file in enumerate(clean_ls):
            if os.path.isfile(file):
                app.file_buttons.append(FileButton(app, app.sidebar_width + 18, 40 + 25 * i, app.file_structure_width * 0.6,
                                                f" {file}", app.background_color))
                continue
            app.file_buttons.append(FolderButton(app, app.sidebar_width + 18, 40 + 25 * i, app.file_structure_width * 0.6,
                                                f"> {file}", app.background_color))
    except:
        return


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

    # drawing current line rectangle
    cmu_graphics.drawRect(
        app.file_structure_width,
        app.top_bar_height + selector_location_y * 20 + 10,
        app.width - app.file_structure_width,
        20,
        fill="gray",
        opacity=5,
        border="gray",
        borderWidth=1
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

    for button in app.open_files:
        button.draw()


def onMousePress(app, mouseX, mouseY):
    app.textarea.handle_click(app, mouseX, mouseY)

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
    app.stepsSinceKeyPressed = 0
    app.textarea.handle_key_press([key])


def onKeyRelease(app, key):
    app.stepsSinceKeyPressed = 0


def onKeyHold(app, keys, modifiers):
    if app.stepsSinceKeyPressed < app.stepsPerSecond * 1.1:
        return

    app.textarea.handle_key_press(keys)


def onStep(app):
    app.stepsSinceKeyPressed += 1


runApp(ConfigData.WINDOW_WIDTH, ConfigData.WINDOW_HEIGHT)
