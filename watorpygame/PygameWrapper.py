
# standard imports
from typing import cast
from enum import Enum

# pygame imports
import pygame
from pygame.surface import Surface

# Wa-Tor imports
from watorpygame.DisplayState import DisplayState
from watorpygame.DisplayCommand import DisplayCommand

from watorpygame.WaTorColors import *

from watorpygame.UserImage import UserImage
from watorpygame.UserImageInfo import UserImageInfo
from watorpygame.UserImageKey import UserImageKey
from watorpygame.UserImageProvider import UserImageProvider, Direction

import ConfigField as cf
import watorpygame.ConfigFieldUser as cfu 

from watorpygame.UserTextBox import UserTextBox
from watorpygame.UserButton import UserButton
from watorpygame.PlayScreen import WaTorPlayScreen

from watorpygame.ConfigScreen import WaTorConfigScreen
from watorpygame.IterationInfo import IterationInfo

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
        self.buttons =[]
        self.textboxes = []
        self.state = DisplayState.OUT

        background_color = WaTorColors().get(ColorChoice.SCREEN_BACKGROUND_COLOR)

        self.config_screen = WaTorConfigScreen(background_color, self.image_provider)
        self.play_screen = WaTorPlayScreen(background_color, self.image_provider)
        
        self.play_screen_need_initialization = True
        self.config_screen_need_initialization = True
        self.running = False
        self.screen = None
        self.clock = None
        # self.max_time = 33 # value in milliseconds correspond to 3O Frame per second
        # self.current_time = 0

    #__________________________________________________________________________
    #
    # region set_state
    #__________________________________________________________________________
    def set_state(self, state : DisplayState) :
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
    # region set_data
    #__________________________________________________________________________
    def set_info(self, iterationInfo : IterationInfo) :
        self.play_screen.set_info(iterationInfo)
    #__________________________________________________________________________
    #
    # region initialize_screen
    #__________________________________________________________________________
    def initialize_screen(self):
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
        self.initialize_controls()

    #__________________________________________________________________________
    #
    # region initialize_controls
    #__________________________________________________________________________
    def initialize_controls(self):
        #______________________________________________________________________
        # the buttons need a screen object to exist (because they are localized in screen) 
        # the textboxes need a font object which does not exist before pygame.init()
        self.initialize_buttons()
        self.initialize_textboxes()

        #______________________________________________________________________
        # transfert to screens
        match self.state :
            case DisplayState.CONF :
                if self.config_screen_need_initialization :
                    self.config_screen.initialize_controls(
                        self.screen,
                        self.border_length,
                        self.buttons,
                        self.textboxes)
                
                    self.config_screen_need_initialization = False

            case _ :
                if self.play_screen_need_initialization :
                    self.play_screen.initialize_controls(
                            self.screen,
                            self.border_length,
                            self.buttons)
                    
                    self.play_screen_need_initialization = False
    
    #__________________________________________________________________________
    #
    # region initialize_buttons
    #__________________________________________________________________________
    def initialize_buttons(self) :
        #______________________________________________________________________
        # Buttons need to be created after the creation of the screen
        if len(self.buttons) != 0 :
            self.disable_buttons()

        self.buttons = []
        match self.state :
            case DisplayState.CONF:
                self.commands = {
                    DisplayCommand.RESET : "Reset",
                    DisplayCommand.GO : "Go" }
                
            case DisplayState.BETWEEN:
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
                        self.window_width - count * (self.button_width + self.border_length),
                        self.window_height - self.button_height - self.border_length,
                        self.button_width,
                        self.button_height)))
            count -= 1

    #__________________________________________________________________________
    #
    # region initialize_textboxes
    #__________________________________________________________________________
    def initialize_textboxes(self):
        
        if len(self.textboxes) != 0 :
            self.disable_textboxes()

        if self.state != DisplayState.CONF :
            return
        
        self.textboxes = []
        config_fields = cast(dict, self.data)

        font = pygame.font.Font(None, 30)

        number_of_textboxes = len(config_fields)
        number_of_spaces = number_of_textboxes -1
        available_height = self.window_height - 4 * self.border_length - self.button_height

        textbox_width = 150
        textbox_height = 0.80 * available_height / number_of_textboxes
        
        total_space = available_height - textbox_height * number_of_textboxes
        single_space = float(total_space)/number_of_spaces
        
        textbox_pos_x = self.window_width - self.border_length - textbox_width 
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
    # region disable_buttons
    #__________________________________________________________________________
    def disable_buttons(self) :
        for button in self.buttons :
            cast(UserButton, button).callback_function = None

    #__________________________________________________________________________
    #
    # region disable_textboxes
    #__________________________________________________________________________
    def disable_textboxes(self) :
        for textbox in self.textboxes :
            cast(UserTextBox, textbox).callback_function = None
        
    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, display_state : DisplayState):
        
        if not self.running:
            self.initialize_screen()  # first time only, start screen
            
        # self.current_time = self.clock.tick() - self.current_time
        # if self.current_time < 100 :
        #     return 
        
                     
        #__________________________________________________________________
        # poll for events 
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            for textbox in self.textboxes :
                cast(UserTextBox, textbox).check_event(event)
            
            # Check for the mouse button down event
            for button in self.buttons:
                cast(UserButton, button).check_event(event)

        center_x = self.screen.get_rect().centerx
        top_y = self.screen.get_rect().top + 25

        match self.state :
            case DisplayState.CONF :  
                self.config_screen.textboxes = self.textboxes
                self.config_screen.buttons = self.buttons   
                self.config_screen.draw(self.screen, self.border_length)

            case DisplayState.BETWEEN :     
                pass
            
            case _ :      
                self.play_screen.buttons = self.buttons  
                self.play_screen.draw(self.screen, self.border_length)
            
        #______________________________________________________________________
        # Wait for the next tick of the Clock

        self.clock.tick(60)  # limits FPS to 60
            
        # _____________________________________________________________________
        # here stopped the old while true

        if not self.running:
            self.callback_function(DisplayCommand.EXIT)
            pygame.quit()

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

        
# if __name__ == "__main__":
#     #put unit tests here
#     pass