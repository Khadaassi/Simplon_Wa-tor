import pygame
import sys
import display_functions as dis_fun

# Initialize Pygame
pygame.init()

clock=pygame.time.Clock()

# Create a Pygame window
window_size = (400, 400)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Display test n°3')

start_button = dis_fun.user_button("Start", 125, 125, 150, 50)

# Start the main loop
while True:
    # Set the frame rate
    clock.tick(60)
 
    # Fill the display with color
    screen.fill((155, 255, 155))

    # Get events from the event queue
    for event in pygame.event.get():
        # Check for the quit event
        if event.type == pygame.QUIT:
            # Quit the game
            pygame.quit()
            sys.exit()
   
        #______________________________________________________________________

        # Check for the mouse button down event
        start_button.check_event(event)

        #______________________________________________________________________

        
    #__________________________________________________________________________

    start_button.show(screen)

    #__________________________________________________________________________

    # Update the game state
    pygame.display.update()
    