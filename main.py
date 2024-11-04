import os
import time

#from plot import plot_population
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
    while display.state == DisplayState.CONF :
        display.update_config(config)

    config = display.get_config()
    world = World((config[0], config[1]), config[2], (config[3], config[4]), config[5], config[6], config[7], config[8], config[9], config[10])
    world.populate_world()

    display.update_view(world, 0)  # create screen with the first world

    current_iteration = 0
    start_t = time.time()  # Start time
    fish_population = []  # List to store fish population
    shark_population = []  # List to store shark population
    megalodon_population = []  # List to store megalodon population

    iterations = []  # List to store iterations
    counter = 0


    print("Initial World State:")
    world.print_grid()
    time.sleep(1)  # Sleep for 1 second
    clear()

    while True:
        if display.state == DisplayState.STOP or display.state == DisplayState.OUT :
            break

        if display.state == DisplayState.WAIT or display.state == DisplayState.PAUSE:
            display.update_view(world, current_iteration)
            continue

        if time.time() - start_t >= world.chronos_length:
            counter += 1
            start_t = time.time()
            current_iteration += 1
            
            clear()
            print("Current iteration : ", current_iteration)
            world.update_world()
            display.update_view(world, current_iteration)  # update screen with the next world
            world.print_grid()
            print(
                f"Fish pop : {world.fish_population} ; Shark pop : {world.shark_population} ; Megalodon pop : {world.megalodon_population}; Pacman score : {world.pacman_score}"
            )
            fish_population.append(world.fish_population)
            shark_population.append(world.shark_population)
            megalodon_population.append(world.megalodon_population)
            iterations.append(current_iteration)

<<<<<<< HEAD
        if fish_population == 0 or shark_population == 0 or counter == 1000:
=======
        if world.fish_population == 0 or world.shark_population == 0 or counter == 100:
>>>>>>> d04d173c42376d07ee5c51ee96f284fced4c6db0
            break

    plot_population(iterations, fish_population, shark_population, megalodon_population)
    while display.state != DisplayState.OUT:
        display.update_view(world, current_iteration)


if __name__ == "__main__":
    main()
