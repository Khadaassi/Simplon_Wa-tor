# pygame imports
import pygame

# pygame imports
import watorpygame.DisplayCommand as DisplayCommand


class UserButton:

    # _________________________________________________________________________
    #
    # region __init__
    # _________________________________________________________________________
    def __init__(self, command_key : DisplayCommand, command_text: str, callback_function, button_rect : pygame.Rect):
        
        self.command_key = command_key
        self.text = command_text
        self.callback_function = callback_function

        self.button_rect = button_rect

        # _____________________________________________________________________
        # Create a surface for the button
        self.button_surface = pygame.Surface((self.button_rect.width, self.button_rect.height))

        # _____________________________________________________________________
        # Create a font object
        font = pygame.font.Font(None, 24)

        # _____________________________________________________________________
        # Render text on the button
        self.text_render = font.render(self.text, True, (0, 0, 0))
        self.text_rect = self.text_render.get_rect(
            center=(
                self.button_surface.get_width() / 2,
                self.button_surface.get_height() / 2))
 
    # _________________________________________________________________________
    #
    # region check_event
    # _________________________________________________________________________
    def check_event(self, event):
        # Check for the mouse button down event
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Call the on_mouse_button_down() function
            if self.button_rect.collidepoint(event.pos):
                self.callback_function(self.command_key)
    
    # _________________________________________________________________________
    #
    # region draw
    # _________________________________________________________________________
    def draw(self, screen: pygame.Surface):

        # Check if the mouse is over the button. This will create the button hover effect
        if self.button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect( self.button_surface, 
                (127, 255, 212), 
                (1, 1, self.button_rect.width - 2, self.button_rect.height - 2))
        else:
            pygame.draw.rect( self.button_surface, 
                (0, 0, 0), 
                (0, 0, self.button_rect.width, self.button_rect.height))
            pygame.draw.rect( self.button_surface, 
                (255, 255, 255), 
                (1, 1, self.button_rect.width - 2, self.button_rect.height - 2))
            pygame.draw.rect( self.button_surface,
                (0, 0, 0), 
                (1, 1, self.button_rect.width - 2, 1), 
                2)
            pygame.draw.rect( self.button_surface, 
                (0, 100, 0), 
                (1, self.button_rect.height - 2, self.button_rect.width - 2, 10), 
                2)

        # __________________________________________________________________________
        # Show the button text
        self.button_surface.blit(self.text_render, self.text_rect)

        # Draw the button on the screen
        screen.blit(self.button_surface, (self.button_rect.x, self.button_rect.y))

# if __name__ == "__main__":
#     #put unit tests here
#     pass