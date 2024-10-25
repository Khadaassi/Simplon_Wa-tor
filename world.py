from random import randint


class World:
    
    def __init__(self, s_pop: tuple[int, int], chro_len: int, world_size: int, fish_repro_time: int, shark_repro_time: int) -> None:
        """
        [Args]\n
        s_pop = a tuple of int containing the starting population of fishes and sharks, respectively
        chro_len = the length of a chronos for this world
        world_size = the size of the grid (world)
        fish_repro_time = the amount of chronos a fish needs to reproduce
        shark_repro_time = the amount of chronos a shark needs to reproduce"""
        
        self.starting_population = s_pop #The initial ratio of fish to shark. starting_population[0] = fishes, starting_population[1] = sharks
        self.chronos_length = chro_len #The amount of iterations of the loop necessary before the next chronos start
        self.size = world_size #The size of the world (= the size of the grid)
        self.fish_reproduction_time = fish_repro_time #The amount of chronos a fish needs to stay alive before producing a new fish
        self.shark_reproduction_time = shark_repro_time #The amount of chronos a fish needs to stay alive before producing a new shark
        self.grid = [] #The actual world. A list of lists holding, fish, sharks or FALSE(water) to simulate a grid view.
        self.current_fish_population = self.starting_population[0] #The current amount of fishes in the world
        self.current_shark_population = self.starting_population[1] #The current amount of sharks in the world
        
        #Cannot create a world smaller than total starting population
        if (sum(self.starting_population)) > self.size*self.size:
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
        for x in range(0, self.size):
            self.grid.append([])
            for y in range(0, self.size):
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
        
        
    def get_empty_grid_space(self) -> int:
        """
        Return the coordinates of a random empty space in the grid as two int x and y.
        """
        
        #Loop through random coordinates until one water tile is found
        found_suitable_space = False
        while not found_suitable_space:
            x = randint(0, self.size-1)
            y = randint(0, self.size-1)
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
                
        
    
    
my_world = World((50, 70), 8, 25, 10, 10)
my_world.populate_world()
my_world.print_grid()