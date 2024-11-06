# pacman.py
from fish import Fish
#______________________________________________________________________________
#
# region Pacman
#______________________________________________________________________________
class Pacman(Fish):
    """
    Pacman class, inherits from Fish

    Attributes
    ----------
    score : int
        Total number of objects consumed by Pacman
    
    Methods
    -------
    eat()
        Pacman eats an object, increasing its score by 1
    reproduce()
        Pacman does not reproduce
    __str__()
        Returns the string "PACMAN"
    """
    def __init__(self, reproduction_age=0):  # Default reproduction_age for Pacman
        super().__init__(reproduction_age)
        self.score = 0  # Tracks total objects eaten

    def eat(self) -> None:
        """
        Pacman eats an object, increasing its score by 1
        """
        self.score += 1
    
    def reproduce(self) -> bool:
        """
        Pacman is unique, no reproduction
        """
        return False
    
    def __str__(self) -> str:
        return "PACMAN"
