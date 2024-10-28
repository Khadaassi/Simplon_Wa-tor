import os
import time
import matplotlib.pyplot as plt
from fish import Fish 
from fish import Shark
from world import World

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
    time.sleep(1) # Sleep for 1 second
    clear()

    while True: 
        if time.time() - start_t >= world.chronos_length: 
            counter += 1
            print_counter += 1       
            start_t = time.time()
            current_iteration += 1
            world.update_world()
            if print_counter == 100:
                clear()
                print("Current iteration : ", current_iteration)
                print_counter = 0
                world.print_grid()
                print(f"Fish pop : {world.fish_population} ; Shark pop : {world.shark_population}")
            fish_population.append(world.fish_population)
            shark_population.append(world.shark_population)
            iterations.append(current_iteration)
        if world.fish_population == 0 or world.shark_population == 0 or counter == 10000:
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

if __name__ == "__main__":
    main()
