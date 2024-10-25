# Example file showing a basic pygame "game loop"
import pygame
import display_functions as dis_fun

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

start_button = dis_fun.user_button("Start", 
    window_width-3*(buttons_height+2*border_length) , 
    window_heigth- buttons_height-border_length, 
    buttons_length, 
    buttons_height)
pause_button = dis_fun.user_button("Pause", 
    window_width-2*(buttons_height+2*border_length) , 
    window_heigth- buttons_height-border_length, 
    buttons_length, 
    buttons_height)
stop_button = dis_fun.user_button("Stop", 
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
            position_x = 50 + x_index*x_cell_length
            position_y = 50 + y_index*y_cell_length
                
            pygame.draw.rect(screen,case_color,[position_x,position_y,x_cell_length,y_cell_length])

    start_button.show(screen)
    pause_button.show(screen)
    stop_button.show(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()