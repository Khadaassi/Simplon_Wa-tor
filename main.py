from fish import Fish 
from fish import Shark
from world import World
import os
import time

clear = lambda: os.system('clear')

def main():

    world = World((30, 10), 1, (30,20), 3, 3, 2, 2)
    world.populate_world()
    current_iteration = 0
    start_t = time.time()

    print("Initial World State:")
    world.print_grid()
    time.sleep(1)
    clear()

    while True: 
        if time.time() - start_t >= world.chronos_length:        
            start_t = time.time()
            current_iteration += 1
            clear()
            print("Current iteration : ", current_iteration)
            world.update_world()
            print(f"Fish pop : {world.fish_population} ; Shark pop : {world.shark_population}")
        if world.fish_population == 0 or world.shark_population == 0:
            break

if __name__ == "__main__":
    main()
