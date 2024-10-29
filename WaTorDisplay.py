from PygameWrapper import PygameWrapper
from world import World
from fish import Fish, Shark
from DisplayState import DisplayState

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

    def __init__(self):
        self.state = DisplayState.WAIT
        self.pygameWrapper = PygameWrapper(self.on_user_command)
        self.user_data = {}   

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


    def update_view(self, world: World):
        """
        Takes a world object which
          is a list[list[str]] object
          or contains a list[list[str]]
        in which  ashark is a 'X', a fish is a 'o', water is a '~'
        """
        self.world = world

        # assert len(self.world.grid[0])  == self.world.size[0]
        # assert len(self.world.grid) == self.world.size[1]

        width = self.world.size[0]
        heigth = self.world.size[1]

        image_tab = [["~" for x in range(width)] for y in range(heigth)]
        for y_index in range(heigth):
            for x_index in range(width):
                item = self.world.grid[y_index][x_index]
                if not item:
                    continue

                if isinstance(item, Fish):
                    image_tab[y_index][x_index] = self.pygameWrapper.fish_image

                if isinstance(item, Shark):
                    image_tab[y_index][x_index] = self.pygameWrapper.shark_image

        self.pygameWrapper.set_tab(image_tab)
        self.pygameWrapper.draw()
