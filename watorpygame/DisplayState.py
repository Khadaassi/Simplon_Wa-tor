# standard imports
from enum import Enum

class DisplayState(Enum):
    CONF = 0
    BETWEEN = 1
    WAIT = 2
    PLAY = 3
    PAUSE = 4
    STOP = 5
    OUT = 6

