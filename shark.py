from fish import Fish

class Shark(Fish):
    """"
    A class to represent a shark in a water ecosystem that inherites of Fish class.
    Methods
    -------
    reproduce()
        Returns a new Shark instance if the shark is of reproductive age.
    eat()
        Simulates the shark eating a fish.
    """

    def __init__(self, reproduction_age: int):
        super().__init__(reproduction_age)
        pass


    def reproduce(self):
        """
        Returns a new Shark instance if the shark is of reproductive age.
        """
        pass

    def eat(self):
        """
        Simulates the shark eating a fish.
        
        """
        pass
#energie shark 