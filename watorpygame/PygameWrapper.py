
# standard imports
from typing import cast
from enum import Enum

# pygame imports
import pygame
from pygame.surface import Surface

# Wa-Tor imports
from watorpygame.DisplayState import DisplayState
from watorpygame.UserButton import UserButton
from watorpygame.UserImage import UserImage
from watorpygame.UserImageInfo import UserImageInfo
from watorpygame.UserImageKey import UserImageKey
from watorpygame.UserImageProvider import UserImageProvider
from watorpygame.UserTextBox import UserTextBox
from watorpygame.PlayScreen import WaTorPlayScreen
from watorpygame.WaTorColors import *
from watorpygame.ConfigScreen import WaTorConfigScreen

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
        self.textboxes = []
        self.state = DisplayState.OUT

        background_color = WaTorColors().colors[ColorChoice.SCREEN_BACKGROUND_COLOR]

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
    # region initialize_screen
    #__________________________________________________________________________
    def initialize_screen(self):
        # pygame setup
        pygame.init()

        #______________________________________________________________________
        # start the window on screen
        size = (self.window_width, self.window_heigth)
        self.screen = pygame.display.set_mode(size)

        #______________________________________________________________________
        # The clock will be used used 
        # each time the tick(60) function will be called 
        self.clock = pygame.time.Clock()
        self.running = True

        #______________________________________________________________________
        # the buttons need a screen object to exist (because they are localized in screen) 
        # the textboxes need a font object which does not exist before pygame.init()
        self.initialize_buttons()
        self.initialize_textboxes()

        #______________________________________________________________________
        # transfert to screens
        if self.state == DisplayState.CONF :
            if self.config_screen_need_initialization :
                self.config_screen.initialize_controls(
                    self.screen,
                    self.border_length,
                    self.buttons)
                
                self.config_screen_need_initialization = False
        else :
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

        if self.state == DisplayState.CONF:
            self.commands = {
                DisplayState.CONF : "Reset",
                DisplayState.WAIT : "Go" }
        else :
            self.commands = {
                DisplayState.PLAY: "Start",
                DisplayState.PAUSE: "Pause", 
                DisplayState.STOP: "Stop" }
            
        count = len(self.commands)
        for command_key, command_text in reversed(self.commands.items()):
            self.buttons.append(
                UserButton( command_key, command_text, self.callback_function,
                    pygame.Rect(
                        self.window_width - count * (self.button_width + self.border_length),
                        self.window_heigth - self.button_heigth - self.border_length,
                        self.button_width,
                        self.button_heigth)))
            count += 1

    #__________________________________________________________________________
    #
    # region initialize_textboxes
    #__________________________________________________________________________
    def initialize_textboxes(self):
        
        if self.state == DisplayState.CONF :
            field_values = cast(dict, self.data).values()
            font = pygame.font.Font(None, 30)

            x = 100
            y = 100
            for field_value in field_values : 
                textbox = UserTextBox(x, y, 100, 50, font, field_value)
                self.textboxes.append(textbox)
                y += 50

    def draw_label(self, screen : pygame.Surface, text : str,  x_pos:int, y_pos:int, font_size : int, align :int = -1) :
        """
        draw text in a y-centered rect on the screen depending on the value of align
            align = -1 (default) draw the text rect starting at x
            align = 0 draw the text rect centered on (x, y)
            align = 1 draw the text rect ending at x + width
        """
        my_font = pygame.font.Font(None, font_size)
        text_surface = my_font.render(text, False, (0, 0, 255))
        width = text_surface.get_width() 
        heigth = text_surface.get_height()
        if align == -1 :
            screen.blit(text_surface, (x_pos,y_pos-heigth/2))
        elif align == 0 :
            screen.blit(text_surface, (x_pos-width/2,y_pos-heigth/2))
        elif align ==1 :
            screen.blit(text_surface, (x_pos-width,y_pos-heigth/2))
        else : raise ValueError("align value not available")

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

            for textbox in self.textboxes :
                cast(UserTextBox, textbox).handle_event(event)

            if event.type == pygame.QUIT:
                self.running = False

            # Check for the mouse button down event
            for button in self.buttons:
                button.check_event(event)

        center_x = self.screen.get_rect().centerx
        top_y = self.screen.get_rect().top + 25

        if self.state == DisplayState.CONF :
            self.draw_label(self.screen, "Ecran de configuration", center_x, top_y, 30, 0)
            self.config_screen.draw(self.screen, self.border_length)
        else :
            self.draw_label(self.screen, "Affichage initial", center_x, top_y, 30, 0)
            self.play_screen.draw(self.screen, self.border_length)
            
        #______________________________________________________________________
        # Wait for the next tick of the Clock

        self.clock.tick(60)  # limits FPS to 60
            
        # _____________________________________________________________________
        # here stopped the old while true

        if not self.running:
            self.callback_function(DisplayState.OUT)
            pygame.quit()

    
    #
    def get_conf(self) -> dict :
        return self.config_screen.get_conf() 

        