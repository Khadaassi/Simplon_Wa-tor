# standard imports
from typing import cast

# pygame imports
import pygame
from pygame.surface import Surface

# Wa-Tor imports
from UserImage import UserImage
from DisplayState import DisplayState

class PlayScreen :
    def __init__(self, screen_background_color ) :
        self.screen_background_color = screen_background_color
        self.shark_image = UserImage("images/Shark_image_1.png", "red", "darkred")
        self.fish_image = UserImage("images/Fish_image_1.png", "green", "darkgreen")
        self.data = []

    def set_data(self, data : list[list]) :
        self.data = data

    def draw(self, screen : Surface, clock : pygame.time.Clock, callback_function) :
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Check for the mouse button down event
            for button in self.pygame_wrapper.buttons:
                button.check_event(event)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(self.screen_background_color)

        # RENDER YOUR GAME HERE
        tab = self.get_tab()
        for y_index in range(self.len_tab_y):
            for x_index in range(self.len_tab_x):

                position_x = self.border_length + x_index * self.cell_width
                position_y = self.border_length + y_index * self.cell_height

                even_case = (x_index + y_index) % 2 == 0

                if tab[y_index][x_index] == "~":
                    case_color = UserImage.light_color if even_case else UserImage.dark_color
                else:
                    obj = tab[y_index][x_index]
                    image = cast(UserImage, obj)
                    case_color = image.light_background_color if even_case else image.dark_background_color
                    
                    x_image = self.border_length + x_index * self.cell_width
                    y_image = self.border_length + y_index * self.cell_height

                pygame.draw.rect(
                    screen,
                    case_color,
                    [position_x, position_y, self.cell_width, self.cell_height],
                )

                if tab[y_index][x_index] == "~":
                    continue

                screen.blit(image.resized, (x_image, y_image))

        for button in self.buttons:
            button.show(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()


        #______________________________________________________________________
        # Wait for the next tick of the Clock

        clock.tick(60)  # limits FPS to 60

        # _____________________________________________________________________
        # here stopped the old while true

        if not self.running:
            callback_function(DisplayState.OUT)
            pygame.quit()
