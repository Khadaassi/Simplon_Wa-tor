from PygameWrapper import PygameWrapper
from world import World
from fish import Fish, Shark, Megalodon, Megalodon_Tail
from enum import Enum


class DisplayState(Enum):
    WAIT = 0
    PLAY = 1
    PAUSE = 2
    STOP = 3
    OUT = 4


class WaTorDisplay:
    """
    Management of the pygame interface
    """

    def __init__(self, app_object=None):
        """
        When instanciated, the object starts a pygame
        needs a app_object which have got three methods :
            app_object.start()
            app_object.pause()
            app_object.stop()
        """
        self.mainObject = app_object
        self.pygameWrapper = PygameWrapper(self.on_user_command)
        self.state = DisplayState.WAIT

    def on_user_command(self, command: str):
        # print(f"Button {command} clicked from a function !")
        if command == "Start":
            self.state = DisplayState.PLAY
        elif command == "Pause":
            if self.state == DisplayState.PLAY:
                self.state = DisplayState.PAUSE
            elif self.state == DisplayState.PAUSE:
                self.state = DisplayState.PLAY
            else:
                pass
        elif command == "Stop":
            self.state = DisplayState.STOP
        elif command == "Quit":
            self.state = DisplayState.OUT
        else:
            self.state = DisplayState.OUT

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
                    
                if isinstance(item, Megalodon):
                    image_tab[y_index][x_index] = self.pygameWrapper.mega_head_image
                    
                if isinstance(item, Megalodon_Tail):
                    image_tab[y_index][x_index] = self.pygameWrapper.mega_tail_image
                    

        self.pygameWrapper.set_tab(image_tab)
        self.pygameWrapper.draw()
