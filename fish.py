from random import randint

#__________________________________________________________________________
#
# region Fish 
#__________________________________________________________________________
class Fish:
    """
    A class to represent a fish in a water ecosystem.

    Attributes
    ----------
    age : int
        The age of the fish.
    reproduction_age : int
        The age at which the fish can reproduce.
    direction : str
        The direction in which the fish is moving.
    has_moved : bool
        A boolean indicating if the fish has moved during the current loop.

    Methods
    -------
    reproduce()
        Returns a new Fish instance if the fish is of reproductive age.
    """
    def __init__(self, reproduction_age: int):
        self.time_since_last_reproduction = 0
        self.reproduction_threshold = reproduction_age
        self.has_moved = False
        self.age = 0

    def reproduce(self) -> bool:
        """
        Returns
        -------
        Fish or None
            A new Fish instance if the fish can reproduce, otherwise None.
        """
        self.time_since_last_reproduction += 1
        if self.time_since_last_reproduction >= self.reproduction_threshold:
            self.time_since_last_reproduction = 0
            return True
        else:
            return False
        
    def __str__(self) -> str:
        return "FISH"
#__________________________________________________________________________
#
# region Shark
#__________________________________________________________________________
class Shark(Fish):
    """ "
    A class to represent a shark in a water ecosystem that inherites of Fish class.

    Attributes
    ----------
    energy : int
        The energy of the shark.
    max_energy : int
        The maximum energy of the shark.
    reproduction_age : int
        The age at which the shark can reproduce.

    Methods
    -------
    eat(energy: int)
        Simulates the shark eating a fish.
    energy_management(energy: int)
        Simulates the shark energy movement.
    """
    def __init__(self, reproduction_age: int, energy: int, evolution_threshold: int):
        super().__init__(reproduction_age)
        self.energy = energy
        self.max_energy = self.energy
        self.fish_eaten = 0
        self.megalodon_evolution_threshold = evolution_threshold # The amount of fish a shark needs to eat to evolve into a megalodon

    def eat(self, energy: int) -> None:
        """
        Simulates the shark eating a fish.
        """
        self.fish_eaten += 1
        self.energy += energy
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def check_for_starvation(self, energy: int = 1):
        """
        Sharks lose energy each time they move. If they have no energy, they die from starvation.

        Parameters
        ----------
        energy : int
            The amount of energy to subtract from the shark's energy. The default is 1.

        Returns
        -------
        bool
            True if the shark no energy left, otherwise False.
        """
        self.energy -= energy
        if self.energy == 0:
            return True
        else:
            return False
        
    def check_for_evolution(self) -> bool:
        """
        Checks if the shark has eaten enough fish to evolve into a megalodon.

        Returns
        -------
        bool
            True if the shark has eaten enough fish to evolve into a megalodon, otherwise False.
        """
        return self.fish_eaten >= self.megalodon_evolution_threshold
    
    def __str__(self) -> str:
        return "SHARK"

#______________________________________________________________________________
#
# region Megalodon 
#______________________________________________________________________________
class Megalodon(Shark):
    """
    A class to represent a megalodon in a water ecosystem that inherites of Shark class.

    Attributes
    ----------
    current_direction : str
        The current direction of the megalodon's head.
    tail_pos : tuple
        The position of the megalodon's tail.
    skip_first_tail_check : bool
        A boolean indicating if the megalodon's tail should be checked for the first time.

    Methods
    -------
    reproduce()
        Returns False as megalodons do not reproduce.
    get_visual()
        Returns the visual representation of the megalodon.

    """
   
    def __init__(self, reproduction_age: int, energy: int, evolution_threshold: int):
        super().__init__(reproduction_age, energy, evolution_threshold)
        self.energy *= 5  # Megalodons have 5 times as much energy as a normal shark
        self.max_energy *= 5
        self.current_direction = "NSWE"[randint(0, 3)] #Get a random direction for the head on spawn. North (N), South (S), West (W), East (E)
        self.tail_pos = (-1, -1)
        self.skip_first_tail_check = True #When a Megalodon spawns, its tail doesn't occupy a space until its first move

    def reproduce(self) -> bool:
        # Megalodons don't reproduce
        return False

    def get_visual(self) -> str:
        """
        Returns
        -------
        str
            The visual representation of the megalodon.
        """
        if self.current_direction == "N" or self.current_direction== "D":
            return "^"
        if self.current_direction == "S" or self.current_direction == "U":
            return "v"
        if self.current_direction == "W" or self.current_direction == "R":
            return "<"
        if self.current_direction == "E" or self.current_direction == "L":
            return ">"
    
    def __str__(self) -> str:
        return "MEGA"
#__________________________________________________________________________
#
# region Megalodon_Tail
#__________________________________________________________________________
class Megalodon_Tail(Megalodon):
    """
    A class to represent a megalodon's tail in a water ecosystem that inherites of Megalodon class.

    Attributes
    ----------
    current_direction : str
        The current direction of the megalodon's tail.
    has_moved : bool
        A boolean indicating if the megalodon's tail has moved during the current loop.
    age : int
        The age of the megalodon's tail.
    head_pos : tuple[int, int]
        The coordinate of the head on the grid.
    
    Methods
    -------
    get_visual()
        Returns the visual representation of the megalodon's tail.
    """
    # Megalodons' tail has no specificities
    def __init__(self, direction: str, current_pos: tuple[int,int], world_size: int):
        self.current_direction = direction
        self.has_moved = True #Megalodon tails only follow the heads and never move on their own
        self.age = 0        
        match direction:
            case "N":
                self.head_pos = (current_pos[0]-1, current_pos[1])
            case "D":
                self.head_pos = (world_size-1, current_pos[1])
            case "S":
                self.head_pos = (current_pos[0]+1, current_pos[1])
            case "U":
                self.head_pos = (0, current_pos[1])
            case "W":
                self.head_pos = (current_pos[0], current_pos[1]-1)
            case "R":
                self.head_pos = (current_pos[0], world_size-1)
            case "E":
                self.head_pos = (current_pos[0], current_pos[1]+1)
            case "L":
                self.head_pos = (current_pos[0], 0)
            case _ :
                 self.head_pos = (-1, -1)
    
    def get_visual(self) -> str:
        """
        Returns the visual representation of the megalodon's tail.
        """
        if self.current_direction == "N" or self.current_direction == "D" or self.current_direction == "S" or self.current_direction == "U":
            return "|"
        if self.current_direction == "W" or self.current_direction == "R" or self.current_direction == "E" or self.current_direction == "L":
            return "-"
    
    def __str__(self) -> str:
        return "TAIL" 
