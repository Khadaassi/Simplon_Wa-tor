
# no standard imports
# no pygame imports

# 'root' Wa-Tor imports
from world import World
from fish import Fish, Shark, Megalodon, Megalodon_Tail
from pacman import Pacman
from ConfigField import ConfigField


# 'wrapped in a folder' Wa-Tor imports
from watorpygame.DisplayState import DisplayState
from watorpygame.DisplayCommand import DisplayCommand
from watorpygame.IterationInfo import IterationInfo
from watorpygame.UserImageKey import UserImageKey
from watorpygame.UserImageProvider import UserImageProvider
from watorpygame.UserImageInfo import UserImageInfo
from watorpygame.PygameWrapper import PygameWrapper

class WaTorDisplay:
    """
    A class to manage the pygame interface 
    and the user interaction.

    Properties
    ----------
    state : DisplayState
        the actual state of all views

    Methods
    -------
    update_config()
        Shows the configuration screen 

    get_config()
        returns the config dictionary updated by user

    update_view()
        Shows the play screen which displays each ne version of the world object

    stop()
        Stop the display and Shows the 'Restart button'
    
    """
    #__________________________________________________________________________
    #
    # region __init__
    #__________________________________________________________________________
    def __init__(self):
        self.__state = DisplayState.CONF
        self.__image_provider = UserImageProvider()
        self.__pygameWrapper = PygameWrapper(self.__image_provider, self.__on_user_command)
        self.__config = {}   
    
    #__________________________________________________________________________
    #
    # region __on_user_command
    #__________________________________________________________________________
    def __on_user_command(self, command: DisplayCommand):
        """
        changes the state of the display
        depending on the command
        udate the public variables 
        
        """

        if self.__state == DisplayState.OUT :
            return # we are closed, we don't take commands anymore

        match command :
            case DisplayCommand.RESET :
                self.__state = DisplayState.CONF
                self.__pygameWrapper.reset_config()

            case DisplayCommand.GO :
                # DisplayState.BETWEEN is the state 
                # between config screen (DisplayState.CONF) and play screen (DisplayState.WAIT)
                # only the call of UpdateView(world) makes the state change
                self.__state = DisplayState.BETWEEN 

            case DisplayCommand.START :
                self.__state = DisplayState.PLAY

            case DisplayCommand.STEP :
                # not implemented feature
                # self.__state = DisplayState.PAUSE
                pass

            case DisplayCommand.PAUSE: 
                if self.__state == DisplayState.PLAY: self.__state = DisplayState.PAUSE
                elif self.__state == DisplayState.PAUSE: self.__state = DisplayState.PLAY
                else: pass 

            case DisplayCommand.STOP:
                self.__state = DisplayState.STOP

            case DisplayCommand.RESTART:
                self.__state = DisplayState.CONF
                self.__pygameWrapper.set_state(self.__state)
                self.__pygameWrapper.set_data(self.__config)
   
            case DisplayCommand.EXIT:
                self.__state = DisplayState.OUT
                self.__pygameWrapper.running = False
                return

            case _ :
                self.__state = DisplayState.OUT

        if self.__state == DisplayState.OUT :
            return # we are closed i've told you

        self.__pygameWrapper.set_state(self.__state)

    #__________________________________________________________________________
    #
    # region state
    #__________________________________________________________________________
    @property
    def state(self) -> DisplayState :
        return self.__state

    #__________________________________________________________________________
    #
    # region update_config
    #__________________________________________________________________________
    def update_config(self, config_from_file: dict):
        
        if self.__state != DisplayState.CONF :
            return 

        self.__pygameWrapper.set_state(self.__state)
        
        assert len(config_from_file) == 13 # until it changes ... 
        # but if it changes, we will know it immediately

        if len(self.__config) == 0 :
            self.__config = config_from_file

        self.__pygameWrapper.set_data(self.__config)
        self.__pygameWrapper.draw(self.__state)

    #__________________________________________________________________________
    #
    # region get_config
    #__________________________________________________________________________
    def get_config(self):
        self.__config = self.__pygameWrapper.get_config()
        return self.__config

    #__________________________________________________________________________
    #
    # region update_view
    #__________________________________________________________________________
    def update_view(self, world: World):
        """
        Call this method when you want to display a new world on screen
        takes a world object which contains a list[list[Fish]]
        """

        if self.__pygameWrapper.running == False :
            return
        
        if self.__state in [DisplayState.CONF, DisplayState.OUT]:
            return
        
        if self.__state == DisplayState.BETWEEN :
            # First call of UpdateView(world) 
            # => makes the state change to DisplayState.WAIT
            self.__state = DisplayState.WAIT
            self.__pygameWrapper.set_state(self.__state)

        # corresponds to the height of screen 
        # it is the number of lines of the matrix
        assert len(world.grid) == world.size[1]

        # corresponds to the width of screen 
        # it is the number of columns of the first line of the matrix
        assert len(world.grid[0]) == world.size[0]

        data, iteration_info = self.__create_data_for_view(world)
                                               
        self.__pygameWrapper.set_data(data)
        self.__pygameWrapper.set_iteration_info(iteration_info)
        self.__pygameWrapper.draw(self.__state)

    #__________________________________________________________________________
    #
    # region stop
    #__________________________________________________________________________
    def stop(self) :
        """
        Call this method when there is no more world to compute
        (at the end of the 'While True')
        It will bring the view from the DisplayState.PLAY state
        to the DisplayState.STOP state, and show the 'Restart' button
        """
        self.__on_user_command(DisplayCommand.STOP)

    #__________________________________________________________________________
    #
    # region __create_data_for_view
    #__________________________________________________________________________
    def __create_data_for_view(self, world : World) -> tuple[list[list[UserImageInfo]], IterationInfo] :

        width = world.size[0]
        heigth = world.size[1]

        data = [[UserImageInfo(UserImageKey.WATER) for x in range(width)] for y in range(heigth)]
        for y_index in range(heigth):
            for x_index in range(width):
                item = world.grid[y_index][x_index]
                if not item:
                    continue

                if isinstance(item, Megalodon_Tail):
                    image_info = UserImageInfo(UserImageKey.MEGA_TAIL)                   
                    image_info.set_direction(item.current_direction)
                    data[y_index][x_index] = image_info                    
                    
                elif isinstance(item, Megalodon):
                    image_info = UserImageInfo(UserImageKey.MEGA_HEAD)
                    image_info.set_direction(item.current_direction)
                    data[y_index][x_index] = image_info
                    
                elif isinstance(item, Shark):
                    data[y_index][x_index] = UserImageInfo(UserImageKey.SHARK )    
                
                elif isinstance(item, Pacman):
                    data[y_index][x_index] = UserImageInfo(UserImageKey.PACMAN) 
                                   
                elif isinstance(item, Fish):
                    data[y_index][x_index] = UserImageInfo(UserImageKey.FISH)

        iteration_info = IterationInfo(
            world.world_age,
            world.fish_population,
            world.shark_population)
        
        if world.enable_megalodons :
            iteration_info.add_megalodons_info(world.megalodon_population)

        if world.enable_pacman :
            iteration_info.add_pacman_info(world.pacman_score)

        return data, iteration_info
 

if __name__ == "__main__":
    #put unit tests here
    pass