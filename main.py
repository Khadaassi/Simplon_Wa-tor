from fish import Fish 
from fish import Shark
from world import World
import os
import time

clear = lambda: os.system('clear')

def main():
    pass

my_world = World((30, 0), 1, (20,10), 10, 10, 5, 5)
my_world.populate_world()
max_iteration = 10
current_iteration = 0
compteur = 0
start_t = time.time()
my_world.print_grid()
clear()
print("current iteration : ", current_iteration)
my_world.print_grid()

while True: 
    if time.time() - start_t >= my_world.chronos_length:        
        start_t = time.time()
        current_iteration += 1
        clear()
        print("current iteration : ", current_iteration)
        my_world.update_world()
        
if __name__ == "__main__":
    main()
