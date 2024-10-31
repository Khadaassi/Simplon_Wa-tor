from pygame.color import Color
from enum import Enum

class ColorChoice(Enum) :
    SCREEN_BACKGROUND_COLOR = 0
    TEXTBOX_INACTIVE = 1
    TEXTBOX_INVALID = 2
    TEXTBOX_ACTIVE = 3

class WaTorColors :
    def __init__(self) :
        self.colors = {
            ColorChoice.SCREEN_BACKGROUND_COLOR : Color("darkgray"),
            ColorChoice.TEXTBOX_INACTIVE : Color((128, 0, 128)),
            ColorChoice.TEXTBOX_ACTIVE : Color((128, 255, 0)),
            ColorChoice.TEXTBOX_INVALID :Color((192, 64, 64))}
