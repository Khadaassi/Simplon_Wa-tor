# standard imports
from enum import Enum

# Wa-Tor imports
from watorpygame.UserImage import UserImage

class UserImageKey(Enum):
    WATER = 0
    FISH = 1
    SHARK = 2
    MEGA_HEAD = 3
    MEGA_TAIL = 4

class UserImageProvider :
    def __init__(self):
        self.__images = {}
        self.__images[UserImageKey.FISH] = UserImage("images/Fish_image_1.png", "green", "darkgreen")
        self.__images[UserImageKey.SHARK] = UserImage("images/Shark_image_1.png", "red", "darkred")
        #self.images[UserImageKey.MEGA_HEAD] = UserImage("images/Shark_image_1.png", "white", "white")
        #self.images[UserImageKey.MEGA_TAIL] = UserImage("images/Shark_image_1.png", "white", "white")
    
    def get_image(self, image_key: UserImageKey) -> UserImage :
        return self.__images[image_key]
    
    def set_image(self, image_key: UserImageKey, userImage : UserImage):
        self.__images[image_key] = userImage
