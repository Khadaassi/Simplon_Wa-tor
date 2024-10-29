# standard imports
from enum import Enum

# Wa-Tor imports
from wa_tor_image import WaTorImage

class WaTorImageKey(Enum):
    WATER = 0
    FISH = 1
    SHARK = 2
    MEGA_HEAD = 3
    MEGA_TAIL = 4

class WaTorImageProvider :
    def __init__(self):
        self.__images = {}
        self.__images[WaTorImageKey.FISH] = WaTorImage("images/Fish_image_1.png", "green", "darkgreen")
        self.__images[WaTorImageKey.SHARK] = WaTorImage("images/Shark_image_1.png", "red", "darkred")
        #self.images[WaTorImageKey.MEGA_HEAD] = UserImage("images/Shark_image_1.png", "white", "white")
        #self.images[WaTorImageKey.MEGA_TAIL] = UserImage("images/Shark_image_1.png", "white", "white")
    
    def get_image(self, image_key: WaTorImageKey) -> WaTorImage :
        return self.__images[image_key]
    
    def set_image(self, image_key: WaTorImageKey, userImage : WaTorImage):
        self.__images[image_key] = userImage
