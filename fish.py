class Fish():
    """
    A class to represent a fish in a water ecosystem.

    Attributes
    ----------
    age : int
        The age of the fish in years.

    Methods
    -------   
    swim(distance: float)
        Simulates the fish swimming a specified distance in meters, potentially affecting its health or energy.
        
    reproduce(partner: 'Fish')
        Returns a new Fish instance if the fish is of reproductive age.

    """
    def __init__(self, age: int, size: float):
        self.age = age
        self.size = 1

    def swim(self, distance: float):
        """
        Simulates the fish swimming a specified distance.
        
        Parameters
        ----------
        distance : float
            The distance that the fish will swim.
        """
        pass

    def reproduce(self):
        """
        Returns a new Fish instance if the Fish is of reproductive age.
        """
        pass
