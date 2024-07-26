from cmu_graphics import *
import enum
from PIL import Image


# All images were obtained from: https://www.flaticon.com/

class Icons:

    IMG_PATH = "./images/"

    TERMINAL = CMUImage(Image.open(IMG_PATH + "terminal.png"))
    FILE = CMUImage(Image.open(IMG_PATH + "open-folder.png"))
    SETTINGS = CMUImage(Image.open(IMG_PATH + "cogwheel.png"))
    INFO = CMUImage(Image.open(IMG_PATH + "info.png"))
    RUN = CMUImage(Image.open(IMG_PATH + "right-arrow.png"))

    def draw(icon, x, y):
        cmu_graphics.drawImage(icon, x, y, height=30, width=30)
