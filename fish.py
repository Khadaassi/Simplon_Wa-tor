class Fish():
    """
    A class to represent a fish in a water ecosystem.

    Attributes
    ----------
    age : int
        The age of the fish in years.

    Methods
    -------   
    swim(direction: str)
        Simulates the fish swimming a specified direction.
        
    reproduce()
        Returns a new Fish instance if the fish is of reproductive age.

    """
    reproduction_age = 3

    def __init__(self, age: int, size: int = 1):
        self.age = age
        self.size = size

    # def swim(self, x, y, direction: str):
    #     """
    #     Simulates the fish swimming a specified direction.
        
    #     Parameters
    #     ----------
    #     direction : 
    #         The direction where the fish will swim.
    #     """
    #     pass

    def reproduce(self):
        """
        Returns a new Fish instance if the fish is of reproductive age.

        Returns
        -------
        Fish or None
            A new Fish instance if the fish can reproduce, otherwise None.
        """
        if self.age >= Fish.reproduction_age:
            new_fish = Fish(age=0, size=1)
            self.age = 0 
            return new_fish
        else:
            return None
