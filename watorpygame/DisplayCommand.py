# standard imports
from enum import Enum

class DisplayCommand(Enum):
    RESET = 0
    GO = 1
    START = 2
    STEP = 3
    PAUSE = 4
    STOP = 5
    RESTART = 6
    EXIT = 7