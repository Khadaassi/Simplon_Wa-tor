
import pygame

from watorpygame.UserButton import UserButton
from watorpygame.UserImage import UserImage
from watorpygame.UserImageInfo import UserImageInfo
from watorpygame.UserImageProvider import UserImageKey, UserImageProvider
from watorpygame.UserLabel import UserLabel

class WaTorConfigScreen :

    #__________________________________________________________________________
    #
    # region __init__
    #__________________________________________________________________________
    def __init__(self, screen_background_color, image_provider: UserImageProvider ) :

        self.screen_background_color = screen_background_color
        self.image_provider = image_provider
       
        self.in_data = {}
        self.out_data = {}

        self.window_width = 0
        self.window_heigth = 0
        self.buttons = []


    def set_data(self, data : dict) :
        self.in_data = data
        self.out_data = self.in_data

    def get_conf(self) -> dict :
        return self.out_data
    
    #__________________________________________________________________________
    #
    # region initialize_controls
    #__________________________________________________________________________
    def initialize_controls(self, screen : pygame.Surface, border_length: int, buttons : list[UserButton]):
        """
        need number of config fields to initialize screen dimensions
        """
        if self.window_width != 0 : 
            return 

        self.window_width = screen.get_width()
        self.window_heigth = screen.get_height()

        self.buttons = buttons

    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, screen : pygame.Surface, border_length : int) :

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(self.screen_background_color)

        center_x = screen.get_rect().centerx
        top_y = screen.get_rect().top + 25

        label_writer = UserLabel()
        label_writer.draw(screen, "WA TOR - Ecran de configuration", center_x, top_y, 30, 0)

        #for line_of_data in self.data :

        for button in self.buttons:
            button.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()
