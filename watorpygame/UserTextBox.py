from pygame import *
from pygame import Surface, Rect, MOUSEBUTTONDOWN, KEYDOWN, K_BACKSPACE
from pygame.font import Font
from pygame.event import Event
from watorpygame.WaTorColors import *
from ConfigField import ConfigField

#from typing import cast

class UserTextBox:
    
    #__________________________________________________________________________
    #
    # region __init__
    #__________________________________________________________________________
    def __init__(self, field_key : ConfigField, x, y, w, h, font : Font, field_value : str = "", eval_function = int ):
        self.field_key = field_key
        self.__field_value = field_value
        self.__rect = Rect(x, y, w, h)
        self.__txt_surface = Surface((w,h))
        self.__font = font
        self.__eval_function = eval_function
        self.callback_function = None

        colors = WaTorColors()
        self.__color_inactive  = colors.get(ColorChoice.TEXTBOX_INACTIVE)
        self.__color_active  = colors.get(ColorChoice.TEXTBOX_ACTIVE)
        self.__color_invalid  = colors.get(ColorChoice.TEXTBOX_INVALID)
        self.color = self.__color_inactive
        self.reset_text(field_value)

    #__________________________________________________________________________
    #
    # region reset_text
    #__________________________________________________________________________
    def reset_text(self, text : str) :
        self.__field_value = text
        self.__txt_surface = self.__font.render( str(self.__field_value), True, self.__color_inactive)
        self.active = False
        self.color = self.__color_inactive

    #__________________________________________________________________________
    #
    # region validate
    #__________________________________________________________________________
    def validate(self) -> bool :
        try :
            val = self.get_validated_value() # transforms value type from str to it's correct type
            return True
        except :
            return False
        
    #__________________________________________________________________________
    #
    # region get_validated_value
    #__________________________________________________________________________
    def get_validated_value(self) -> bool | int | float | str :   
        if self.__eval_function == bool :
            if self.__field_value == "True" : 
                return True
            elif self.__field_value == "False" : 
                return False 
            else : 
                raise TypeError("Must be True or False")  
        elif self.__eval_function == str :
            return str(self.__field_value)
        else :
            val = self.__eval_function(self.__field_value)
            if val >= 0 :
                return val
            else :
                raise TypeError("Negative numbers are not accepted") 

    #__________________________________________________________________________
    #
    # region register_callback_function
    #__________________________________________________________________________
    def register_callback_function(self, callback_function) :
        self.callback_function = callback_function

    #__________________________________________________________________________
    #
    # region get_rect
    #__________________________________________________________________________
    def get_rect(self) -> Rect :
        return self.__rect
    
    #__________________________________________________________________________
    #
    # region check_event
    #__________________________________________________________________________
    def check_event(self, event : Event):
        if event.type == MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.__rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.__color_active if self.active else self.__color_inactive

        if event.type == KEYDOWN:
            if self.active:
                #if event.key == pg.K_RETURN:
                    #print(self.field_value)
                    #self.field_value = ''
                if event.key == K_BACKSPACE:
                    self.__field_value = str(self.__field_value)[:-1]
                else:
                    self.__field_value = str(self.__field_value) + str(event.unicode)

                if self.validate() :
                    self.color = self.__color_active if self.active else self.__color_inactive
                    if self.callback_function != None :
                        self.callback_function(self.field_key)
                else : 
                    self.color = self.__color_invalid if self.active else self.__color_inactive

                # Re-render the text.
                self.__txt_surface = self.__font.render(str(self.__field_value), True, self.color)

    # #__________________________________________________________________________
    # #
    # # region update
    # #__________________________________________________________________________
    # def update(self):
    #     # Resize the box if the text is too long.
    #     width = max(200, self.__txt_surface.get_width()+10)
    #     self.__rect.w = width

    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, screen : Surface):
        # black background
        pygame.draw.rect(screen, (0,0,0), self.__rect, 0)
        # Blit the text.
        x_start = self.__rect.x + self.__rect.width/2 - self.__txt_surface.get_width()/2
        y_start = self.__rect.y + self.__rect.height/2 - self.__txt_surface.get_height()/2 
        screen.blit(self.__txt_surface, (x_start, y_start))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.__rect, 2)
