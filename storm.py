from random import randint

class Storm_Tile:
    #This class is used to represent the storm on the grid.
    def __init__(self) -> None:
        pass

class Storm:
        
    min_size = 3
    max_size = 9
    min_duration = 5
    max_duration = 20
    
    def __init__(self) -> None:
        self.duration = randint(self.min_duration, self.max_duration)
        self.coordinates = [] #List holding the coordinates of every grid cell affected by the storm
        self.size = 0
    
    def spawn_storm(self, max_x: int, max_y: int) -> None:
        """
        
        """
        #Get "eye of the storm", epicenter tile randomly
        init_x = randint(0, max_x)
        init_y = randint(0, max_y)
        self.coordinates.append((init_x, init_y))
        
        #Spawn each storm tile based on a cyclone pattern. (Cross pattern into X pattern into cross pattern.....)
        self.size = randint(self.min_size, self.max_size)
        size = self.size - 1 #Epicenter took 1 size
        x_offset = 0
        y_offset = 0
        clockwork = 0 #Storm is spawned in a clockwork pattern (starting at 12)
        diagonals = False
        #Add a storm tile while there is still storm to add
        while size > 0:
            for i in range(0, 4):
                #First pattern is cross shaped (North, then East, then South, then West)
                if not diagonals:
                    match clockwork:
                        case 0:
                            self.coordinates.append((init_x-1-x_offset if init_x!= 0 else max_x-x_offset, init_y))
                        case 1:
                            self.coordinates.append((init_x, init_y+1+y_offset if init_y != max_y else 0+y_offset))
                        case 2:
                            self.coordinates.append((init_x+1+x_offset if init_x!= max_x else 0+x_offset, init_y))
                        case 3:
                            self.coordinates.append((init_x, init_y-1-y_offset if init_y != 0 else max_y+y_offset))
                #Second pattern is X shaped (Nort-East then South-East then South-West then North-West)
                else:
                    match clockwork:
                        case 0:
                            self.coordinates.append((init_x-1-x_offset if init_x!= 0 else max_x-x_offset, init_y+1+y_offset if init_y != max_y else 0+y_offset))
                        case 1:
                            self.coordinates.append((init_x+1+x_offset if init_x!= max_x else 0+x_offset, init_y+1+y_offset if init_y != max_y else 0+y_offset))
                        case 2:
                            self.coordinates.append((init_x+1+x_offset if init_x!= max_x else 0+x_offset, init_y-1-y_offset if init_y != 0 else max_y-y_offset))
                        case 3:
                            self.coordinates.append((init_x-1-x_offset if init_x!= max_x else 0-x_offset, init_y-1-y_offset if init_y != 0 else max_y-y_offset))
                
                clockwork = clockwork + 1 if clockwork < 3 else 0
                size -= 1
                if size <= 0:
                    break
            
            #Each time a pattern is completed, we need to expand the radius
            x_offset = x_offset+1 if diagonals else x_offset
            y_offset = y_offset+1 if diagonals else y_offset
            diagonals = not diagonals
    
    def check_for_ending(self) -> bool:
        self.duration -= 1
        return self.duration <= 0
         
if __name__ == "__main__":
    diagonals = True
    print(f"Diagonals = {diagonals}")
    print(f"-Diagonals = {not diagonals}")
        