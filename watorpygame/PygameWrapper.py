
# standard imports
from typing import cast
from enum import Enum

# pygame imports
import pygame
from pygame.surface import Surface

# Wa-Tor imports
from DisplayState import DisplayState
from watorpygame.UserButton import UserButton
from watorpygame.UserImage import UserImage
from watorpygame.UserImageProvider import UserImageKey, UserImageProvider
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
        self.window_heigth = 700  # defaut value

        #______________________________________________________________________
        # Central definition of 
        # borders & buttons dimensions
        self.border_length = 25
        self.button_heigth = 50
        self.button_width = 75
        self.buttons =[]

        self.screen_background_color = "lightgray"
        self.play_screen = WaTorPlayScreen(self.screen_background_color, self.image_provider)
        
        self.play_screen_need_initialization = True
        self.running = False
        self.screen = None
        self.clock = None

    #__________________________________________________________________________
    #
    # region set_data
    #__________________________________________________________________________
    def set_data(self, data : list[list[UserImageKey]]):
        self.play_screen.set_data(data)
    
    #__________________________________________________________________________
    #
    # region initialize_screen
    #__________________________________________________________________________
    def initialize_screen(self):
        # pygame setup
        pygame.init()

        #______________________________________________________________________
        # start the window on screen
        self.screen = pygame.display.set_mode((self.window_width, self.window_heigth))

        #______________________________________________________________________
        # The clock will be used used 
        # each time the tick(60) function will be called 
        self.clock = pygame.time.Clock()
        self.running = True

        #______________________________________________________________________
        # Buttons need to be created after the creation of the screen

        self.commands = {
            DisplayState.PLAY: "Start",
            DisplayState.PAUSE: "Pause", 
            DisplayState.STOP: "Stop"
        }
        count = 3
        for command_key, command_text in reversed(self.commands.items()):
            self.buttons.append(
                UserButton( command_key, command_text, self.callback_function,
                    pygame.Rect(
                        self.window_width - count * (self.button_width + self.border_length),
                        self.window_heigth - self.button_heigth - self.border_length,
                        self.button_width,
                        self.button_heigth)))
            count += 1

        #______________________________________________________________________
        # transfert to play_screen
        if self.play_screen_need_initialization :
            self.play_screen.initialize_controls(
                    self.screen,
                    self.border_length,
                    self.buttons)
            
            self.play_screen_need_initialization = False

    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, display_state : DisplayState = DisplayState.WAIT):
        if not self.running:
            self.initialize_screen()  # first time only, start screen
                     
        #__________________________________________________________________
        # poll for events 
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Check for the mouse button down event
            for button in self.buttons:
                button.check_event(event)
                
        self.play_screen.draw(self.screen, self.border_length)
            
        #______________________________________________________________________
        # Wait for the next tick of the Clock

        self.clock.tick(60)  # limits FPS to 60
            
        # _____________________________________________________________________
        # here stopped the old while true

        if not self.running:
            self.callback_function(DisplayState.OUT)
            pygame.quit()

        