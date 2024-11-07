from random import randint

#______________________________________________________________________________
#
# region Storm
#______________________________________________________________________________
class Storm_Tile:
    """
    This class is used to represent a storm tile. It is used to store the coordinates of the storm tile.
    """
    def __init__(self) -> None:
        pass

class Storm:
    """
    This class is used to represent a storm. It is used to store the coordinates of the storm and the duration of the storm.

    [Attributes]
    duration : int : The duration of the storm.
    coordinates : list : List of coordinates of the storm.
    size : int : The size of the storm.
    min_size : int : The minimum size of the storm.
    max_size : int : The maximum size of the storm.
    min_duration : int : The minimum duration of the storm.
    max_duration : int : The maximum duration of the storm.

    [Methods]
    spawn_storm : 
        This method is used to spawn a new storm. It will get the coordinates, duration and size of the storm.
    check_for_ending : 
        This method is used to check if the storm has ended. It will reduce the duration of the storm by 1.

    """
    min_size = 3
    max_size = 9
    min_duration = 5
    max_duration = 20
    
    def __init__(self) -> None:
        
        self.duration = randint(self.min_duration, self.max_duration) #Each storm's duration is randomized
        self.coordinates = [] #List holding the coordinates of every grid cell affected by the storm
        self.size = 0
    
    def spawn_storm(self, max_x: int, max_y: int) -> None:
        """
        The main function of storm. Get "eye of the storm", epicenter tile randomly. This will create a new storm, getting coordinates, duration and size.
        
        Parameters
        ----------
        max_x : the max height of the grid. \n
        max_y : the max width of the grid.
        """
        init_x = randint(0, max_x)
        init_y = randint(0, max_y)
        self.coordinates.append((init_x, init_y))
        
        #Set size randomly
        self.size = randint(self.min_size, self.max_size)
        size = self.size - 1 #Epicenter took 1 size
        
        #Spawn each storm tile based on a cyclone pattern. (Cross pattern into X pattern into cross pattern.....)
        x_offset = 0
        y_offset = 0
        clock = 0 #Storm is spawned in a clockwork pattern (starting at 12)
        diagonals = False #Check if next spawn needs to be diagonal or orthogonal
        
        #Add a storm tile while there is still storm to add
        while size > 0:
            for i in range(0, 4):
                #First pattern is cross shaped (North, then East, then South, then West)
                if not diagonals:
                    match clock:
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
                    match clock:
                        case 0:
                            self.coordinates.append((init_x-1-x_offset if init_x!= 0 else max_x-x_offset, init_y+1+y_offset if init_y != max_y else 0+y_offset))
                        case 1:
                            self.coordinates.append((init_x+1+x_offset if init_x!= max_x else 0+x_offset, init_y+1+y_offset if init_y != max_y else 0+y_offset))
                        case 2:
                            self.coordinates.append((init_x+1+x_offset if init_x!= max_x else 0+x_offset, init_y-1-y_offset if init_y != 0 else max_y-y_offset))
                        case 3:
                            self.coordinates.append((init_x-1-x_offset if init_x!= max_x else 0-x_offset, init_y-1-y_offset if init_y != 0 else max_y-y_offset))
                
                #Update the current pattern and check if there is no tile left to generate.
                clock = clock + 1 if clock < 3 else 0
                size -= 1
                if size <= 0:
                    break
            
            #Each time a pattern is completed, we need to expand the radius
            x_offset = x_offset+1 if diagonals else x_offset
            y_offset = y_offset+1 if diagonals else y_offset
            diagonals = not diagonals
    
    def check_for_ending(self) -> bool:
        """
        Reduce duration by 1 and return True if Storm is ending.

        Returns
        -------
        bool : True if storm has ended, False otherwise.
        """
        self.duration -= 1
        return self.duration <= 0
