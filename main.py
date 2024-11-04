import os
import time

from plot import plot_population
from configfile import *
from world import World
from pacman import Pacman
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

    
    display = WaTorDisplay(DisplayState.CONF)  # initialize View
    while display.state == DisplayState.CONF : # added to restart a new simulation at the end of the first one

        while display.state == DisplayState.CONF :
            display.update_config(config)

        config = display.get_config()
        world = World( (config[ConfigField.FISH_POPULATION], config[ConfigField.SHARK_POPULATION]),
            config[ConfigField.REFRESH_LENGTH], 
            (config[ConfigField.WORLD_WIDTH], config[ConfigField.WORD_HEIGTH]), 
            config[ConfigField.FISH_REPRO_TIME], config[ConfigField.SHARK_REPRO_TIME],
            config[ConfigField.SHARK_ENERGY], config[ConfigField.SHARK_ENERGY_GAIN],
            config[ConfigField.ALLOW_MEGALODONS], config[ConfigField.MEGALODON_EVOLUTION_THRESHOLD],
            config[ConfigField.ALLOW_PACMAN])

        world.populate_world()
        
        if not display.state == DisplayState.OUT :
            display.update_view(world)  # create screen with the first world

        current_iteration = 0
        start_t = time.time()  # Start time
        fish_population = []  # List to store fish population
        shark_population = []  # List to store shark population
        megalodon_population = []  # List to store megalodon population

        iterations = []  # List to store iterations

        fish_ages = [] # List of dictionaries to store fish age pyramid
        shark_ages = []  # List of dictionaries to store shark age pyramid
        megalodon_ages = []  # List of dictionaries to store megalodon age pyramid


        counter = 0


        print("Initial World State:")
        world.print_grid()
        time.sleep(1)  # Sleep for 1 second
        clear()

        while True:
            if display.state == DisplayState.STOP or display.state == DisplayState.OUT :
                break

            if display.state == DisplayState.WAIT or display.state == DisplayState.PAUSE:
                display.update_view(world)
                continue

            if time.time() - start_t >= world.chronos_length:
                counter += 1
                start_t = time.time()
                current_iteration += 1
                
                clear()
                
                world.update_world()
                display.update_view(world)  # update screen with the next world
                
                #Console print
                # console_print(world)
                
                #Statistics appending
                fish_population.append(world.fish_population)
                shark_population.append(world.shark_population)
                megalodon_population.append(world.megalodon_population)
                iterations.append(current_iteration)

                fish_ages.append(world.fish_age_dict)
                shark_ages.append(world.shark_age_dict)
                megalodon_ages.append(world.megalodon_age_dict)
                
            if world.fish_population == 0 or world.shark_population == 0 or counter == config[ConfigField.MAX_ITERATION]:
                break

        display.there_is_no_more_data() # tells display there is no more world to show 

        plot_population(iterations, fish_population, shark_population, megalodon_population)
        
        print( world.fish_age_dict[0])
        print( world.shark_age_dict[0])
        print( world.megalodon_age_dict[0])
        
        while display.state not in [DisplayState.CONF, DisplayState.OUT] :
            display.update_view(world)

        

    


def console_print(world: World) -> None:
    print("Current iteration : ", world.world_age)
    world.print_grid()
    print(
        f"Fish pop : {world.fish_population} ; Shark pop : {world.shark_population} ; Megalodon pop : {world.megalodon_population}; Pacman score : {world.pacman_score}"
        )

if __name__ == "__main__":
    main()
