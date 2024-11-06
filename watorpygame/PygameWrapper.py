
# standard imports
from typing import cast
from enum import Enum, StrEnum

# pygame imports
import pygame
from pygame.surface import Surface

# 'root' Wa-Tor imports
import ConfigField as cf

# 'wrapped in a folder' Wa-Tor imports
import watorpygame.ConfigFieldUser as cfu 
from watorpygame.DisplayState import DisplayState
from watorpygame.DisplayCommand import DisplayCommand

from watorpygame.WaTorColors import *

from watorpygame.IterationInfo import IterationInfo

from watorpygame.UserImage import UserImage
from watorpygame.UserImageInfo import UserImageInfo
from watorpygame.UserImageKey import UserImageKey
from watorpygame.UserImageProvider import UserImageProvider, Direction

from watorpygame.UserTextBox import UserTextBox
from watorpygame.UserButton import UserButton

from watorpygame.ConfigScreen import WaTorConfigScreen
from watorpygame.PlayScreen import WaTorPlayScreen



class PygameWrapper:

    #__________________________________________________________________________
    #
    # region __init__
    #__________________________________________________________________________
    def __init__(self, image_provider : UserImageProvider, callback_function):
        self.__image_provider = image_provider
        self.__callback_function = callback_function

        #______________________________________________________________________
        # Default window dimensions 
        self.__window_width = 1000  # defaut value
        self.__window_height = 800  # defaut value

        #______________________________________________________________________
        # Central definition of 
        # borders & buttons dimensions
        self.__border_length = 30
        self.__button_height = 50
        self.__button_width = 100

        self.__buttons = []
        self.__textboxes = []

        self.__state = DisplayState.OUT # will be set somewhere else anyway
        self.__data = {}

        self.__config_screen = WaTorConfigScreen(self.__image_provider)
        self.__play_screen = WaTorPlayScreen(self.__image_provider)
        
        self.__running = False
        self.__controls_need_initialization = True
        self.__screen = None
        self.__clock = None

        # self.max_time = 33 # value in milliseconds correspond to 3O Frame per second
        # self.current_time = 0

    #__________________________________________________________________________
    #
    # region __initialize_screen
    #__________________________________________________________________________
    def __initialize_screen(self):
        # pygame setup
        pygame.init()
        pygame.display.set_caption("wa - tor + pygame = wapygame ")

        #______________________________________________________________________
        # start the window on screen
        size = (self.__window_width, self.__window_height)
        self.__screen = pygame.display.set_mode(size)

        #______________________________________________________________________
        # The clock will be used used 
        # each time the tick(60) function will be called 
        self.__clock = pygame.time.Clock()
        self.__running = True

    #__________________________________________________________________________
    #
    # region __initialize_buttons
    #__________________________________________________________________________
    def __initialize_buttons(self, screen : pygame.Surface) :
        #______________________________________________________________________
        # Buttons need to be created after the creation of the screen

        self.__buttons = []
        commands = { }
        match self.__state :
            case DisplayState.CONF:
                commands = {
                    DisplayCommand.RESET : "Reset",
                    DisplayCommand.GO : "Go" }
                
            case DisplayState.BETWEEN: #only the call of UpdateView(world) make the state change
                commands = { }

            case DisplayState.WAIT :
                commands = {
                    DisplayCommand.START: "Start" }
            
            case DisplayState.PLAY :
                commands = {
                    DisplayCommand.PAUSE: "Pause", 
                    DisplayCommand.STOP: "Stop" }
            
            case DisplayState.PAUSE :
                commands = {
                    DisplayCommand.PAUSE: "Resume", 
                    DisplayCommand.STOP: "Stop" }

            case DisplayState.STOP :
                commands = {
                    DisplayCommand.RESTART: "Restart", 
                    DisplayCommand.EXIT: "Exit" }
            
            case _ :
                commands = { }
            
        count = len(commands)
        if count == 0 :
            return
        
        for command_key, command_text in commands.items():
            self.__buttons.append(
                UserButton( command_key, command_text, self.__callback_function,
                    pygame.Rect(
                        self.__window_width - count * (self.__button_width + self.__border_length),
                        self.__window_height - self.__button_height - self.__border_length,
                        self.__button_width,
                        self.__button_height)))
            count -= 1

    #__________________________________________________________________________
    #
    # region __initialize_textboxes
    #__________________________________________________________________________
    def __initialize_textboxes(self, screen : pygame.Surface) :
        
        self.__textboxes = []
        config_fields = cast(dict[cf.ConfigField, bool|int|float] , self.__data)
        if len(self.__data) == 0:
            return

        font = pygame.font.Font(None, 30)

        number_of_textboxes = len(config_fields)
        number_of_spaces = number_of_textboxes -1
        available_height = self.__window_height - 4 * self.__border_length - self.__button_height

        textbox_width = 150
        textbox_height = 0.80 * available_height / number_of_textboxes
        
        total_space = available_height - textbox_height * number_of_textboxes
        single_space = float(total_space)/number_of_spaces
        
        textbox_pos_x = self.__window_width - self.__border_length - textbox_width 
        textbox_pos_y = 2 * self.__border_length

        field_user = cfu.ConfigFieldTranslator()
        for field_key, field_value in config_fields.items() : 
            textbox = UserTextBox(field_key, 
                textbox_pos_x, int(textbox_pos_y), 
                textbox_width, int(textbox_height), 
                font, 
                str(field_value),
                field_user.get_validation_function(field_key))
            self.__textboxes.append(textbox)
            textbox_pos_y += textbox_height + single_space    

    #__________________________________________________________________________
    #
    # region __disable controls
    #__________________________________________________________________________
    def __disable_controls(self) :
        for button in self.__buttons :
            cast(UserButton, button).callback_function = None

        self.__buttons = []
        self.__play_screen.buttons = []
        self.__config_screen.buttons = []

        if len(self.__textboxes) ==0 :
            self.__controls_need_initialization = True
            return
        
        for textbox in self.__textboxes :
            cast(UserTextBox, textbox).callback_function = None

        self.__textboxes = []
        self.__config_screen.textboxes = []

        self.__controls_need_initialization = True

    #__________________________________________________________________________
    #
    # region __initialize_controls
    #__________________________________________________________________________
    def __initialize_controls(self, screen : pygame.Surface):
        #______________________________________________________________________
        # the buttons need a screen object to exist (because they are localized in screen) 
        # the textboxes need a font object which does not exist before pygame.init()

        if not self.__controls_need_initialization :
            return
        
        if self.__state in [DisplayState.BETWEEN, DisplayState.OUT] : 
            return

        if len(self.__textboxes) != 0 :
            self.__disable_controls()

        self.__screen = screen
        self.__initialize_buttons(self.__screen)
        if len(self.__buttons) == 0 :
            return

        #______________________________________________________________________
        # transfert to screens
        match self.__state :
            case DisplayState.CONF :  
                self.__initialize_textboxes(self.__screen) 
                if len(self.__textboxes) == 0 :
                    return

                self.__config_screen.initialize_controls(
                    self.__buttons,
                    self.__textboxes)
            case _ :
                self.__play_screen.initialize_controls(
                        self.__screen,
                        self.__border_length,
                        self.__buttons)

        # only when everythings is OK   
        self.__controls_need_initialization = False

    #__________________________________________________________________________
    #
    # region running
    #__________________________________________________________________________
    @property
    def running(self) :
        return self.__running
    
    #__________________________________________________________________________
    #
    # region stop_running
    #__________________________________________________________________________
    def stop_running(self) :
        self.__running = False


    #__________________________________________________________________________
    #
    # region set_state
    #__________________________________________________________________________
    def set_state(self, state : DisplayState) :
        if state is not self.__state :
            self.__disable_controls()
        
        self.__state = state

    #__________________________________________________________________________
    #
    # region set_data
    #__________________________________________________________________________
    def set_data(self, data_from_watordisplay) :
        if self.__state == DisplayState.CONF :
            self.__data = cast(dict, data_from_watordisplay )
            self.__config_screen.set_data(self.__data)
        else :
            self.__data = cast(list[list[UserImageInfo]], data_from_watordisplay)
            self.__play_screen.set_data(self.__data)

    #__________________________________________________________________________
    #
    # region set_iteration_info
    #__________________________________________________________________________
    def set_iteration_info(self, iterationInfo : IterationInfo) :
        self.__play_screen.set_iteration_info(iterationInfo)

    #__________________________________________________________________________
    #
    # region reset_config
    #__________________________________________________________________________
    def reset_config(self):
        self.__config_screen.reset_config() 

    #__________________________________________________________________________
    #
    # region get_config
    #__________________________________________________________________________
    def get_config(self) -> dict :
        return self.__config_screen.get_config() 
           
    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, display_state : DisplayState):
        
        if not self.__running:
            self.__initialize_screen()  # first time only, start screen
            
        if self.__controls_need_initialization :
            self.__initialize_controls(self.__screen) 

        # self.current_time = self.clock.tick() - self.current_time
        # if self.current_time < 100 :
        #     return         
                     

        state_before_events = self.__state 

        #__________________________________________________________________
        # poll for events 
        # pygame.QUIT event means the user clicked X to close your window
        #
        # HERE the DisplayState can change !!!!
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.__running = False

            for textbox in self.__textboxes :
                cast(UserTextBox, textbox).check_event(event)
            
            # Check for the mouse button down event
            for button in self.__buttons:
                cast(UserButton, button).check_event(event)

        
        if self.__state == state_before_events :
            #______________________________________________________________________
            # Call the draw method of the specific screen
            match self.__state :
                case DisplayState.CONF :   
                    self.__config_screen.draw(self.__screen, self.__border_length)

                case DisplayState.BETWEEN :     
                    pass
                
                case _ :  
                    self.__play_screen.draw(self.__screen, self.__border_length)
                
            #______________________________________________________________________
            # Wait for the next tick of the Clock

            self.__clock.tick(60)  # limits FPS to 60
                
        # _____________________________________________________________________
        # here stopped the old while true

        if not self.__running:
            self.__callback_function(DisplayCommand.EXIT)
            pygame.quit()

   
        
# if __name__ == "__main__":
#     #put unit tests here
#     pass