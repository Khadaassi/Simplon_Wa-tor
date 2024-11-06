import pygame
from enum import Enum

class ColorChoice(Enum) :
    SCREEN_BACKGROUND_COLOR = 0
    TEXTBOX_INACTIVE = 1
    TEXTBOX_INVALID = 2
    TEXTBOX_ACTIVE = 3
    DEFAULT_FRONT_LABEL = 4
    DEFAULT_BACK_LABEL = 5
    FIELD_FRONT_LABEL = 6
    FIELD_BACK_LABEL = 7
    ERROR_FRONT_LABEL = 8
    ERROR_BACK_LABEL = 9
    CELL_EMPTY_WATER = 10


class WaTorColors :
    def __init__(self) :
        self.__colors = {
            ColorChoice.SCREEN_BACKGROUND_COLOR : pygame.Color("darkgray"),
            ColorChoice.TEXTBOX_INACTIVE : pygame.Color((0, 0, 255)),
            ColorChoice.TEXTBOX_ACTIVE : pygame.Color((128, 255, 0)),
            ColorChoice.TEXTBOX_INVALID :pygame.Color((192, 64, 64)),
            ColorChoice.DEFAULT_FRONT_LABEL : pygame.Color((0, 0, 200)),
            ColorChoice.DEFAULT_BACK_LABEL : pygame.Color("white"),
            ColorChoice.FIELD_FRONT_LABEL : pygame.Color("black"),
            ColorChoice.FIELD_BACK_LABEL : pygame.Color((0, 0, 200)), 
            ColorChoice.ERROR_FRONT_LABEL : pygame.Color("red"),
            ColorChoice.ERROR_BACK_LABEL : pygame.Color("black"), 
            ColorChoice.CELL_EMPTY_WATER : pygame.Color(0, 0, 170)}
        
    def get(self, choice: ColorChoice) -> pygame.color.Color :
        return self.__colors[choice]


