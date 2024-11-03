
import pygame

from watorpygame.UserButton import UserButton
from watorpygame.UserImage import UserImage
from watorpygame.UserImageInfo import UserImageInfo
from watorpygame.UserImageKey import UserImageKey
from watorpygame.UserImageProvider import UserImageProvider
from watorpygame.UserLabel import UserLabel
from watorpygame.UserTextBox import UserTextBox
from watorpygame.ConfigField import ConfigField

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
        self.window_height = 0
        self.buttons = []
        self.textboxes = []

    #__________________________________________________________________________
    #
    # region set_data
    #__________________________________________________________________________
    def set_data(self, data : dict) :
        self.in_data = data
        self.out_data = self.in_data

    #__________________________________________________________________________
    #
    # region reset_config
    #__________________________________________________________________________
    def reset_config(self) :
        self.out_data = self.in_data
        for textbox in self.textboxes :
            field_value = self.out_data[textbox.field_key]
            textbox.reset_text(field_value)

    #__________________________________________________________________________
    #
    # region validate
    #__________________________________________________________________________
    def validate(self) -> bool :
        validated = True
        for textbox in self.textboxes :
            if not textbox.validate() :
                validated = False
                break

        return validated 

    #__________________________________________________________________________
    #
    # region get_config
    #__________________________________________________________________________
    def get_config(self) -> dict :
        if self.validate() :
            selected_data = self.out_data 
        else : 
            selected_data = self.in_data

        return selected_data
    
    #__________________________________________________________________________
    #
    # region initialize_controls
    #__________________________________________________________________________
    def initialize_controls(self, screen : pygame.Surface, border_length: int, buttons : list[UserButton], textboxes : list[UserTextBox]):
        """
        need number of config fields to initialize screen dimensions
        """
        if self.window_width != 0 : 
            return 

        self.window_width = screen.get_width()
        self.window_height = screen.get_height()

        self.buttons = buttons
        self.textboxes = textboxes
        for textbox in self.textboxes :
            textbox.register_validation_function(self.on_textbox_validated)

    #__________________________________________________________________________
    #
    # region on_textbox_validated
    #__________________________________________________________________________
    def on_textbox_validated(self, field_key: ConfigField) :
        for textbox in self.textboxes :
            if textbox.field_key == field_key :
                val = textbox.get_validated_value()
                self.out_data[field_key] = val

    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, screen : pygame.Surface, border_length : int) :

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(self.screen_background_color)

        center_x = screen.get_rect().centerx
        top_y = screen.get_rect().top 

        label_writer = UserLabel()
        label_writer.draw(screen, "Wa - Tor : l'écran de configuration", center_x, top_y +20, 40, 0)

        project_image = self.image_provider.get_image(UserImageKey.PROJECT)
    
        image_width = self.window_width-2*border_length
        image_height = self.window_height - 4* border_length - self.buttons[0].button_rect.height
        surface = pygame.Surface((image_width, image_height))
            
        transformed = pygame.transform.scale(project_image.image, (image_width, image_height), surface)

        # project_image.define_dimensions(self.window_width, self.window_height)
        # converted_rect = project_image.resized.convert()

        screen.blit(transformed, (border_length, 2*border_length) )

        #for key, textbox in self.textboxes.items 
        #for line_of_data in self.data :

        for textbox in self.textboxes :
            rect = textbox.get_rect()
            label_writer.draw(screen, "{0} :".format(textbox.field_key.value), rect.left-10, rect.centery, 40, 1, True)
            textbox.draw(screen)

        for button in self.buttons:
            button.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()
