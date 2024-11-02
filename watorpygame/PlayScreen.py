# standard imports
from typing import cast
from enum import Enum

# pygame imports
import pygame
from pygame.surface import Surface

# Wa-Tor imports
from watorpygame.DisplayState import DisplayState
from watorpygame.UserImage import UserImage
from watorpygame.UserImageKey import UserImageKey
from watorpygame.UserImageProvider import UserImageProvider, Direction
from watorpygame.UserImageInfo import UserImageInfo
from watorpygame.UserLabel import UserLabel
from watorpygame.UserButton import UserButton

from watorpygame.IterationInfo import IterationInfo

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
        self.window_height = 0
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
    # region set_info
    #__________________________________________________________________________
    def set_info(self, iterationInfo : IterationInfo):

        self.iterationInfo = iterationInfo
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
        
        if len(self.data) == 0:
            return

        self.window_width = screen.get_width()
        self.window_height = screen.get_height()

        self.buttons = buttons
        button_heigth = buttons[0].button_rect.height

        #_______________________________________________________________________
        # Creation of the chessboard
        self.table_width = self.window_width - 2 * border_length
        self.table_heigth = self.window_height - button_heigth - 4 * border_length

        self.cell_width = (self.table_width) // self.data_width
        self.cell_heigth = (self.table_heigth) // self.data_height

        self.image_provider = UserImageProvider(self.cell_width, self.cell_heigth)
        
        #_______________________________________________________________________
        # Adapt image dimensions to the cells dimensions
        # ATTENTION ! - this part of code may cause strange bugs ;)
        # for image_key in [UserImageKey.FISH, UserImageKey.SHARK]:
        #     image = self.image_provider.get_image(image_key)
        #     image.define_dimensions(self.cell_width, self.cell_heigth)
        #     self.image_provider.set_image(image_key, image)
                
                        
        # for image_key in [UserImageKey.MEGA_HEAD, UserImageKey.MEGA_TAIL]:
        #     for x in range(0, 4):
        #         match x:
        #             case 0:
        #                 image = self.image_provider.get_image(image_key, Direction.NORTH)
        #             case 1:
        #                 image = self.image_provider.get_image(image_key, Direction.SOUTH)
        #             case 2:
        #                 image = self.image_provider.get_image(image_key, Direction.WEST)
        #             case 3:
        #                 image = self.image_provider.get_image(image_key, Direction.EAST)
                

    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, screen : pygame.Surface, border_length : int) :
        
        # fill the screen with a color to wipe away anything from last frame
        screen.fill(self.screen_background_color)

        center_x = screen.get_rect().centerx
        top_y = screen.get_rect().top

        # put the title
        label_writer = UserLabel()
        label_writer.draw(screen, "Wa - Tor : l'écran principal", center_x, top_y+20, 30, 0)

        label_writer.draw(screen, "Current iteration : {0}".format(self.iterationInfo.current_iteration), border_length, int(1.5*border_length), 20, -1)
        label_writer.draw(screen, 
            "Fish pop : {0} ; Shar pop : {1} ; Megalodon pop : {2}".format(
                self.iterationInfo.fish_pop,
                self.iterationInfo.shark_pop,
                self.iterationInfo.megalodon_pop), 
                border_length, 
                self.window_height - int(1.5*border_length) - self.buttons[0].button_rect.height, 
                20, -1)

        # RENDER YOUR GAME HERE
        for y_index in range(self.data_height):
            for x_index in range(self.data_width):

                position_x = border_length + x_index * self.cell_width
                position_y = 2*border_length + y_index * self.cell_heigth

                even_cell = (x_index + y_index) % 2 == 0
                image_key = cast(UserImageInfo, self.data[y_index][x_index]).image_key          

                #---------
                #Water drawing logic
                if image_key in [UserImageKey.WATER] :
                    cell_color = (0, 0, 170)
                    # UserImage.light_color if even_cell else UserImage.dark_color
                    pygame.draw.rect( screen, cell_color, [position_x, position_y, self.cell_width, self.cell_heigth] )
                    continue
                
                #---------
                #Fish drawing logic
                
                cell_rect = pygame.Rect( position_x, position_y, self.cell_width, self.cell_heigth )              
                
                if image_key in [UserImageKey.MEGA_HEAD, UserImageKey.MEGA_TAIL]:              
                    fish_image = self.image_provider.get_image(image_key, self.data[y_index][x_index].direction)
                    #Anchor the heads and tails to the right edge when upside down
                    match self.data[y_index][x_index].direction:
                        case Direction.NORTH:
                            if image_key == UserImageKey.MEGA_HEAD:
                                # Center the image horizontally, anchor at the bottom
                                x_image = cell_rect.centerx - (fish_image.resized.get_width() // 2)
                                y_image = cell_rect.bottom - fish_image.resized.get_height()  # Anchor at the bottom
                            
                            if image_key == UserImageKey.MEGA_TAIL:
                                # Center the image horizontally, anchor at the top
                                x_image = cell_rect.centerx - (fish_image.resized.get_width() // 2)
                                y_image = cell_rect.top  # Anchor at the top
                        case Direction.SOUTH:
                            if image_key == UserImageKey.MEGA_TAIL:
                                # Center the image horizontally, anchor at the bottom
                                x_image = cell_rect.centerx - (fish_image.resized.get_width() // 2)
                                y_image = cell_rect.bottom - fish_image.resized.get_height()  # Anchor at the bottom
                            
                            if image_key == UserImageKey.MEGA_HEAD:
                                # Center the image horizontally, anchor at the top
                                x_image = cell_rect.centerx - (fish_image.resized.get_width() // 2)
                                y_image = cell_rect.top  # Anchor at the top
                        case Direction.WEST:
                            if image_key == UserImageKey.MEGA_HEAD:
                                # Anchor at the right side, center vertically
                                x_image = cell_rect.right - fish_image.resized.get_width()  # Anchor at the right
                                y_image = cell_rect.centery - (fish_image.resized.get_height() // 2)
                            
                            if image_key == UserImageKey.MEGA_TAIL:
                                # Anchor at the left side, center vertically
                                x_image = cell_rect.left  # Anchor at the left
                                y_image = cell_rect.centery - (fish_image.resized.get_height() // 2)
                        case Direction.EAST:
                            if image_key == UserImageKey.MEGA_TAIL:
                                # Anchor at the right side, center vertically
                                x_image = cell_rect.right - fish_image.resized.get_width()  # Anchor at the right
                                y_image = cell_rect.centery - (fish_image.resized.get_height() // 2)
                            
                            if image_key == UserImageKey.MEGA_HEAD:
                                # Anchor at the left side, center vertically
                                x_image = cell_rect.left  # Anchor at the left
                                y_image = cell_rect.centery - (fish_image.resized.get_height() // 2)
                        case _:
                            center_x, center_y = cell_rect.center
                            # Calculate the top-left corner for blitting the image
                            x_image = center_x - (fish_image.resized.get_width() // 2)
                            y_image = center_y - (fish_image.resized.get_height() // 2)  
                        
                    
                else:
                    fish_image = self.image_provider.get_image(image_key)
                    #Fish and sharks are drawn in the center of their cell                    
                    # Center of the cell
                    center_x, center_y = cell_rect.center
                    # Calculate the top-left corner for blitting the image
                    x_image = center_x - (fish_image.resized.get_width() // 2)
                    y_image = center_y - (fish_image.resized.get_height() // 2)  
                                
                
                cell_color = fish_image.light_background_color if even_cell else fish_image.dark_background_color                
                
                pygame.draw.rect(screen, cell_color, cell_rect )   
                
                screen.blit(fish_image.resized, (x_image, y_image))

        for button in self.buttons:
            button.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        
# if __name__ == "__main__":
#     #put unit tests here
#     pass
        
