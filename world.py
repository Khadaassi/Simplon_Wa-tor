from fish import Fish
from fish import Shark
from fish import Megalodon
from fish import Megalodon_Tail
from random import randint

class World:
    
    def __init__(self, s_pop: tuple[int, int], chro_len: int, world_size: tuple[int, int], fish_repro_time: int, shark_repro_time: int,\
        shark_energy: int, shark_energy_gain: int, allow_megalodons: bool = True, megalodon_evolution_threshold: int = 5, shark_energy_depletion_rate: int = 1) -> None:
        """
        [Args]\n
        s_pop = a tuple of int containing the starting population of fishes and sharks, respectively
        chro_len = the length of a chronos for this world
        world_size = a tuple of int defining the world dimension as follow [width, height]
        fish_repro_time = the amount of chronos a fish needs to reproduce
        shark_repro_time = the amount of chronos a shark needs to reproduce
        shark_energy = starting energy of a newly created shark (also its maximum, if needed)
        shark_energy_gain = amount of energy a shark gains when eating a fish
        allow_megalodons = if False, sharks will never evolve to Megalodons"""
        
        #World parameters block
        self.starting_population = s_pop #The initial ratio of fish to shark. starting_population[0] = fishes, starting_population[1] = sharks
        self.chronos_length = chro_len #The amount of iterations of the loop necessary before the next chronos start
        self.size = world_size #The size of the world (= the size of the grid)
        self.fish_reproduction_time = fish_repro_time #The amount of chronos a fish needs to stay alive before producing a new fish
        self.shark_reproduction_time = shark_repro_time #The amount of chronos a fish needs to stay alive before producing a new shark
        self.grid = [] #The actual world. A list of lists holding, fishes, sharks or FALSE (water) to simulate a grid view.
        self.current_fish_population = self.starting_population[0] #The current amount of fishes in the world
        self.current_shark_population = self.starting_population[1] #The current amount of sharks in the world
        self.shark_energy = shark_energy #The starting energy of a shark.  
        self.shark_energy_gained_by_eating = shark_energy_gain #The amount of energy a shark gains when eating a fish
        self.shark_energy_depletion_rate = shark_energy_depletion_rate #The amount of energy lost when a shark moves. 1 by default.
        self.enable_megalodons = allow_megalodons #if False, Megalodons generation will be disabled.
        self.megalodon_evolution_threshold = megalodon_evolution_threshold #The amount of Fish a shark needs to eat before evolving to a Megalodon
        
        #Internal logic block
        self.next_move_will_eat = False
        
        #Stats block
        self.fish_population = self.starting_population[0]
        self.shark_population = self.starting_population[1]
        self.megalodon_population = 0
        
        #DEBUG block
        self.megalodon_starting_population = 0 #Force the presence of X megalodons on the starting world.
        
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
        mega = self.megalodon_starting_population
        
        #Fill the grid with water
        for x in range(0, self.size[1]):
            self.grid.append([])
            for y in range(0, self.size[0]):
                self.grid[x].append(False)            
        
        #Place the fishes randomly
        while fishes > 0:
            x, y = self.get_empty_grid_space()
            self.grid[x][y] = Fish(self.fish_reproduction_time)            
            fishes -= 1
        
        #Place the sharks randomly
        while sharks > 0:
            x, y = self.get_empty_grid_space()
            self.grid[x][y] = Shark(self.shark_reproduction_time, self.shark_energy, self.megalodon_evolution_threshold)            
            sharks -= 1  
        
        #Place the megalodons randomly
        #DEPRECATED : Megalodons shouldn't be manually placed during world generation. They should only appear from evolving sharks.
        while mega > 0:
            x, y = self.get_empty_grid_space()
            self.grid[x][y] = Megalodon(self.shark_reproduction_time, self.shark_energy, self.megalodon_evolution_threshold)            
            mega -= 1 
        
    def update_world(self) -> None:
        """
        Update the world state and the state of every entity in the grid. (Movement, reproduction, death)
        """
        
        #Move everything
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid[x])):
                
                #skip water tiles
                if self.grid[x][y] == False:
                    continue
                
                #Skip fishes that have already moved or ar Megalodon tails
                if self.grid[x][y].has_moved or isinstance(self.grid[x][y], Megalodon_Tail):
                    continue
                
                #Set parameters for next entity
                self.next_move_will_eat = False
                isMegalodon = isinstance(self.grid[x][y], Megalodon) and not isinstance(self.grid[x][y], Megalodon_Tail)
                isShark = isinstance(self.grid[x][y], Shark) and not isinstance(self.grid[x][y], Megalodon) and not isinstance(self.grid[x][y], Megalodon_Tail)
                self.grid[x][y].has_moved = True                
                will_reproduce = self.grid[x][y].reproduce()   
                will_die = False        
                
                #Get the availlable directions for current entity    
                direction = self.get_shark_directions(x, y) if isShark else self.get_megalodons_directions(x, y) if isMegalodon \
                    else self.get_fish_direction(x, y)
                
                #If no legal movement, continue the loop
                if direction == "":
                    continue
                
                #Get one direction randomly among all availlable direction
                direction = direction[randint(0, len(direction)-1)]                
                
                #If Shark will eat a fish or Megalodons will eat a shark, it gains energy
                if self.next_move_will_eat:
                        self.grid[x][y].eat(self.shark_energy_gained_by_eating)    
                        #If Megaladons can appear, check if current shark can evolve
                        if isShark and self.enable_megalodons:
                            if self.grid[x][y].check_for_evolution() :
                                self.grid[x][y] = Megalodon(self.shark_reproduction_time, self.shark_energy, self.megalodon_evolution_threshold)       
                
                #Sharks lose energy when moving.
                if isShark:
                    if not self.grid[x][y].energy_management(self.shark_energy_depletion_rate):
                        self.grid[x][y] = False
                        will_die = True
                
                if isMegalodon:
                    #Remove old tail. If newly evolved, skip this check.
                    if self.grid[x][y].skip_first_tail_check:
                        self.grid[x][y].skip_first_tail_check = False
                    else:
                        self.grid[self.grid[x][y].tail_pos[0]][self.grid[x][y].tail_pos[1]] = False                     
                    #Megalodons lose energy when moving.
                    if not self.grid[x][y].energy_management(self.shark_energy_depletion_rate):
                        self.grid[x][y] = False
                        will_die = True
                    else:
                        #If they don't die, save current pos as new tail pos and set direction
                        self.grid[x][y].current_direction = direction
                        #Save new tail position
                        self.grid[x][y].tail_pos = (x, y)     
                
                #Move entity to new cell depending on direction                
                #North/Up block
                if direction == "N":                    
                    self.grid[x-1][y] = self.grid[x][y] if not will_die else False               
                if direction == "D":
                    self.grid[len(self.grid)-1][y] = self.grid[x][y] if not will_die else False  
                                    
                #South/Down block
                if direction == "S":
                    self.grid[x+1][y] = self.grid[x][y] if not will_die else False                     
                if direction == "U":
                    self.grid[0][y] = self.grid[x][y] if not will_die else False  
                    
                #West/Right block             
                if direction == "W":
                    self.grid[x][y-1] = self.grid[x][y] if not will_die else False                      
                if direction == "R":
                    self.grid[x][len(self.grid[x])-1] = self.grid[x][y] if not will_die else False  
                    
                #East/Left block
                if direction == "E":
                    self.grid[x][y+1] = self.grid[x][y] if not will_die else False                      
                if direction == "L":
                    self.grid[x][0] = self.grid[x][y] if not will_die else False  
                
                #Check for leaving tile behavior
                #If reproducing, left a new entity of same type. Else, leaves water.
                if isMegalodon:
                    #Move tail if the Megalodon didn't die
                    if not will_die:
                        self.grid[x][y] = Megalodon_Tail(direction)                                       
                elif will_reproduce:
                    if isShark:
                        self.grid[x][y] = Shark(self.shark_reproduction_time, self.shark_energy, self.megalodon_evolution_threshold)
                    else:
                        self.grid[x][y] = Fish(self.fish_reproduction_time)
                else:
                    self.grid[x][y] = False               
                        
        #Reset fishes movement
        for x in self.grid:
            for y in x:
                if y:
                    y.has_moved = False        
          
        
    def get_empty_grid_space(self) -> int:
        """
        Return the coordinates of a random empty space in the grid as two int x and y.
        """
        
        #Loop through random coordinates until one water tile is found
        found_suitable_space = False
        while not found_suitable_space:
            x = randint(0, self.size[1]-1)
            y = randint(0, self.size[0]-1)
            if self.grid[x][y] == False:
                found_suitable_space = True
        return x, y

    def print_grid(self) -> None: 
        """
        Print the state of the world in the console.
        """   
        self.fish_population = 0
        self.shark_population = 0    
        self.megalodon_population = 0
        for x in self.grid:
            line = "| "
            for y in x:
                if isinstance(y, Megalodon) or isinstance(y, Megalodon_Tail):
                    line += f"[\033[35m{y.get_visual()}\033[0m]"
                    if not isinstance(y, Megalodon_Tail):
                        self.megalodon_population += 1
                elif isinstance(y, Shark):
                    line += f"[\033[31mX\033[0m]"
                    self.shark_population += 1
                elif isinstance(y,Fish):
                    line += f"[\033[33mO\033[0m]"
                    self.fish_population += 1
                else:
                    line += f"[\033[34m~\033[0m]"                
            line += " |"
            print(line)
    
    def get_megalodons_directions(self, x: int, y: int) -> str:
        """
        Return all possible movement for the Megalodon based only on the presence of sharks in its move radius. 
        If no sharks exist in this radius, acts like a normal fish instead.
        Possible directions are :
        N = North
        D = Down (from top edge to bottom edge)
        S = South
        U = Up (from bottom edge to top edge)
        W = West
        R = Right (from left edge to right edge)
        E = East
        L = Left (from right edge to left edge)
        
        [Args]\n
        x, y = current coordinate of Megalodon
        """
                
        outcomes = ""               
        
        #Check for North availlable
        if x == 0 and self.check_for_only_shark_in_tile(len(self.grid)-1, y):
            outcomes += "D"            
        elif x == 0:
            pass
        elif self.check_for_only_shark_in_tile(x-1, y):
            outcomes += "N"
            
        #Check for South availlable
        if x == (len(self.grid) - 1) and self.check_for_only_shark_in_tile(0, y):
            outcomes += "U"    
        elif x == (len(self.grid) - 1):
            pass      
        elif self.check_for_only_shark_in_tile(x+1, y):
            outcomes += "S"
            
        #Check for West availlable
        if y == 0 and self.check_for_only_shark_in_tile(x, len(self.grid[y])-1):
            outcomes += "R"     
        elif y == 0:
            pass
        elif self.check_for_only_shark_in_tile(x, y-1):
            outcomes += "W"
            
        #check for East availlabke
        if y == (len(self.grid[x]) - 1) and self.check_for_only_shark_in_tile(x, 0):
            outcomes += "L"  
        elif y == (len(self.grid[x]) - 1):
            pass
        elif self.check_for_only_shark_in_tile(x, y+1):
            outcomes += "E"
        
        if outcomes != "":
            self.next_move_will_eat = True
            return outcomes

        #If no shark availlable, return normal fish behavior
        return self.get_fish_direction(x, y)
    
    def get_shark_directions(self, x: int, y: int) -> str:
        """
        Return all possible movement for the shark based only on the presence of fishes in its move radius. 
        If no fishes exist in this radius, acts like a normal fish instead.
        Possible directions are :
        N = North
        D = Down (from top edge to bottom edge)
        S = South
        U = Up (from bottom edge to top edge)
        W = West
        R = Right (from left edge to right edge)
        E = East
        L = Left (from right edge to left edge)
        
        [Args]\n
        x, y = current coordinate of shark
        """
                
        outcomes = ""               
        
        #Check for North availlable
        if x == 0 and self.check_for_only_fish_in_tile(len(self.grid)-1, y):
            outcomes += "D"            
        elif x == 0:
            pass
        elif self.check_for_only_fish_in_tile(x-1, y):
            outcomes += "N"
            
        #Check for South availlable
        if x == (len(self.grid) - 1) and self.check_for_only_fish_in_tile(0, y):
            outcomes += "U"    
        elif x == (len(self.grid) - 1):
            pass      
        elif self.check_for_only_fish_in_tile(x+1, y):
            outcomes += "S"
            
        #Check for West availlable
        if y == 0 and self.check_for_only_fish_in_tile(x, len(self.grid[y])-1):
            outcomes += "R"     
        elif y == 0:
            pass
        elif self.check_for_only_fish_in_tile(x, y-1):
            outcomes += "W"
            
        #check for East availlabke
        if y == (len(self.grid[x]) - 1) and self.check_for_only_fish_in_tile(x, 0):
            outcomes += "L"  
        elif y == (len(self.grid[x]) - 1):
            pass
        elif self.check_for_only_fish_in_tile(x, y+1):
            outcomes += "E"
        
        if outcomes != "":
            self.next_move_will_eat = True
            return outcomes

        #If no fish availlable, return normal fish behavior
        return self.get_fish_direction(x, y)
    
    def get_fish_direction(self, x: int, y: int) -> str:
        """
        Return all possible movement for the fish :
        N = North
        D = Down (from top edge to bottom edge)
        S = South
        U = Up (from bottom edge to top edge)
        W = West
        R = Right (from left edge to right edge)
        E = East
        L = Left (from right edge to left edge)
        
        [Args]\n
        x, y = current coordinate of fish
        """
        
        outcomes = ""               
                     
        #Check for North availlable
        if x == 0 and self.grid[len(self.grid)-1][y] == False:
            outcomes += "D"            
        elif x == 0:
            pass
        elif self.grid[x-1][y] == False:
            outcomes += "N"
            
        #Check for South availlable
        if x == (len(self.grid) - 1) and self.grid[0][y] == False:
            outcomes += "U"    
        elif x == (len(self.grid) - 1):
            pass      
        elif self.grid[x+1][y] == False:
            outcomes += "S"
            
        #Check for West availlable
        if y == 0 and self.grid[x][len(self.grid[y])-1] == False:
            outcomes += "R"     
        elif y == 0:
            pass
        elif self.grid[x][y-1] == False:
            outcomes += "W"
            
        #check for East availlabke
        if y == (len(self.grid[x]) - 1) and self.grid[x][0] == False:
            outcomes += "L"  
        elif y == (len(self.grid[x]) - 1):
            pass
        elif self.grid[x][y+1] == False:
            outcomes += "E"
     
        return outcomes

    def check_for_only_shark_in_tile(self, x: int, y: int) -> bool:
        return isinstance(self.grid[x][y], Shark) and not\
            isinstance(self.grid[x][y], Megalodon)
            
    def check_for_only_fish_in_tile(self, x: int, y: int) -> bool:
        return isinstance(self.grid[x][y], Fish) and not isinstance(self.grid[x][y], Shark) and not\
            isinstance(self.grid[x][y], Megalodon)
