import pygame


class UserButton:

    def __init__(
        self,
        name: str,
        callback_function,
        x_position: int,
        y_position: int,
        x_width: int,
        y_height: int,
    ):
        self.name = name
        self.callback_function = callback_function
        self.x_position = x_position
        self.y_position = y_position
        self.x_width = x_width
        self.y_height = y_height
        # ______________________________________________________________________
        # Create a font object
        font = pygame.font.Font(None, 24)

        # Create a surface for the button
        self.button_surface = pygame.Surface((self.x_width, self.y_height))

        # Render text on the button
        self.text_render = font.render(self.name, True, (0, 0, 0))
        self.text_rect = self.text_render.get_rect(
            center=(
                self.button_surface.get_width() / 2,
                self.button_surface.get_height() / 2,
            )
        )

        # Create a pygame.Rect object that represents the button's boundaries
        self.button_rect = pygame.Rect(
            self.x_position, self.y_position, self.x_width, self.y_height
        )  # Adjust the position as needed
        # ______________________________________________________________________

    def check_event(self, event):
        # Check for the mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Call the on_mouse_button_down() function
            if self.button_rect.collidepoint(event.pos):
                self.callback_function(self.name)

    def show(self, screen: pygame.Surface):

        # Check if the mouse is over the button. This will create the button hover effect
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(
                self.button_surface,
                (127, 255, 212),
                (1, 1, self.x_width - 2, self.y_height - 2),
            )
        else:
            pygame.draw.rect(
                self.button_surface, (0, 0, 0), (0, 0, self.x_width, self.y_height)
            )
            pygame.draw.rect(
                self.button_surface,
                (255, 255, 255),
                (1, 1, self.x_width - 2, self.y_height - 2),
            )
            pygame.draw.rect(
                self.button_surface, (0, 0, 0), (1, 1, self.x_width - 2, 1), 2
            )
            pygame.draw.rect(
                self.button_surface,
                (0, 100, 0),
                (1, self.y_height - 2, self.x_width - 2, 10),
                2,
            )
        # __________________________________________________________________________

        # __________________________________________________________________________
        # Show the button text
        self.button_surface.blit(self.text_render, self.text_rect)

        # Draw the button on the screen
        screen.blit(self.button_surface, (self.button_rect.x, self.button_rect.y))
