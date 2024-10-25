class Fish():
    """
    A class to represent a fish in a water ecosystem.

    Attributes
    ----------
    age : int
        The age of the fish in years.

    Methods
    --------  
    reproduce()
        Returns a new Fish instance if the fish is of reproductive age.

    """

    def __init__(self, reproduction_age: int):
        self.age = 0
        self.reproduction_age = reproduction_age

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
