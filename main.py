from fish import Fish 
from fish import Shark
from world import World
import os
import time
import matplotlib.pyplot as plt

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')

def main():

    world = World((40, 20), 0.5, (20,10), 3, 3, 2, 2)
    world.populate_world()
    current_iteration = 0
    start_t = time.time()
    fish_population = []
    shark_population = []
    iterations = []
    counter = 0

    print("Initial World State:")
    world.print_grid()
    time.sleep(1)
    clear()

    while True: 
        if time.time() - start_t >= world.chronos_length: 
            counter += 1       
            start_t = time.time()
            current_iteration += 1
            clear()
            print("Current iteration : ", current_iteration)
            world.update_world()
            print(f"Fish pop : {world.fish_population} ; Shark pop : {world.shark_population}")
            fish_population.append(world.fish_population)
            shark_population.append(world.shark_population)
            iterations.append(current_iteration)
        if world.fish_population == 0 or world.shark_population == 0 or counter == 80:
            break

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
