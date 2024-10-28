class CommandObserver :
    def __init__(self) : pass
    def on_user_command(self, command:str) : pass

class CommandBuilder :
    """
    That object contains a reference to one other object
    """
    def __init__(self, observer : CommandObserver) :
        self.observer = observer

    def command_callback(self) :
        return self.observer.on_user_command
        