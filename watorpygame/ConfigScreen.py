
import pygame

from watorpygame.UserButton import UserButton
from watorpygame.UserImage import UserImage
from watorpygame.UserImageInfo import UserImageInfo
from watorpygame.UserImageKey import UserImageKey
from watorpygame.UserImageProvider import UserImageProvider
from watorpygame.UserLabel import UserLabel
from watorpygame.WaTorColors import WaTorColors, ColorChoice

from watorpygame.UserTextBox import UserTextBox
from ConfigField import ConfigField
from watorpygame.ConfigFieldUser import ConfigFieldUser

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

        self.buttons = []
        self.textboxes = []

        self.too_many_entities_fields = [
            ConfigField.FISH_POPULATION,
            ConfigField.SHARK_POPULATION,
            ConfigField.WORLD_WIDTH,
            ConfigField.WORLD_HEIGTH
        ]
        self.too_many_entities = False

    #__________________________________________________________________________
    #
    # region set_data
    #__________________________________________________________________________
    def set_data(self, data : dict) :
        self.in_data = data
        self.out_data = self.in_data.copy()

    #__________________________________________________________________________
    #
    # region reset_config
    #__________________________________________________________________________
    def reset_config(self) :
        self.out_data = self.in_data.copy()
        for textbox in self.textboxes :
            field_value = self.out_data[textbox.field_key]
            textbox.reset_text(field_value)

        self.too_many_entities = False

    #__________________________________________________________________________
    #
    # region validate_all
    #__________________________________________________________________________
    def validate_all(self) -> bool :
        validated = True
        for textbox in self.textboxes :
            if not textbox.validate() :
                validated = False
                break

        if not validated :
            return False

        return self.check_nb_entities() 
    #__________________________________________________________________________
    #
    # region check nb entities
    #__________________________________________________________________________
    def check_nb_entities(self)-> bool:
        """
        return True if the values in textboxes check thah condition :
        nb_fish + nb_shark <= world_width * world_height 
        """
        nb_fish = 0
        nb_shark = 0  
        world_width = 0
        world_height = 0
        for textbox in self.textboxes :
            match textbox.field_key :
                case ConfigField.FISH_POPULATION : nb_fish = self.out_data[ConfigField.FISH_POPULATION]
                case ConfigField.SHARK_POPULATION : nb_shark = self.out_data[ConfigField.SHARK_POPULATION]
                case ConfigField.WORLD_WIDTH : world_width = self.out_data[ConfigField.WORLD_WIDTH]
                case ConfigField.WORLD_HEIGTH : world_height = self.out_data[ConfigField.WORLD_HEIGTH]

        if nb_fish + nb_shark > world_width * world_height :
            self.too_many_entities = True
            return False
        
        self.too_many_entities = False
        return True

    #__________________________________________________________________________
    #
    # region get_config
    #__________________________________________________________________________
    def get_config(self) -> dict :
        if self.validate_all() :
            selected_data = self.out_data 
        else : 
            selected_data = self.in_data

        return selected_data
    
    #__________________________________________________________________________
    #
    # region initialize_controls
    #__________________________________________________________________________
    def initialize_controls(self, buttons : list[UserButton], textboxes : list[UserTextBox]):
        """
        need number of config fields to initialize screen dimensions
        """

        self.buttons = buttons
        self.textboxes = textboxes
        for textbox in self.textboxes :
            textbox.register_validation_function(self.on_textbox_validated)

    #__________________________________________________________________________
    #
    # region on_textbox_validated
    #__________________________________________________________________________
    def on_textbox_validated(self, field_key: ConfigField) :
        found = False
        for textbox in self.textboxes :
            if found : 
                break

            if textbox.field_key == field_key :
                found = True
                val = textbox.get_validated_value()
                self.out_data[field_key] = val              
                if textbox.field_key in self.too_many_entities_fields :
                    self.check_nb_entities()

    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, screen : pygame.Surface, border_length : int) :

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(self.screen_background_color)
        window_rect = screen.get_rect()
        window_width = window_rect.width
        window_height = window_rect.height
        center_x = window_rect.centerx
        top_y = window_rect.top 

        label_writer = UserLabel()
        label_writer.draw(screen, "Wa - Tor : l'écran de configuration", center_x, top_y +20, 40, 0)

        project_image = self.image_provider.get_image(UserImageKey.PROJECT)

        button_height = self.buttons[0].button_rect.height
    
        image_width = window_width-2*border_length
        image_height = window_height - 4* border_length - button_height
        surface = pygame.Surface((image_width, image_height))
            
        transformed = pygame.transform.scale(project_image.image, (image_width, image_height), surface)

        # project_image.define_dimensions(self.window_width, self.window_height)
        # converted_rect = project_image.resized.convert()

        screen.blit(transformed, (border_length, 2*border_length) )

        colors = WaTorColors()
        if not self.check_nb_entities() :
            error_label_writer = UserLabel()
            error_label_writer.front_color = colors.get(ColorChoice.ERROR_FRONT_LABEL)
            error_label_writer.back_color = colors.get(ColorChoice.ERROR_BACK_LABEL)
            error_label_writer.draw(screen, 
                "Trop de poissons et de requins pour la taille du monde.", 
                2* border_length, 
                window_height- button_height - int(1.5*border_length),30, -1, True)
            error_label_writer.draw(screen, 
                "Si vous continuez, la configuration par défaut sera utilisée.", 
                3* border_length, 
                window_height- button_height - int(0.5*border_length),25, -1, True)

        field_user = ConfigFieldUser()
        for textbox in self.textboxes :
            rect = textbox.get_rect()
            label_writer.front_color = colors.get(ColorChoice.FIELD_FRONT_LABEL)
            label_writer.back_color = colors.get(ColorChoice.FIELD_BACK_LABEL)
            label_writer.draw(screen, 
                "{0} :".format(field_user.get_label_text(textbox.field_key)), 
                rect.left-10, 
                rect.centery, 30, 1, True)
            textbox.draw(screen)

        for button in self.buttons:
            button.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()
