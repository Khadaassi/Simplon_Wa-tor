
# Wa-Tor imports

from world import World
from fish import Fish, Shark
from DisplayState import DisplayState
from watorpygame.UserImageProvider import UserImageKey, UserImageProvider
from watorpygame.PygameWrapper import PygameWrapper

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
        self.state = DisplayState.WAIT
        self.image_provider = UserImageProvider()
        self.pygameWrapper = PygameWrapper(self.image_provider, self.on_user_command)
        self.user_data = {}   
    #__________________________________________________________________________
    #
    # region on_user_command
    #__________________________________________________________________________
    def on_user_command(self, command: DisplayState , command_data: dict =None):
        """
        update WatorDisplay instance variable : state
        optionally uses command_data object if provided
        """
        if command == DisplayState.PLAY: 
            self.state = DisplayState.PLAY

        elif command == DisplayState.PAUSE: 
            if self.state == DisplayState.PLAY: self.state = DisplayState.PAUSE
            elif self.state == DisplayState.PAUSE: self.state = DisplayState.PLAY
            else: pass

        elif command == DisplayState.STOP:
            self.state = DisplayState.STOP

        elif command == DisplayState.OUT:
            self.state = DisplayState.OUT

        else:
            self.state = DisplayState.OUT

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

        data = [[UserImageKey.WATER for x in range(width)] for y in range(heigth)]
        for y_index in range(heigth):
            for x_index in range(width):
                item = self.world.grid[y_index][x_index]
                if not item:
                    continue

                if isinstance(item, Fish):
                    data[y_index][x_index] = UserImageKey.FISH
                                                                 
                if isinstance(item, Shark):
                    data[y_index][x_index] = UserImageKey.SHARK
                                                                 
        self.pygameWrapper.set_data(data)
        self.pygameWrapper.draw()
