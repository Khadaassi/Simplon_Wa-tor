# standard imports
from enum import Enum

class DisplayCommand(Enum):
    RESET = 0   # stay in DisplayState.CONF
    GO = 1      # from DisplayState.CONF to DisplayState.BETWEEN ( before DisplayState.WAIT ) 
    START = 2   # from DisplayState.WAIT to DisplayState.PLAY 
    PAUSE = 3   # altern between DisplayState.PAUSE and DisplayState.PLAY
    STOP = 4    # from all other states ... to DisplayState.STOP
    RESTART = 5 # from DisplayState.STOP to DisplayState.CONF
    EXIT = 6    # from all other states ... to DisplayState.OUT (the end of the display)