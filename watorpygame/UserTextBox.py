import pygame as pg
#from watorpygame.WaTorColors import *

COLOR_INACTIVE = pg.Color((128, 0, 128))
COLOR_INVALID = pg.Color((192, 64, 64))
COLOR_ACTIVE = pg.Color((128, 255, 0))

class UserTextBox:

    def __init__(self, x, y, w, h, font : pg.font.Font, text=" "):
        self.rect = pg.Rect(x, y, w, h)
        #font = pg.font.Font(None, 30)
       #self.colors = WatorColors()
        self.color  = COLOR_INACTIVE
        self.text = text
        self.txt_surface = font.render( str(self.text), True, self.color)
        self.active = False

    def get_rect(self) -> pg.Rect :
        return self.rect

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

                try :
                    val = int(self.text)
                    self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
                except:
                    self.color = COLOR_INVALID if self.active else COLOR_INACTIVE

                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        x_start = self.rect.x + self.rect.width/2 - self.txt_surface.get_width()/2
        y_start = self.rect.y + self.rect.height/2 - self.txt_surface.get_height()/2 
        screen.blit(self.txt_surface, (x_start, y_start))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)
