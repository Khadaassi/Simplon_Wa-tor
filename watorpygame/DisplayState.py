# standard imports
from enum import Enum

class DisplayState(Enum):
    CONF = 0
    WAIT = 1
    PLAY = 2
    PAUSE = 4
    STOP = 5
    OUT = 6
    BETWEEN = 7
