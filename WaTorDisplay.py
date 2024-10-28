class WaTorDisplay:
    """
        Management of the pygame interface
    """
    def __init__(self, app_object):
        """
            When instanciated, the object starts a pygame
            needs a app_object which have got three methods : 
                app_object.start()
                app_object.pause()
                app_object.stop()
        """
        self.mainObject = app_object

    def update_view(self, world):
        """
            Takes a world object which
              is a list[list[str]] object 
              or contains a list[list[str]]
            in which  ashark is a 'X', a fish is a 'o', water is a '~'
        """
        self.world = world

# app_object.start()
# app_object.pause()
# app_object.stop()