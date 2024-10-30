from watorpygame.UserImageProvider import UserImageKey

class UserImageInfo:
    
    def __init__(self, image_key: UserImageKey = UserImageKey.WATER) -> None:
        self.image_key = image_key
        self.direction = ""