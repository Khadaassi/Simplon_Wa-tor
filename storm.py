from random import randint

class Storm_Tile:
    def __init__(self) -> None:
        pass

class Storm:
    
    #TODO : Scale storm size from grid size (storm can't be more than x% of total grid)
    
    min_size = 10
    max_size = 10
    base_duration = 10
    
    def __init__(self) -> None:
        self.duration = self.base_duration
        self.coordinates = []
        self.size = 0
    
    def spawn_storm(self, max_x: int, max_y: int) -> None:
        
        #Get "eye of the storm", epicenter randomly
        init_x = randint(0, max_x)
        init_y = randint(0, max_y)
        self.coordinates.append((init_x, init_y))
        
        #
        self.size = randint(self.min_size, self.max_size)
        size = self.size
        x_offset = 0
        y_offset = 0
        clockwork = 0
        diagonals = False
        while size > 0:
            for i in range(0, 4):
                if not diagonals:
                    match clockwork:
                        case 0:
                            self.coordinates.append((init_x-1+x_offset if init_x!= 0 else max_x-x_offset, init_y+y_offset))
                        case 1:
                            self.coordinates.append((init_x+x_offset, init_y+1+y_offset if init_y != max_y else 0+y_offset))
                        case 2:
                            self.coordinates.append((init_x+1+x_offset if init_x!= max_x else 0+x_offset, init_y+y_offset))
                        case 3:
                            self.coordinates.append((init_x+x_offset, init_y-1+y_offset if init_y != 0 else max_y-y_offset))
                else:
                    match clockwork:
                        case 0:
                            self.coordinates.append((init_x-1+x_offset if init_x!= 0 else max_x-x_offset, init_y+1+y_offset if init_y != max_y else 0+y_offset))
                        case 1:
                            self.coordinates.append((init_x+1+x_offset if init_x!= max_x else 0+x_offset, init_y+1+y_offset if init_y != max_y else 0+y_offset))
                        case 2:
                            self.coordinates.append((init_x+1+x_offset if init_x!= max_x else 0+x_offset, init_y-1+y_offset if init_y != 0 else max_y-y_offset))
                        case 3:
                            self.coordinates.append((init_x+1+x_offset if init_x!= max_x else 0+x_offset, init_y-1+y_offset if init_y != 0 else max_y-y_offset))
                
                clockwork = clockwork + 1 if clockwork < 3 else 0
                size -= 1
                if size <= 0:
                    break
            
            x_offset = x_offset+1 if diagonals else x_offset
            y_offset = y_offset+1 if diagonals else y_offset
            if diagonals:
                diagonals = False
            else:
                diagonals = True
    
    def check_for_ending(self) -> bool:
        self.duration -= 1
        return self.duration <= 0
         
        
        