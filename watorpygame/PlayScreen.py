# standard imports
from typing import cast
from enum import Enum

# pygame imports
import pygame
from pygame.surface import Surface

# Wa-Tor imports
from watorpygame.DisplayState import DisplayState
from watorpygame.UserImage import UserImage
from watorpygame.UserButton import UserButton
from watorpygame.UserImageProvider import UserImageKey, UserImageProvider

class WaTorPlayScreen :
    #__________________________________________________________________________
    #
    # region __init__
    #__________________________________________________________________________
    def __init__(self, screen_background_color, image_provider: UserImageProvider ) :

        self.screen_background_color = screen_background_color
        self.image_provider = image_provider
       
        self.data = []
        self.data_height = 0
        self.data_width = 0

        self.window_width = 0
        self.window_heigth = 0
        self.table_width = 0
        self.table_heigth = 0
        self.cell_width =0
        self.cell_heigth = 0
    
    #__________________________________________________________________________
    #
    # region set_data
    #__________________________________________________________________________
    def set_data(self, data: list[list]):
        #______________________________________________________________________
        # about format informations :
        #    data_height corresponds to the number of lines in the matrix 
        #    data_width corresponds to the number of columns in the matrix 
        self.data = data
        self.data_height = len(self.data)
        self.data_width = len(self.data[0])
    
    #__________________________________________________________________________
    #
    # region initialize_controls
    #__________________________________________________________________________
    def initialize_controls(self, screen : pygame.Surface, border_length: int, buttons : list[UserButton]):
        """
        Need the data dimensions to create the chessboard
        """
        if self.window_width != 0 : 
            return 

        self.window_width = screen.get_width()
        self.window_heigth = screen.get_height()

        self.buttons = buttons
        button_heigth = buttons[0].button_rect.height

        #_______________________________________________________________________
        # Creation of the chessboard
        self.table_width = self.window_width - 2 * border_length
        self.table_heigth = self.window_heigth - button_heigth - 3 * border_length

        self.cell_width = (self.table_width) // self.data_width
        self.cell_heigth = (self.table_heigth) // self.data_height
 
        #_______________________________________________________________________
        # Adapt image dimensions to the cells dimensions
        # ATTENTION ! - this part of code may cause etrange bugs ;)
        for image_key in [UserImageKey.FISH, UserImageKey.SHARK]:
            image = self.image_provider.get_image(image_key)
            image.define_dimensions(self.cell_width, self.cell_heigth)
            self.image_provider.set_image(image_key, image)

    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, screen : pygame.Surface, border_length : int) :
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill(self.screen_background_color)

        # RENDER YOUR GAME HERE
        for y_index in range(self.data_height):
            for x_index in range(self.data_width):

                position_x = border_length + x_index * self.cell_width
                position_y = border_length + y_index * self.cell_heigth

                even_cell = (x_index + y_index) % 2 == 0
                image_key = self.data[y_index][x_index]

                if image_key in [UserImageKey.WATER, UserImageKey.MEGA_HEAD, UserImageKey.MEGA_TAIL] :
                    cell_color = UserImage.light_color if even_cell else UserImage.dark_color
                    pygame.draw.rect( screen, cell_color, [position_x, position_y, self.cell_width, self.cell_heigth] )
                    continue

                fish_image = self.image_provider.get_image(image_key)
                cell_color = fish_image.light_background_color if even_cell else fish_image.dark_background_color
                pygame.draw.rect( screen, cell_color, [position_x, position_y, self.cell_width, self.cell_heigth] )
                    
                x_image = border_length + x_index * self.cell_width
                y_image = border_length + y_index * self.cell_heigth

                screen.blit(fish_image.resized, (x_image, y_image))

        for button in self.buttons:
            button.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        

        
