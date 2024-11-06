import os
import time

from world import World
from pacman import Pacman
from configfile import *
from consoleprint import console_print
from stats import *
from WaTorDisplay import WaTorDisplay
from watorpygame.DisplayState import DisplayState

clear = lambda: os.system("cls" if os.name == "nt" else "clear")

def main():
    """
    Main function to run the simulation
    """
    if not os.path.exists("config.ini"):
        write_config()

    config = read_config()
 
    display = WaTorDisplay()  # initialize View
    while display.state == DisplayState.CONF : # added to restart a new simulation at the end of the first one

        while display.state == DisplayState.CONF :
            display.update_config(config)

        config = display.get_config()
        world = World((config[ConfigField.FISH_POPULATION], config[ConfigField.SHARK_POPULATION]),
            config[ConfigField.REFRESH_LENGTH], 
            (config[ConfigField.WORLD_WIDTH], config[ConfigField.WORLD_HEIGTH]), 
            config[ConfigField.FISH_REPRO_TIME], config[ConfigField.SHARK_REPRO_TIME],
            config[ConfigField.SHARK_ENERGY], config[ConfigField.SHARK_ENERGY_GAIN],
            config[ConfigField.ALLOW_MEGALODONS], config[ConfigField.MEGALODON_EVOLUTION_THRESHOLD],
            config[ConfigField.ALLOW_PACMAN], config[ConfigField.ALLOW_STORMS])
        
        world.populate_world()
        
        if not display.state == DisplayState.OUT :
            display.update_view(world)  # create screen with the first world

        start_t = time.time()  # Start time

        fish_population = []  # List to store fish population
        shark_population = []  # List to store shark population
        megalodon_population = []  # List to store megalodon population
        iterations = []  # List to store iterations
        population_stats(fish_population, shark_population, megalodon_population, iterations, world)

        print("Initial World State:")
        world.print_grid()
        time.sleep(1)  # Sleep for 1 second
        clear()
        
        # Main loop
        while True:
            if display.state == DisplayState.STOP or display.state == DisplayState.OUT :
                break

            if display.state == DisplayState.WAIT or display.state == DisplayState.PAUSE:
                display.update_view(world)
                continue

            if time.time() - start_t >= world.chronos_length:
                start_t = time.time()
                
                clear()
                
                world.update_world()
                display.update_view(world)  # update screen with the next world
                
                #Console print
                #console_print(world)
                
                #Statistics appending
                population_stats(fish_population, shark_population, megalodon_population, iterations, world)
                
            if world.fish_population == 0 or world.shark_population == 0 or world.world_age == config[ConfigField.MAX_ITERATION]:
                break

        display.stop() # tells display there is no more world to show 

        # function to plot the population of fish and sharks
        # plot_population(iterations, fish_population, shark_population, megalodon_population)
       
        # keep the screen visible while user don't quit the pygame window (or click on 'Exit') 
        while display.state not in [DisplayState.CONF, DisplayState.OUT] :
            display.update_view(world)
      
if __name__ == "__main__":
    main()
