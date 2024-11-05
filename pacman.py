# pacman.py
from fish import Fish

class Pacman(Fish):
    """
    Pacman class, inherits from Fish
    Pacman is a unique fish that does not reproduce
    Pacman has a score attribute that tracks the total objects consumed
    """
    def __init__(self, reproduction_age=0):  # Default reproduction_age for Pacman
        super().__init__(reproduction_age)
        self.score = 0  # Tracks total objects consumed

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
