from random import randint
import os
import time
clear = lambda: os.system("clear")


class World:
    
    def __init__(self, s_pop: tuple[int, int], chro_len: int, world_size: tuple[int, int], fish_repro_time: int, shark_repro_time: int,\
        shark_energy: int, shark_energy_gain: int) -> None:
        """
        [Args]\n
        s_pop = a tuple of int containing the starting population of fishes and sharks, respectively
        chro_len = the length of a chronos for this world
        world_size = a tuple of int defining the world dimension as follow [width, height]
        fish_repro_time = the amount of chronos a fish needs to reproduce
        shark_repro_time = the amount of chronos a shark needs to reproduce
        shark_energy = starting energy of a newly created shark
        shark_energy_gain = amount of energy a shark gains when eating a fish"""
        
        self.starting_population = s_pop #The initial ratio of fish to shark. starting_population[0] = fishes, starting_population[1] = sharks
        self.chronos_length = chro_len #The amount of iterations of the loop necessary before the next chronos start
        self.size = world_size #The size of the world (= the size of the grid)
        self.fish_reproduction_time = fish_repro_time #The amount of chronos a fish needs to stay alive before producing a new fish
        self.shark_reproduction_time = shark_repro_time #The amount of chronos a fish needs to stay alive before producing a new shark
        self.grid = [] #The actual world. A list of lists holding, fish, sharks or FALSE(water) to simulate a grid view.
        self.current_fish_population = self.starting_population[0] #The current amount of fishes in the world
        self.current_shark_population = self.starting_population[1] #The current amount of sharks in the world
        self.shark_energy = shark_energy #The starting energy of a shark.  
        self.shark_energy_gained_by_eating = shark_energy_gain #The amount of energy a shark gains when eating a fish
        
        #Cannot create a world smaller than total starting population
        if (sum(self.starting_population)) > self.size[0]*self.size[1]:
            raise ValueError("Total population too big : try increasing world size or reducing populations")
        
        
    def populate_world(self) -> None:
        """
        Populate the first state of the world by placing fishes and sharks randomly in the grid.
        """
        
        #Reset the grid
        self.grid = [] 
        
        #Get buffer values for fishes and sharks
        fishes = self.starting_population[0]
        sharks = self.starting_population[1]
        
        #Fill the grid with water
        for x in range(0, self.size[1]):
            self.grid.append([])
            for y in range(0, self.size[0]):
                self.grid[x].append("~")            
        
        #Place the fishes randomly
        while fishes > 0:
            x, y = self.get_empty_grid_space()
            self.grid[x][y] = "O"            
            fishes -= 1
        
        #Place the sharks randomly
        while sharks > 0:
            x, y = self.get_empty_grid_space()
            self.grid[x][y] = "X"            
            sharks -= 1  
        
    def update_world(self) -> None:
        #Move everything
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid[x])):
                direction = self.get_direction(x, y)
                if direction == "":
                    continue
                direction = direction[randint(0, len(direction)-1)]
                if direction == "N":
                    self.grid[x-1][y] = self.grid[x][y]
                    self.grid[x][y] = "~"
                if direction == "S":
                    self.grid[x+1][y] = self.grid[x][y]
                    self.grid[x][y] = "~"
                if direction == "W":
                    self.grid[x][y-1] = self.grid[x][y]
                    self.grid[x][y] = "~"
                if direction == "E":
                    self.grid[x][y+1] = self.grid[x][y]
                    self.grid[x][y] = "~"
        
        self.print_grid()
        
        
                
                 
        
    def get_empty_grid_space(self) -> int:
        """
        Return the coordinates of a random empty space in the grid as two int x and y.
        """
        
        #Loop through random coordinates until one water tile is found
        found_suitable_space = False
        while not found_suitable_space:
            x = randint(0, self.size[1]-1)
            y = randint(0, self.size[0]-1)
            if self.grid[x][y] == "~":
                found_suitable_space = True
        return x, y

    

    def print_grid(self) -> None: 
        """
        Print the state of the world in the console.
        """       
        for x in self.grid:
            line = "| "
            for y in x:
                line += f"[{y}]"
            line += " |"
            print(line)
    
    
    def get_direction(self, x: int, y: int) -> str:
        outcomes = ""
        fish = True
        
        if fish:
            #TODO: gérer les bords
            #Check for North availlable
            if x == 0 or x == len(self.grid)-1 or y == len(self.grid[0])-1 or y == 0:
                return ""
            if self.grid[x-1][y] == "~":
                outcomes += "N"
            #Check for South availlable
            if self.grid[x+1][y] == "~":
                outcomes += "S"
            #Check for West availlable
            if self.grid[x][y-1] == "~":
                outcomes += "W"
            #check for East availlabke
            if self.grid[x][y+1] == "~":
                outcomes += "E"
        else:
            pass
        
        return outcomes
                     
        
    
    
my_world = World((2, 0), 3, (5, 5), 10, 10, 5, 5)
my_world.populate_world()
max_loop = 5
current_loop = 0
compteur = 0
start_t = time.time()
my_world.print_grid()
clear()
while current_loop < max_loop: 
    if time.time() - start_t >= my_world.chronos_length:        
        start_t = time.time()
        current_loop += 1
        clear()
        print("current loop : ", current_loop)
        my_world.update_world()

print("END OF SIMULATION")
    