from fish import Fish

class Shark(Fish):
    """"
    A class to represent a shark in a water ecosystem that inherites of Fish class.
    Methods
    -------
    swim(direction: int)
        Simulates the shark swimming a specified direction.
    reproduce()
        Returns a new Shark instance if the shark is of reproductive age.
    eat(prey: 'Fish')
        Simulates the shark eating a fish.
    """

    def __init__(self, age: int, size: float):
        super().__init__(age, size)

    def swim(self, direction: int):
        """
        Simulates the shark swimming a specified distance.
        
        Parameters
        ----------
        direction : int
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
