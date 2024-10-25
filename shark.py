from fish import Fish

class Shark(Fish):
    """"
    A class to represent a shark in a water ecosystem that inherites of Fish class.
    Methods
    -------
    swim(distance: float)
        Simulates the shark swimming a specified distance in meters, potentially affecting its health or energy.
    eat(prey: 'Fish')
        Simulates the shark eating a fish.
    """

    def __init__(self, age: int, size: float):
        super().__init__(age, size)

    def swim(self, distance: float):
        """
        Simulates the shark swimming a specified distance.
        
        Parameters
        ----------
        distance : float
            The distance that the shark will swim.
        """
        pass

    def reproduce(self):
        """
        Returns a new Shark instance if the shark is of reproductive age.
        """
        pass

    def eat(self, prey: 'Fish'):
        """
        Simulates the shark eating a fish.
        
        Parameters
        ----------
        prey : Fish
            The fish that the shark will eat.
        """
        pass
