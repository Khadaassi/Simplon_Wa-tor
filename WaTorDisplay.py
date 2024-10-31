
# Wa-Tor imports

from world import World
from fish import Fish, Shark, Megalodon, Megalodon_Tail
from watorpygame.DisplayState import DisplayState
from watorpygame.UserImageProvider import UserImageKey, UserImageProvider
from watorpygame.PygameWrapper import PygameWrapper
from watorpygame.UserImageInfo import UserImageInfo
from watorpygame.ConfigFields import ConfigFields

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
        if command == DisplayState.CONF:
            self.state = DisplayState.CONF
        
        elif command == DisplayState.WAIT:
            self.state = DisplayState.WAIT

        elif command == DisplayState.PLAY:
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

        self.pygameWrapper.set_state(self.state)

        if command_data != None :
            self.user_data = command_data

    #__________________________________________________________________________
    #
    # region display_conf_screen
    #__________________________________________________________________________
    def display_conf_screen(self, config_from_file:list) -> list:

        self.state = DisplayState.CONF
        self.pygameWrapper.set_state(self.state )

        #check config_from_file here
        assert len(config_from_file) == 11

        display_config = {}
        display_config[ConfigFields.FISH_POPULATION] = config_from_file[0]
        display_config[ConfigFields.SHARK_POPULATION]= config_from_file[1]
        display_config[ConfigFields.REFRESH_LENGTH] = config_from_file[2]
        display_config[ConfigFields.WORLD_WIDTH]= config_from_file[3]
        display_config[ConfigFields.WORD_HEIGTH] = config_from_file[4]
        display_config[ConfigFields.FISH_REPRO_TIME] = config_from_file[5]
        display_config[ConfigFields.SHARK_REPRO_TIME] = config_from_file[6]
        display_config[ConfigFields.SHARK_ENERGY] = config_from_file[7]
        display_config[ConfigFields.SHARK_ENERGY_GAIN]  = config_from_file[8]
        display_config[ConfigFields.ALLOW_MEGALODONS] = config_from_file[9]
        display_config[ConfigFields.MEGALODON_EVOLUTION_THRESHOLD] = config_from_file[10]
        
        self.pygameWrapper.set_data(display_config)
        self.pygameWrapper.initialize_screen()
        while True :
            if self.state != DisplayState.CONF :
                break
            
            self.pygameWrapper.draw(self.state)


        #while(self.state != DisplayState.WAIT) :
        conf = self.pygameWrapper.get_conf()
        returned_config = [0 for i in range(11)]
        returned_config[0] = conf[ConfigFields.FISH_POPULATION] 
        returned_config[1]= conf [ConfigFields.SHARK_POPULATION]
        returned_config[2] = conf[ConfigFields.REFRESH_LENGTH]
        returned_config[3]= conf[ConfigFields.WORLD_WIDTH]
        returned_config[4] = conf[ConfigFields.WORD_HEIGTH]
        returned_config[5] = conf[ConfigFields.FISH_REPRO_TIME]
        returned_config[6] = conf[ConfigFields.SHARK_REPRO_TIME] 
        returned_config[7] = conf[ConfigFields.SHARK_ENERGY]
        returned_config[8]  = conf[ConfigFields.SHARK_ENERGY_GAIN]
        returned_config[9] = conf[ConfigFields.ALLOW_MEGALODONS] 
        returned_config[10] = conf[ConfigFields.MEGALODON_EVOLUTION_THRESHOLD]
        

        return returned_config


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
                                   
                elif isinstance(item, Fish):
                    data[y_index][x_index] = UserImageInfo(UserImageKey.FISH)
                                                              
        self.pygameWrapper.set_data(data)
        self.pygameWrapper.draw(self.state)
