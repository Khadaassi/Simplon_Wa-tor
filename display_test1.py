# Example file showing a basic pygame "game loop"
import pygame
from UserButton import UserButton
from UserImage import UserImage

# pygame setup
pygame.init()

#borders & buttons dimensions
border_length= 50
buttons_height=50
buttons_length=100

# format 16/9
table_width = 16 * 50
table_heigth = 9 * 50

window_width = table_width + 2 * border_length
window_heigth = table_heigth + buttons_height + 3 * border_length

screen = pygame.display.set_mode((window_width, window_heigth))
clock = pygame.time.Clock()
running = True

x_length = 16 # tableau de 16 cases
y_length = 9 # tableau de 9 cases

x_cell_length= (table_width)//x_length
y_cell_length = (table_heigth)//y_length

x_test_image = 8
y_test_image = 4
shark_image = UserImage("Shark_image_1.png")
shark_image.define_dimensions(x_cell_length, y_cell_length)
shark_image_x = border_length + (x_test_image-1) * x_cell_length
shark_image_y = border_length + (y_test_image-1) * y_cell_length

x_test_image_2 = 3
y_test_image_2 = 1
fish_image = UserImage("Fish_image_1.png")
fish_image.define_dimensions(x_cell_length, y_cell_length)
fish_image_x = border_length + (x_test_image_2-1) * x_cell_length
fish_image_y = border_length + (y_test_image_2-1) * y_cell_length


start_button = UserButton("Start", 
    window_width-3*(buttons_height+2*border_length) , 
    window_heigth- buttons_height-border_length, 
    buttons_length, 
    buttons_height)
pause_button = UserButton("Pause", 
    window_width-2*(buttons_height+2*border_length) , 
    window_heigth- buttons_height-border_length, 
    buttons_length, 
    buttons_height)
stop_button = UserButton("Stop", 
    window_width-(buttons_height+2*border_length), 
    window_heigth- buttons_height-border_length, 
    buttons_length, 
    buttons_height)



while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for the mouse button down event
        start_button.check_event(event)
        pause_button.check_event(event)
        stop_button.check_event(event)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    white_color = (255,255,255)
    black_color = (0,0,0)

    # RENDER YOUR GAME HERE
    for x_index in range(0,x_length):
        for y_index in range(0,y_length):
            case_color = white_color if (x_index+y_index)%2==0 else black_color
            position_x = border_length + x_index*x_cell_length
            position_y = border_length + y_index*y_cell_length
                
            pygame.draw.rect(screen,case_color,[position_x,position_y,x_cell_length,y_cell_length])

    screen.blit(shark_image.resized, 
                (shark_image_x,shark_image_y))
    
    screen.blit(fish_image.resized, 
                (fish_image_x, fish_image_y))


    start_button.show(screen)
    pause_button.show(screen)
    stop_button.show(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()