
# Wa-Tor imports

from world import World
from fish import Fish, Shark, Megalodon, Megalodon_Tail
from pacman import Pacman
from watorpygame.IterationInfo import IterationInfo

from watorpygame.DisplayCommand import DisplayCommand
from watorpygame.DisplayState import DisplayState

from watorpygame.UserImageKey import UserImageKey
from watorpygame.UserImageProvider import UserImageProvider
from watorpygame.UserImageInfo import UserImageInfo
from ConfigField import ConfigField



from watorpygame.PygameWrapper import PygameWrapper

import pygame

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
    def __init__(self, state : DisplayState = DisplayState.WAIT):
        self.state = state
        self.image_provider = UserImageProvider()
        self.pygameWrapper = PygameWrapper(self.image_provider, self.on_user_command)
        self.__config = {}   
    #__________________________________________________________________________
    #
    # region on_user_command
    #__________________________________________________________________________
    def on_user_command(self, command: DisplayCommand, command_data: dict = None):
        """
        update WatorDisplay instance variable : state
        optionally uses command_data object if provided
        """

        if self.state == DisplayState.OUT :
            return # we are closed, we don't take commands anymore

        precedent_state = self.state
        match command :
            case DisplayCommand.RESET :
                self.state = DisplayState.CONF
                self.pygameWrapper.reset_config()

            case DisplayCommand.GO :
                self.state = DisplayState.BETWEEN # state between config screen and play screen
                self.pygameWrapper.disable_textboxes()

            case DisplayCommand.START :
                self.state = DisplayState.PLAY

            # not implemented feature
            # case DisplayCommand.STEP :
            #     self.state = DisplayState.PAUSE

            case DisplayCommand.PAUSE: 
                if self.state == DisplayState.PLAY: self.state = DisplayState.PAUSE
                elif self.state == DisplayState.PAUSE: self.state = DisplayState.PLAY
                else: pass 

            case DisplayCommand.STOP:
                self.state = DisplayState.STOP

            case DisplayCommand.RESTART:
                self.state = DisplayState.CONF
                self.pygameWrapper.set_state(self.state)
                self.pygameWrapper.set_data(self.__config)
   
            case DisplayCommand.EXIT:
                self.state = DisplayState.OUT
                self.pygameWrapper.running = False
                return

            case _ :
                self.state = DisplayState.OUT

        if self.state == DisplayState.OUT :
            return # we are closed i've told you

        self.pygameWrapper.set_state(self.state)
        if self.state != precedent_state :
            self.pygameWrapper.initialize_buttons()

        if command_data != None :           #not used code 
            self.user_data = command_data   #not used code

    
    #__________________________________________________________________________
    #
    # region _get_config_dict
    #__________________________________________________________________________
    def __get_config_dict(self, config_from_file:list) -> dict:

        #check config_from_file here
        assert len(config_from_file) == 13

        display_config = config_from_file
        # display_config[ConfigField.FISH_POPULATION] = config_from_file[0]
        # display_config[ConfigField.SHARK_POPULATION] = config_from_file[1]
        # display_config[ConfigField.REFRESH_LENGTH] = config_from_file[2]
        # display_config[ConfigField.WORLD_WIDTH] = config_from_file[3]
        # display_config[ConfigField.WORD_HEIGTH] = config_from_file[4]
        # display_config[ConfigField.FISH_REPRO_TIME] = config_from_file[5]
        # display_config[ConfigField.SHARK_REPRO_TIME] = config_from_file[6]
        # display_config[ConfigField.SHARK_ENERGY] = config_from_file[7]
        # display_config[ConfigField.SHARK_ENERGY_GAIN]  = config_from_file[8]
        # display_config[ConfigField.ALLOW_MEGALODONS] = config_from_file[9]
        # display_config[ConfigField.MEGALODON_EVOLUTION_THRESHOLD] = config_from_file[10]
        # display_config[ConfigField.ALLOW_PACMAN] = config_from_file[11]
        
        return display_config
            
    #__________________________________________________________________________
    #
    # region get_config
    #__________________________________________________________________________
    def get_config(self) -> list :
        self.__config = self.pygameWrapper.get_config()
        
        # config_list = [0 for i in range(12)]
        # config_list[0] = self.__config[ConfigField.FISH_POPULATION] 
        # config_list[1] = self.__config [ConfigField.SHARK_POPULATION]
        # config_list[2] = self.__config[ConfigField.REFRESH_LENGTH]
        # config_list[3] = self.__config[ConfigField.WORLD_WIDTH]
        # config_list[4] = self.__config[ConfigField.WORD_HEIGTH]
        # config_list[5] = self.__config[ConfigField.FISH_REPRO_TIME]
        # config_list[6] = self.__config[ConfigField.SHARK_REPRO_TIME] 
        # config_list[7] = self.__config[ConfigField.SHARK_ENERGY]
        # config_list[8] = self.__config[ConfigField.SHARK_ENERGY_GAIN]
        # config_list[9] = self.__config[ConfigField.ALLOW_MEGALODONS] 
        # config_list[10] = self.__config[ConfigField.MEGALODON_EVOLUTION_THRESHOLD]
        # config_list[11] = self.__config[ConfigField.ALLOW_PACMAN]
        
        return self.__config
    
    #__________________________________________________________________________
    #
    # region update_config
    #__________________________________________________________________________
    def update_config(self, config_from_file:list):
        
        self.state = DisplayState.CONF
        self.pygameWrapper.set_state(self.state)

        if len(self.__config) == 0 :
            self.__config = display_config = self.__get_config_dict(config_from_file)
            self.pygameWrapper.set_data(display_config)

        self.pygameWrapper.draw(self.state)

    #__________________________________________________________________________
    #
    # region update_view
    #__________________________________________________________________________
    def update_view(self, world: World):
        """
        Takes a world object which contains a list[list[Fish]]
        """

        if self.pygameWrapper.running == False :
            return

        self.world = world

        # assert len(self.world.grid[0])  == self.world.size[0]
        # assert len(self.world.grid) == self.world.size[1]

        width = self.world.size[0]
        heigth = self.world.size[1]

        iterationInfo = IterationInfo(
            world.world_age,
            world.fish_population,
            world.shark_population)
        
        if world.enable_megalodons :
            iterationInfo.add_megalodons_info(world.megalodon_population)

        if world.enable_pacman :
            iterationInfo.add_pacman_info(world.pacman_score)

        data = [[UserImageInfo(UserImageKey.WATER) for x in range(width)] for y in range(heigth)]
        for y_index in range(heigth):
            for x_index in range(width):
                item = self.world.grid[y_index][x_index]
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
                                                              
        self.pygameWrapper.set_data(data)
        self.pygameWrapper.set_info(iterationInfo)
        if self.state == DisplayState.BETWEEN :
            self.state = DisplayState.WAIT
            self.pygameWrapper.set_state(self.state)
            self.pygameWrapper.initialize_controls() # new controls (no textboxes, different buttons)

        self.pygameWrapper.draw(self.state)

    def this_is_the_end(self) :
        self.on_user_command(DisplayCommand.STOP)
        

if __name__ == "__main__":
    #put unit tests here
    pass