
# standard imports
from typing import cast
from enum import Enum

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
        self.image_provider = image_provider
        self.callback_function = callback_function

        #______________________________________________________________________
        # Default window dimensions 
        self.window_width = 1000  # defaut value
        self.window_height = 700  # defaut value

        #______________________________________________________________________
        # Central definition of 
        # borders & buttons dimensions
        self.border_length = 30
        self.button_height = 50
        self.button_width = 100

        self.buttons = []
        self.textboxes = []
        self.state = DisplayState.CONF

        background_color = WaTorColors().get(ColorChoice.SCREEN_BACKGROUND_COLOR)

        self.config_screen = WaTorConfigScreen(background_color, self.image_provider)
        self.play_screen = WaTorPlayScreen(background_color, self.image_provider)
        
        self.running = False
        self.controls_need_initialization = True
        self.screen = None
        self.clock = None

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
        size = (self.window_width, self.window_height)
        self.screen = pygame.display.set_mode(size)

        #______________________________________________________________________
        # The clock will be used used 
        # each time the tick(60) function will be called 
        self.clock = pygame.time.Clock()
        self.running = True

    #__________________________________________________________________________
    #
    # region __initialize_buttons
    #__________________________________________________________________________
    def __initialize_buttons(self, screen : pygame.Surface) :
        #______________________________________________________________________
        # Buttons need to be created after the creation of the screen

        screen_rect = screen.get_rect()
        window_width = screen_rect.width
        window_height = screen_rect.height

        self.buttons = []
        match self.state :
            case DisplayState.CONF:
                self.commands = {
                    DisplayCommand.RESET : "Reset",
                    DisplayCommand.GO : "Go" }
                
            case DisplayState.BETWEEN: #only the call of UpdateView(world) make the state change
                self.commands = { }

            case DisplayState.WAIT :
                self.commands = {
                    DisplayCommand.START: "Start" }
            
            case DisplayState.PLAY :
                self.commands = {
                    #DisplayCommand.STEP : "Step", # not implemented feature
                    DisplayCommand.PAUSE: "Pause", 
                    DisplayCommand.STOP: "Stop" }
            
            case DisplayState.PAUSE :
                self.commands = {
                    #DisplayCommand.STEP : "Step", # not implemented feature
                    DisplayCommand.PAUSE: "Resume", 
                    DisplayCommand.STOP: "Stop" }

            case DisplayState.STOP :
                self.commands = {
                    DisplayCommand.RESTART: "Restart", 
                    DisplayCommand.EXIT: "Exit" }
            
            case _ :
                self.commands = { }
            
        count = len(self.commands)
        if count == 0 :
            return
        
        for command_key, command_text in self.commands.items():
            self.buttons.append(
                UserButton( command_key, command_text, self.callback_function,
                    pygame.Rect(
                        window_width - count * (self.button_width + self.border_length),
                        window_height - self.button_height - self.border_length,
                        self.button_width,
                        self.button_height)))
            count -= 1

    #__________________________________________________________________________
    #
    # region __initialize_textboxes
    #__________________________________________________________________________
    def __initialize_textboxes(self, screen : pygame.Surface) :
        
        self.textboxes = []
        config_fields = self.data
        if len(self.data) == 0:
            return
        
        screen_rect = screen.get_rect()
        window_width = screen_rect.width
        window_height = screen_rect.height

        font = pygame.font.Font(None, 30)

        number_of_textboxes = len(config_fields)
        number_of_spaces = number_of_textboxes -1
        available_height = window_height - 4 * self.border_length - self.button_height

        textbox_width = 150
        textbox_height = 0.80 * available_height / number_of_textboxes
        
        total_space = available_height - textbox_height * number_of_textboxes
        single_space = float(total_space)/number_of_spaces
        
        textbox_pos_x = window_width - self.border_length - textbox_width 
        textbox_pos_y = 2 * self.border_length

        field_user = cfu.ConfigFieldUser()
        for field_key, field_value in config_fields.items() : 
            textbox = UserTextBox(field_key, 
                textbox_pos_x, int(textbox_pos_y), 
                textbox_width, int(textbox_height), 
                font, 
                str(field_value),
                field_user.get_validation_function(field_key))
            self.textboxes.append(textbox)
            textbox_pos_y += textbox_height + single_space    

    #__________________________________________________________________________
    #
    # region __disable controls
    #__________________________________________________________________________
    def __disable_controls(self) :
        for button in self.buttons :
            cast(UserButton, button).callback_function = None

            self.buttons = []
            self.play_screen.buttons = []
            self.config_screen.buttons = []

        if len(self.textboxes) ==0 :
            self.controls_need_initialization = True
            return
        
        for textbox in self.textboxes :
            cast(UserTextBox, textbox).callback_function = None

            self.textboxes = []
            self.config_screen.textboxes = []

        self.controls_need_initialization = True

    #__________________________________________________________________________
    #
    # region initialize_controls
    #__________________________________________________________________________
    def initialize_controls(self, screen : pygame.Surface):
        #______________________________________________________________________
        # the buttons need a screen object to exist (because they are localized in screen) 
        # the textboxes need a font object which does not exist before pygame.init()

        if not self.controls_need_initialization :
            return
        
        if self.state in [DisplayState.BETWEEN, DisplayState.OUT] : 
            return

        if len(self.textboxes) != 0 :
            self.__disable_controls()

        self.screen = screen
        self.__initialize_buttons(self.screen)
        if len(self.buttons) == 0 :
            return

        #______________________________________________________________________
        # transfert to screens
        match self.state :
            case DisplayState.CONF :  
                self.__initialize_textboxes(self.screen) 
                if len(self.textboxes) == 0 :
                    return

                self.config_screen.initialize_controls(
                    self.buttons,
                    self.textboxes)
            case _ :
                self.play_screen.initialize_controls(
                        self.screen,
                        self.border_length,
                        self.buttons)

        # only when everythings is OK   
        self.controls_need_initialization = False

    #__________________________________________________________________________
    #
    # region set_state
    #__________________________________________________________________________
    def set_state(self, state : DisplayState) :
        if state is not self.state :
            self.__disable_controls()
        
        self.state = state

    #__________________________________________________________________________
    #
    # region set_data
    #__________________________________________________________________________
    def set_data(self, data) :
        if self.state == DisplayState.CONF :
            self.data = cast(dict, data )
            self.config_screen.set_data(self.data)
        else :
            self.data = cast(list[list[UserImageInfo]], data)
            self.play_screen.set_data(self.data)

    #__________________________________________________________________________
    #
    # region set_iteration_info
    #__________________________________________________________________________
    def set_iteration_info(self, iterationInfo : IterationInfo) :
        self.play_screen.set_iteration_info(iterationInfo)

    #__________________________________________________________________________
    #
    # region reset_config
    #__________________________________________________________________________
    def reset_config(self):
        self.config_screen.reset_config() 

    #__________________________________________________________________________
    #
    # region get_config
    #__________________________________________________________________________
    def get_config(self) -> dict :
        return self.config_screen.get_config() 
     
           
    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, display_state : DisplayState):
        
        if not self.running:
            self.__initialize_screen()  # first time only, start screen
            
        if self.controls_need_initialization :
            self.initialize_controls(self.screen) 

        # self.current_time = self.clock.tick() - self.current_time
        # if self.current_time < 100 :
        #     return         
                     

        state_before_events = self.state 

        #__________________________________________________________________
        # poll for events 
        # pygame.QUIT event means the user clicked X to close your window
        #
        # HERE the DisplayState can change !!!!
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            for textbox in self.textboxes :
                cast(UserTextBox, textbox).check_event(event)
            
            # Check for the mouse button down event
            for button in self.buttons:
                cast(UserButton, button).check_event(event)

        
        if self.state == state_before_events :
            #______________________________________________________________________
            # Call the draw method of the specific screen
            match self.state :
                case DisplayState.CONF :   
                    self.config_screen.draw(self.screen, self.border_length)

                case DisplayState.BETWEEN :     
                    pass
                
                case _ :  
                    if len(self.buttons) != 0 :
                        self.play_screen.draw(self.screen, self.border_length)
                
            #______________________________________________________________________
            # Wait for the next tick of the Clock

            self.clock.tick(60)  # limits FPS to 60
                
        # _____________________________________________________________________
        # here stopped the old while true

        if not self.running:
            self.callback_function(DisplayCommand.EXIT)
            pygame.quit()

   
        
# if __name__ == "__main__":
#     #put unit tests here
#     pass