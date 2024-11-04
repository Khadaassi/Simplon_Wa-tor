from watorpygame.UserImageKey import UserImageKey
from watorpygame.UserImageProvider import Direction

class UserImageInfo:
    
    def __init__(self, image_key: UserImageKey = UserImageKey.WATER) -> None:
        self.image_key = image_key
        self.direction = Direction.NONE
    
    def set_direction(self, direction: str) -> None :
        if direction in "ND" :
            self.direction = Direction.NORTH
        elif direction in "SU":
            self.direction = Direction.SOUTH
        elif direction in "WR":
            self.direction = Direction.WEST
        elif direction in "EL":
            self.direction = Direction.EAST
            