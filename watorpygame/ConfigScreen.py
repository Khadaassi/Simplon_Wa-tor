
# no standard imports
# pygame imports
import pygame

# 'root' Wa-Tor imports
from ConfigField import ConfigField

# 'wrapped in a folder' Wa-Tor imports
from watorpygame.ConfigFieldUser import ConfigFieldTranslator
from watorpygame.WaTorColors import WaTorColors, ColorChoice

from watorpygame.UserImage import UserImage
from watorpygame.UserImageInfo import UserImageInfo
from watorpygame.UserImageKey import UserImageKey
from watorpygame.UserImageProvider import UserImageProvider

from watorpygame.UserLabel import UserLabel
from watorpygame.UserButton import UserButton
from watorpygame.UserTextBox import UserTextBox


class WaTorConfigScreen :

    #__________________________________________________________________________
    #
    # region __init__
    #__________________________________________________________________________
    def __init__(self, image_provider: UserImageProvider ) :

        self.__image_provider = image_provider
       
        self.__config_file_memory = {}
        self.__in_data = {}
        self.__out_data = {}

        self.buttons = []
        self.textboxes = []

        self.__too_many_entities_fields = [
            ConfigField.FISH_POPULATION,
            ConfigField.SHARK_POPULATION,
            ConfigField.WORLD_WIDTH,
            ConfigField.WORLD_HEIGTH
        ]
        self.__too_many_entities = False

    #__________________________________________________________________________
    #
    # region __on_textbox_validating
    #__________________________________________________________________________
    def __on_textbox_validation(self, field_key: ConfigField) :
        for textbox in self.textboxes :
            if textbox.field_key == field_key :
                typed_value = textbox.get_validated_value()
                self.__out_data[field_key] = typed_value              
                break

        if field_key in self.__too_many_entities_fields :
            self.__check_nb_entities()

    #__________________________________________________________________________
    #
    # region __validate_textboxes
    #__________________________________________________________________________
    def __validate_textboxes(self) -> bool :
        for textbox in self.textboxes :
            if textbox.validate() :
                self.__out_data[textbox.field_key] = textbox.get_validated_value()
            else : 
                return False

        return self.__check_nb_entities() 
    
    #__________________________________________________________________________
    #
    # region __check nb entities
    #__________________________________________________________________________
    def __check_nb_entities(self)-> bool:
        """
        return True if the values in textboxes check thah condition :
        nb_fish + nb_shark <= world_width * world_height 
        """
        nb_fish = 1
        nb_shark = 1
        world_width = 1
        world_height = 1
        nb_pacman = 0
        for field in ConfigField:
            match field :
                case ConfigField.FISH_POPULATION : nb_fish = self.__out_data[ConfigField.FISH_POPULATION]
                case ConfigField.SHARK_POPULATION : nb_shark = self.__out_data[ConfigField.SHARK_POPULATION]
                case ConfigField.WORLD_WIDTH : world_width = self.__out_data[ConfigField.WORLD_WIDTH]
                case ConfigField.WORLD_HEIGTH : world_height = self.__out_data[ConfigField.WORLD_HEIGTH]
                case ConfigField.ALLOW_PACMAN : 
                    if self.__out_data[ConfigField.ALLOW_PACMAN] :
                        nb_pacman = 1
                case _ : pass

        if nb_fish + nb_shark + nb_pacman > world_width * world_height :
            self.__too_many_entities = True
        else :            self.__too_many_entities = False
            
        return not self.__too_many_entities

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
            textbox.register_callback_function(self.__on_textbox_validation)

    #__________________________________________________________________________
    #
    # region set_data
    #__________________________________________________________________________
    def set_data(self, data : dict) :
        self.__in_data = data

        if self.__config_file_memory == {} :
            self.__config_file_memory = self.__in_data.copy()

        if self.__out_data == {} :
            self.__out_data = self.__in_data.copy()

    #__________________________________________________________________________
    #
    # region reset_config
    #__________________________________________________________________________
    def reset_config(self) :
        self.__out_data = self.__config_file_memory.copy()
        for textbox in self.textboxes :
            field_value = str(self.__out_data[textbox.field_key])
            textbox.reset_text(field_value)

        self.__too_many_entities = False

    #__________________________________________________________________________
    #
    # region get_config
    #__________________________________________________________________________
    def get_config(self) -> dict :
        """
        That function has to be called when textboxes exist : before to quit the config screen
        """
        if len(self.textboxes) == 0 : 
            return {}

        if self.__validate_textboxes() :
            config_data = self.__out_data.copy()
        else : 
            config_data = self.__in_data
        
        self.__out_data = {}

        return config_data
    

    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, screen : pygame.Surface, border_length : int) :

        colors = WaTorColors()
      
        # fill the screen with a color to wipe away anything from last frame
        screen.fill(colors.get(ColorChoice.SCREEN_BACKGROUND_COLOR))

        window_rect = screen.get_rect()
        window_width = window_rect.width
        window_height = window_rect.height
        center_x = window_rect.centerx
        top_y = window_rect.top 

        label_writer = UserLabel()
        label_writer.draw(screen, "Wa - Tor : l'écran de configuration", center_x, top_y +20, 40, 0)

        project_image = self.__image_provider.get_image(UserImageKey.PROJECT)

        button_height = self.buttons[0].button_rect.height
    
        image_width = window_width-2*border_length
        image_height = window_height - 4* border_length - button_height
            
        transformed = pygame.transform.scale(project_image.image, (image_width + 10, image_height + 10))
        screen.blit(transformed, (border_length - 5, 2*border_length - 5) )

        if not self.__check_nb_entities() :
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

        field_translator = ConfigFieldTranslator()
        for textbox in self.textboxes :
            rect = textbox.get_rect()
            label_writer.front_color = colors.get(ColorChoice.FIELD_FRONT_LABEL)
            label_writer.back_color = colors.get(ColorChoice.FIELD_BACK_LABEL)
            label_writer.draw(screen, 
                "{0} :".format(field_translator.get_label_text(textbox.field_key)), 
                rect.left-10, 
                rect.centery, 30, 1, True)
            textbox.draw(screen)

        for button in self.buttons:
            button.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()
