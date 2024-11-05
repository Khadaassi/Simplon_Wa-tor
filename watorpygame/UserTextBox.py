import pygame as pg
from watorpygame.WaTorColors import *
from ConfigField import ConfigField

#from typing import cast

class UserTextBox:
    
    #__________________________________________________________________________
    #
    # region __init__
    #__________________________________________________________________________
    def __init__(self, field_key : ConfigField, x, y, w, h, font : pg.font.Font, field_value : str = "", validation_function = int ):
        self.field_key = field_key
        self.rect = pg.Rect(x, y, w, h)
        self.font = font
        self.validation_function = validation_function
        colors = WaTorColors()
        self.color_inactive  = colors.get(ColorChoice.TEXTBOX_INACTIVE)
        self.color_active  = colors.get(ColorChoice.TEXTBOX_ACTIVE)
        self.color_invalid  = colors.get(ColorChoice.TEXTBOX_INVALID)
        self.color = self.color_inactive
        self.callback_function = None
        self.reset_text(field_value)
    #__________________________________________________________________________
    #
    # region reset_text
    #__________________________________________________________________________
    def reset_text(self, text : str) :
        self.field_value = text
        self.txt_surface = self.font.render( str(self.field_value), True, self.color_inactive)
        self.active = False
        self.color = self.color_inactive

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
        if self.validation_function == bool :
            if self.field_value == "True" : 
                return True
            elif self.field_value == "False" : 
                return False 
            else : 
                raise TypeError("Must be True or False")  
        elif self.validation_function == str :
            return str(self.field_value)
        else :
            val = self.validation_function(self.field_value)
            if val >= 0 :
                return val
            else :
                raise TypeError("Negative numbers are not accepted") 
    
    #__________________________________________________________________________
    #
    # region register_validation_function
    #__________________________________________________________________________
    def register_validation_function(self, callback_function) :
        self.callback_function = callback_function

    #__________________________________________________________________________
    #
    # region get_rect
    #__________________________________________________________________________
    def get_rect(self) -> pg.Rect :
        return self.rect
    
    #__________________________________________________________________________
    #
    # region check_event
    #__________________________________________________________________________
    def check_event(self, event : pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pg.KEYDOWN:
            if self.active:
                #if event.key == pg.K_RETURN:
                    #print(self.field_value)
                    #self.field_value = ''
                if event.key == pg.K_BACKSPACE:
                    self.field_value = str(self.field_value)[:-1]
                else:
                    self.field_value = str(self.field_value) + str(event.unicode)

                if self.validate() :
                    self.color = self.color_active if self.active else self.color_inactive
                    if self.callback_function != None :
                        self.callback_function(self.field_key)
                else : 
                    self.color = self.color_invalid if self.active else self.color_inactive

                # Re-render the text.
                self.txt_surface = self.font.render(str(self.field_value), True, self.color)

    #__________________________________________________________________________
    #
    # region update
    #__________________________________________________________________________
    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    #__________________________________________________________________________
    #
    # region draw
    #__________________________________________________________________________
    def draw(self, screen : pg.Surface):
        # black background
        pg.draw.rect(screen, (0,0,0), self.rect, 0)
        # Blit the text.
        x_start = self.rect.x + self.rect.width/2 - self.txt_surface.get_width()/2
        y_start = self.rect.y + self.rect.height/2 - self.txt_surface.get_height()/2 
        screen.blit(self.txt_surface, (x_start, y_start))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
