import pygame
from UserButton import UserButton
from UserImage import UserImage
from typing import cast


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
        self.len_tab_x = 0
        self.len_tab_y = 0

        self.table_width = 0
        self.table_height = 0
        self.x_cell_length = 0
        self.y_cell_length = 0

        self.shark_image = UserImage("images/Shark_image_1.png")
        self.fish_image = UserImage("images/Fish_image_1.png")
        self.running = False
        self.screen = None

        # perhaps that clock is never used
        # since the while True has been removed
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
        # format width = len(x) / heigth = len(y)
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

        self.screen = pygame.display.set_mode((self.window_width, self.window_heigth))
        self.clock = pygame.time.Clock()
        self.running = True

        # Buttons need to be created after the creation of the screen

        self.commands = ["Start", "Pause", "Stop"]
        count = 3
        for command in reversed(self.commands):
            self.buttons.append(
                UserButton(
                    command,
                    self.callback_function,
                    self.window_width
                    - count * (self.buttons_width + self.border_length),
                    self.window_heigth - self.buttons_height - self.border_length,
                    self.buttons_width,
                    self.buttons_height,
                )
            )
            count += 1

    def draw(self):
        if not self.running:
            self.initialize_screen()  # first time only

        # ______________________________________________________________________
        # here started the old while true

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Check for the mouse button down event
            for button in self.buttons:
                button.check_event(event)

        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill((100, 100, 100))

        # RENDER YOUR GAME HERE
        tab = self.get_tab()
        for y_index in range(self.len_tab_y):
            for x_index in range(self.len_tab_x):

                position_x = self.border_length + x_index * self.x_cell_length
                position_y = self.border_length + y_index * self.y_cell_length

                case_color = (
                    UserImage.light_color
                    if (x_index + y_index) % 2 == 0
                    else UserImage.dark_color
                )
                pygame.draw.rect(
                    self.screen,
                    case_color,
                    [position_x, position_y, self.x_cell_length, self.y_cell_length],
                )

                if tab[y_index][x_index] == "~":
                    continue

                obj = tab[y_index][x_index]
                image = cast(UserImage, obj)

                x_image = self.border_length + x_index * self.x_cell_length
                y_image = self.border_length + y_index * self.y_cell_length

                self.screen.blit(image.resized, (x_image, y_image))

        for button in self.buttons:
            button.show(self.screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        self.clock.tick(60)  # limits FPS to 60

        # ______________________________________________________________________
        # here stopped the old while true

        if not self.running:
            self.callback_function("Quit")
            pygame.quit()
