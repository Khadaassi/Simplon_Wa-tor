import pygame
from watorpygame.WaTorColors import ColorChoice, WaTorColors

class UserLabel :

    #__________________________________________________________________________
    #
    # region __init__
    #__________________________________________________________________________
    def __init__(self) :
       pass

    #__________________________________________________________________________
    #
    # region draw_label
    #__________________________________________________________________________
    def draw(self, screen : pygame.Surface, 
             text : str,  
             x_pos:int, y_pos:int, 
             font_size : int, 
             align :int = -1, 
             backlabel: bool = False) :
        """
        draw text in a y-centered rect on the screen depending on the value of align
            align = -1 (default) draw the text rect starting at x
            align = 0 draw the text rect centered on (x, y)
            align = 1 draw the text rect ending at x
        """

        colors = WaTorColors()
        back_color = colors.get(ColorChoice.BACK_LABEL)
        front_color = colors.get(ColorChoice.FRONT_LABEL)

        my_font = pygame.font.Font(None, font_size)
        text_surface_back = my_font.render(text, False, back_color)
        text_surface_front = my_font.render(text, False, front_color)

        width = text_surface_front.get_width() 
        heigth = text_surface_front.get_height()

        match align :
            case -1 :
                if backlabel : screen.blit(text_surface_back, (1+x_pos,1+y_pos-heigth/2))
                screen.blit(text_surface_front, (x_pos,y_pos-heigth/2))
            case 0 :
                if backlabel : screen.blit(text_surface_back, (1+x_pos-width/2,1+y_pos-heigth/2))
                screen.blit(text_surface_front, (x_pos-width/2,y_pos-heigth/2))
            case 1 :
                if backlabel : screen.blit(text_surface_back, (1+x_pos-width,1+y_pos-heigth/2))
                screen.blit(text_surface_front, (x_pos-width,y_pos-heigth/2))
            case _ :
                  raise ValueError("align value not available")
        
# if __name__ == "__main__":
#     #put unit tests here
#     pass
