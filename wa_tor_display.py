
# Wa-Tor imports

from world import World
from fish import Fish, Shark
from wa_tor_display_state import WaTorDisplayState
from wa_tor_image_provider import WaTorImageKey, WaTorImageProvider
from PygameWrapper import PygameWrapper

class WaTorDisplay:
    """
    A class to manage the pygame interface 
    and the user interaction.

    Attributes
    ----------
    state : DisplayState
        the actual state of all views.
    user_data : dict
        all the informations provided by the user

    Methods
    -------
    update_view()
        Update the data on the sreen

    on_user_command()
        set state variable 
        and possibly set the informations provided by the user
    
    """
    #__________________________________________________________________________
    #
    # region __init__
    #__________________________________________________________________________
    def __init__(self):
        self.state = WaTorDisplayState.WAIT
        self.image_provider = WaTorImageProvider()
        self.pygameWrapper = PygameWrapper(self.image_provider, self.on_user_command)
        self.user_data = {}   
    #__________________________________________________________________________
    #
    # region __init__
    #__________________________________________________________________________
    def on_user_command(self, command: WaTorDisplayState , command_data: dict =None):
        """
        update WatorDisplay instance variable : state
        optionally uses command_data object if provided
        """
        if command == WaTorDisplayState.PLAY: 
            self.state = WaTorDisplayState.PLAY

        elif command == WaTorDisplayState.PAUSE: 
            if self.state == WaTorDisplayState.PLAY: self.state = WaTorDisplayState.PAUSE
            elif self.state == WaTorDisplayState.PAUSE: self.state = WaTorDisplayState.PLAY
            else: pass

        elif command == WaTorDisplayState.STOP:
            self.state = WaTorDisplayState.STOP

        elif command == WaTorDisplayState.OUT:
            self.state = WaTorDisplayState.OUT

        else:
            self.state = WaTorDisplayState.OUT

        if command_data != None :
            self.user_data = command_data

    #__________________________________________________________________________
    #
    # region update_view
    #__________________________________________________________________________
    def update_view(self, world: World):
        """
        Takes a world object which contains a list[list[Fish]]
        """
        self.world = world

        # assert len(self.world.grid[0])  == self.world.size[0]
        # assert len(self.world.grid) == self.world.size[1]

        width = self.world.size[0]
        heigth = self.world.size[1]

        data = [[WaTorImageKey.WATER for x in range(width)] for y in range(heigth)]
        for y_index in range(heigth):
            for x_index in range(width):
                item = self.world.grid[y_index][x_index]
                if not item:
                    continue

                if isinstance(item, Fish):
                    data[y_index][x_index] = WaTorImageKey.FISH
                                                                 
                if isinstance(item, Shark):
                    data[y_index][x_index] = WaTorImageKey.SHARK
                                                                 
        self.pygameWrapper.set_data(data)
        self.pygameWrapper.draw()
