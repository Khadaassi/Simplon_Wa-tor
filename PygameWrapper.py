
# standard imports
from typing import cast

# pygame imports
import pygame
from pygame.surface import Surface

# Wa-Tor imports
from UserButton import UserButton
from UserImage import UserImage
from DisplayState import DisplayState
from PlayScreen import PlayScreen

class PygameWrapper:

    def __init__(self, callback_function):
        self.tab = []
        self.callback_function = callback_function
        self.window_width = 1000  # defaut value
        self.window_heigth = 700  # defaut value

        # borders & buttons dimensions
        self.border_length = 25
        self.buttons_height = 50
        self.buttons_width = 75

        self.play_screen = PlayScreen(self, 0,0,0,0,0,0)

        self.screen_background_color = (100, 100, 100)
        
        self.running = False
        self.screen = None
        self.clock = None

        self.buttons = []

    def get_tab(self):
        return self.tab

    def set_tab(self, tab):
        self.tab = tab

        if len(self.tab) == 0:
            return

        if self.len_tab_x != len(self.tab[0]):
            self.initialize_controls()

    def initialize_controls(self):
        #______________________________________________________________________
        # about format informations :
        #    len_tab_x = width corresponds to the number of columns in the matrix 
        #    len_tab_y = height corresponds to the number of lines in the matrix 
        self.len_tab_x = len(self.tab[0])
        self.len_tab_y = len(self.tab)

        self.table_width = self.window_width - 2 * self.border_length
        self.table_heigth = (
            self.window_heigth - self.buttons_height - 3 * self.border_length
        )

        self.x_cell_length = (self.table_width) // self.len_tab_x
        self.y_cell_length = (self.table_heigth) // self.len_tab_y

        self.shark_image.define_dimensions(self.x_cell_length, self.y_cell_length)
        self.fish_image.define_dimensions(self.x_cell_length, self.y_cell_length)

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
            DisplayState.STOP: "Stop"}
        count = 3
        for command_key, command_text in reversed(self.commands.items()):
            self.buttons.append(
                UserButton( command_key, command_text, self.callback_function,
                    pygame.Rect(
                        self.window_width - count * (self.buttons_width + self.border_length),
                        self.window_heigth - self.buttons_height - self.border_length,
                        self.buttons_width,
                        self.buttons_height
                    )
                )
            )
            count += 1

    def draw(self, screen_surface: Surface, clock, callback_function, display_state : DisplayState = DisplayState.WAIT):
        if not self.running:
            self.initialize_screen()  # first time only

        # _____________________________________________________________________
        # here started the old while true
        if display_state == DisplayState.WAIT :
            self.play_screen.draw()

        