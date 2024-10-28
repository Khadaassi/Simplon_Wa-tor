from PygameWrapper import PygameWrapper
from world import World
from fish import Fish, Shark

class WaTorDisplay:
    """
        Management of the pygame interface
    """
    def __init__(self, app_object):
        """
            When instanciated, the object starts a pygame
            needs a app_object which have got three methods : 
                app_object.start()
                app_object.pause()
                app_object.stop()
        """
        self.mainObject = app_object
        self.pygameWrapper = PygameWrapper()

    def update_view(self, world : World):
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

        image_tab  = [ ['~' for x in range(width)] for y in range(heigth)]
        for y_index in range(heigth):
            for x_index in range(width):
                item = self.world.grid[y_index][x_index]
                if not item :
                    continue

                if isinstance(item, Fish) :
                    image_tab[y_index][x_index] = self.pygameWrapper.fish_image

                if isinstance(item, Shark) :
                    image_tab[y_index][x_index] = self.pygameWrapper.shark_image


        self.pygameWrapper.set_tab(image_tab)
        self.pygameWrapper.show()
