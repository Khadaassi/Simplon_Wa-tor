from random import randint

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
        self.age = 0
        self.reproduction_age = reproduction_age
        self.direction = ""  # for later
        self.has_moved = False

    def __str__(self) -> str:
        return "FISH"

    def reproduce(self):
        """
        Returns a new Fish instance if the fish is of reproductive age.

        Returns
        -------
        Fish or None
            A new Fish instance if the fish can reproduce, otherwise None.
        """
        self.age += 1
        if self.age >= self.reproduction_age:
            self.age = 0
            return True
        else:
            return False


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

    def __str__(self) -> str:
        return "SHARK"

    def eat(self, energy: int):
        """
        Simulates the shark eating a fish.
        """
        self.fish_eaten += 1
        self.energy += energy
        if self.energy > self.max_energy:
            self.energy = self.max_energy

    def energy_management(self, energy: int):
        """
        Simulates the shark energy movement.
        """
        self.energy -= energy
        if self.energy == 0:
            return False
        else:
            return True
        
    def check_for_evolution(self) -> bool:
        return self.fish_eaten >= self.megalodon_evolution_threshold


class Megalodon(Shark):

    # Megalodons have twice as much energy
    def __init__(self, reproduction_age: int, energy: int, evolution_threshold: int):
        super().__init__(reproduction_age, energy, evolution_threshold)
        self.energy *= 5
        self.max_energy *= 5
        self.current_direction = "NSWE"[randint(0, 3)] #The current direction of the head. North (N), South (S), West (W), East (E)
        self.tail_pos = (0,0)
        self.skip_first_tail_check = True #When a Megalodon spawns, its tail doesn't occupy a space until its first move

    def reproduce(self):
        # Megalodons don't reproduce
        return False

    def get_visual(self) -> str:
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


class Megalodon_Tail(Megalodon):

    # Megalodons' tail has no specificities
    def __init__(self, direction: str):
        self.current_direction = direction
        self.has_moved = True #Megalodon tails only follow the heads and never move on their own
    
    def get_visual(self) -> str:
        if self.current_direction == "N" or self.current_direction == "D" or self.current_direction == "S" or self.current_direction == "U":
            return "|"
        if self.current_direction == "W" or self.current_direction == "R" or self.current_direction == "E" or self.current_direction == "L":
            return "-"
    
    def __str__(self) -> str:
        return "TAIL" 
