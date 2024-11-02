import pygame
from enum import Enum

class ColorChoice(Enum) :
    SCREEN_BACKGROUND_COLOR = 0
    TEXTBOX_INACTIVE = 1
    TEXTBOX_INVALID = 2
    TEXTBOX_ACTIVE = 3
    FRONT_LABEL = 4
    BACK_LABEL = 5

class WaTorColors :
    def __init__(self) :
        self.__colors = {
            ColorChoice.SCREEN_BACKGROUND_COLOR : pygame.Color("darkgray"),
            ColorChoice.TEXTBOX_INACTIVE : pygame.Color((0, 0, 255)),
            ColorChoice.TEXTBOX_ACTIVE : pygame.Color((128, 255, 0)),
            ColorChoice.TEXTBOX_INVALID :pygame.Color((192, 64, 64)),
            ColorChoice.FRONT_LABEL : pygame.Color((0, 0, 200)), 
            ColorChoice.BACK_LABEL : pygame.Color((100, 100, 100))}
        
    def get(self, choice: ColorChoice) -> pygame.color.Color :
        return self.__colors[choice]


