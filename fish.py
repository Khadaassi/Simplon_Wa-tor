class Fish():
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

    def __init__(self, reproduction_age: int, has_moved: bool):
        self.age = 0
        self.reproduction_age = reproduction_age
        self.direction = "" # for later
        self.has_moved = has_moved

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
    """"
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

    def __init__(self, reproduction_age: int, energy: int):
        super().__init__(reproduction_age)
        self.energy = energy
        self.max_energy = self.energy
        pass


    def eat(self, energy: int):
        """
        Simulates the shark eating a fish.
        """
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
