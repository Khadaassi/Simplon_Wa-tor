import os
import time
from plot import plot_population 
from fish import Shark
from world import World
from WaTorDisplay import *


clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """
    Main function to run the simulation
    """


    world = World((500, 200), 0.001, (40,30), 3, 3, 2, 2)
    world.populate_world()
    current_iteration = 0
    start_t = time.time() # Start time
    fish_population = [] # List to store fish population
    shark_population = [] # List to store shark population
    iterations = [] # List to store iterations
    counter = 0
    print_counter = 0

    
    print("Initial World State:")
    world.print_grid()


    display = WaTorDisplay() # initialize View
    display.update_view(world) # create screen with the first world
    
    time.sleep(1) # Sleep for 1 second
    clear()

    while True: 
        if display.state == DisplayState.STOP : 
            break

        if display.state != DisplayState.PLAY or display.state == DisplayState.PAUSE: 
            display.update_view(world)
            continue

        if time.time() - start_t >= world.chronos_length: 
            counter += 1
            print_counter += 1       
            start_t = time.time()
            current_iteration += 1

            clear()
            print("Current iteration : ", current_iteration)
            world.update_world()
            display.update_view(world) # update screen with the next world
            world.print_grid()
            print(f"Fish pop : {world.fish_population} ; Shark pop : {world.shark_population}")
            fish_population.append(world.fish_population)
            shark_population.append(world.shark_population)
            iterations.append(current_iteration)

        if world.fish_population == 0 or world.shark_population == 0 or counter == 100:

            break

    plot_population(iterations, fish_population, shark_population)    
    while display.state != DisplayState.OUT : display.update_view(world)
 

if __name__ == "__main__":
    main()
