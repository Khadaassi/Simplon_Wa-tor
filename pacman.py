# pacman.py
from fish import Fish

class Pacman(Fish):
    def __init__(self, reproduction_age=0):  # Default reproduction_age for Pacman
        super().__init__(reproduction_age)
        self.score = 0  # Tracks total objects consumed

    def eat(self):
        self.score += 1
    
    def reproduce(self):
        # Pacman is unique, no reproduction
        return False
    
    def __str__(self) -> str:
        return "PACMAN"
