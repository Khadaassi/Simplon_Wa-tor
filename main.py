import os
import time
import matplotlib.pyplot as plt
from fish import Fish 
from fish import Shark
from world import World
from WaTorDisplay import *


clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """
    Main function to run the simulation
    """
    world = World((100, 50), 0.5, (20,15), 3, 3, 2, 2)
    world.populate_world()
    current_iteration = 0
    start_t = time.time() # Start time
    fish_population = [] # List to store fish population
    shark_population = [] # List to store shark population
    iterations = [] # List to store iterations
    counter = 0

    
    print("Initial World State:")
    world.print_grid()

    #________________________
    # NCA {
    display = WaTorDisplay() # initialize View
    display.update_view(world) # create screen with the first world
    # }
    
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
            start_t = time.time()
            current_iteration += 1
            clear()
            print("Current iteration : ", current_iteration)

            #________________________
            # NCA {
            world.update_world()
            display.update_view(world) # update screen with the next world
            # }
        
            world.print_grid()
            print(f"Fish pop : {world.fish_population} ; Shark pop : {world.shark_population}")
            fish_population.append(world.fish_population)
            shark_population.append(world.shark_population)
            iterations.append(current_iteration)

        if world.fish_population == 0 or world.shark_population == 0 or counter == 100:
            break

        

# Plotting the population changes of fish and sharks over time

    plt.figure(figsize=(10, 6))
    plt.plot(iterations, fish_population, label='Fish Population', color='blue')
    plt.plot(iterations, shark_population, label='Shark Population', color='red')
    plt.xlabel('Iteration')
    plt.ylabel('Population')
    plt.title('Population Changes of Fish and Sharks Over Time')
    plt.legend()
    plt.show()

    while display.state != DisplayState.OUT : display.update_view(world)



if __name__ == "__main__":
    main()
