import pygame

class UserImage :
    def __init__(self, png_filename: str) :
        self.image = pygame.image.load(png_filename)
        self.__proportion = self.image.get_width() / self.image.get_height()
        self.resized = self.image

    def define_dimensions (self, width: int, height: int):
        min_size = min(width, height)
        if self.image.get_width() > self.image.get_height() :
            image_width = min_size
            image_height = int(min_size/self.__proportion)
        else :
            image_width = int(min_size*self.__proportion)
            image_height = min_size

        self.resized = pygame.transform.scale( self.image, [image_width, image_height])
