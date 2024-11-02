import pygame

class UserLabel :
    def __init__(self) :
       pass

    #__________________________________________________________________________
    #
    # region draw_label
    #__________________________________________________________________________
    def draw(self, screen : pygame.Surface, text : str,  x_pos:int, y_pos:int, font_size : int, align :int = -1) :
        """
        draw text in a y-centered rect on the screen depending on the value of align
            align = -1 (default) draw the text rect starting at x
            align = 0 draw the text rect centered on (x, y)
            align = 1 draw the text rect ending at x + width
        """
        my_font = pygame.font.Font(None, font_size)
        text_surface_back = my_font.render(text, False, "white")
        text_surface_front = my_font.render(text, False, (0, 0, 255))
        width = text_surface_front.get_width() 
        heigth = text_surface_front.get_height()
        if align == -1 :
            screen.blit(text_surface_back, (2+x_pos,2+y_pos-heigth/2))
            screen.blit(text_surface_front, (x_pos,y_pos-heigth/2))
        elif align == 0 :
            screen.blit(text_surface_back, (2+x_pos-width/2,2+y_pos-heigth/2))
            screen.blit(text_surface_front, (x_pos-width/2,y_pos-heigth/2))
        elif align ==1 :
            screen.blit(text_surface_back, (2+x_pos-width,2+y_pos-heigth/2))
            screen.blit(text_surface_front, (x_pos-width,y_pos-heigth/2))
        else : 
            raise ValueError("align value not available")
        
if __name__ == "__main__":
    #put unit tests here
    pass
