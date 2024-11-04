# standard imports
from enum import Enum
from typing import cast
import pygame

# Wa-Tor imports
from watorpygame.UserImage import UserImage
from watorpygame.UserImageKey import UserImageKey


class Direction(Enum):
    NONE = ""
    NORTH = "ND"
    SOUTH = "SU"
    WEST = "WR"
    EAST = "EL"
    
class UserImageProvider :
    
    light_color = (0, 0, 255)
    dark_color = (0, 0, 255)
    
    def __init__(self, width: int = 0, height: int = 0):
        self.__images = {}
        self.__width = width
        self.__height = height
        self.__images[UserImageKey.PROJECT] = UserImage("images/Img-wator.png",  self.light_color, self.dark_color)
        self.__images[UserImageKey.FISH] = UserImage("images/Fish_image_1.png", self.light_color, self.dark_color)
        self.__images[UserImageKey.SHARK] = UserImage("images/Shark_image_1.png", self.light_color, self.dark_color)
        
        for item in self.__images.values():
            item.define_dimensions(self.__width, self.__height)
        
        self.__images[UserImageKey.MEGA_HEAD] = []
        self.__images[UserImageKey.MEGA_TAIL] = []
        self.__images[UserImageKey.PACMAN] = []
                
        #If entity need directional representation, make all the relevant directions
        for image_key in self.__images.keys() :
            if image_key in [UserImageKey.MEGA_HEAD, UserImageKey.MEGA_TAIL] :
                self.__images[image_key] = self.generate_images(image_key)
            if image_key in [UserImageKey.PACMAN]:
                self.__images[image_key] = self.generate_images(image_key)
        
        
                
                
    def generate_images(self, image_key : UserImageKey):
        """ 
        Generate directional version of an image.
        """
        
        results = []
        
        if image_key == UserImageKey.PACMAN:
            results.append(UserImage((f"images/pacman_close.png"), self.dark_color, self.dark_color))
            results.append(UserImage((f"images/pacman_open.png"), self.dark_color, self.dark_color))
            results[0].define_dimensions(self.__width, self.__height)
            results[1].define_dimensions(self.__width, self.__height)
            return results
        
        #Make 4 copies of base image. results[0] will be the base image.
        results = [UserImage((f"images/{image_key.name}.png".lower()), self.dark_color, self.dark_color) for x in range(0, 4)]
        #Resize the standard copy
        results[0].define_dimensions(self.__width, self.__height)
        #Make a copy rotated 90° clockwise
        results[1].resized = pygame.transform.rotate(results[1].resized, -90.0)
        results[1].define_dimensions(self.__width, self.__height)
        #Make a copy rotated 90° counter-clockwise
        results[2].resized = pygame.transform.rotate(results[2].resized, 90.0)
        results[2].define_dimensions(self.__width, self.__height)
        #Make a copy fliped on the x-axis.
        results[3].resized = pygame.transform.flip(results[3].resized, True, False)
        results[3].define_dimensions(self.__width, self.__height)
        return results
    
    def get_image(self, image_key: UserImageKey, orientation: Direction = Direction.NONE, pacman_status: int = -1) -> UserImage :
        
        #Get the direction version of image
        if orientation != Direction.NONE :
            if orientation == Direction.NORTH:
                return self.__images[image_key][1]  
            if orientation == Direction.SOUTH:
                return self.__images[image_key][2]  
            if orientation == Direction.WEST:
                return self.__images[image_key][0]  
            if orientation == Direction.EAST:
                return self.__images[image_key][3]  
            
        #Get Pacman image based on current iteration
        match pacman_status:
            case 0:                
                return self.__images[image_key][0]
            case 1:
                return self.__images[image_key][1]
            case -1 | _:
                pass
            
        #If no direction is needed, return the base image.    
        return self.__images[image_key]
          
    
    # def set_image(self, image_key: UserImageKey, userImage : UserImage, orientation: Direction = Direction.NONE):
    #     if orientation != Direction.NONE :
    #         if orientation == Direction.NORTH:
    #             self.__images[image_key][1] = userImage  
    #         if orientation == Direction.SOUTH:
    #             self.__images[image_key][2] = userImage 
    #         if orientation == Direction.WEST:
    #             self.__images[image_key][0] = userImage
    #         if orientation == Direction.EAST:
    #             self.__images[image_key][3] = userImage
    #     else:
    #         self.__images[image_key] = userImage
