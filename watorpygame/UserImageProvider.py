# Wa-Tor imports
from watorpygame.UserImage import UserImage
from watorpygame.UserImageKey import UserImageKey


class UserImageProvider :
    def __init__(self):
        self.__images = {}
        self.__images[UserImageKey.FISH] = UserImage("images/Fish_image_1.png", "green", "darkgreen")
        self.__images[UserImageKey.SHARK] = UserImage("images/Shark_image_1.png", "red", "darkred")
        self.__images[UserImageKey.MEGA_HEAD] = UserImage("images/mega_head.png", "purple", "magenta")
        self.__images[UserImageKey.MEGA_TAIL] = UserImage("images/mega_tail.png", "purple", "magenta")
        self.__images[UserImageKey.PROJECT] = UserImage("images/Img-wator.png", "green", "darkgreen")
    
    def get_image(self, image_key: UserImageKey) -> UserImage :
        return self.__images[image_key]
    
    def set_image(self, image_key: UserImageKey, userImage : UserImage):
        self.__images[image_key] = userImage
