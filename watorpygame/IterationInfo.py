class IterationInfo :
    def __init__(self, current_iteration : int, fish_pop : int, shark_pop : int) :
        self.current_iteration = current_iteration
        self.fish_pop = fish_pop
        self.shark_pop = shark_pop
        self.allow_megalodons = False
        self.megalodon_pop = 0
        self.allow_pacman = False
        self.pacman_score = 0
        self.allow_storms = False

    def add_megalodons_info(self, megalodon_pop) :
        self.allow_megalodons = True
        self.megalodon_pop = megalodon_pop

    def add_pacman_info(self, pacman_score) :
        self.allow_pacman = True
        self.pacman_score = pacman_score

    def add_storms_info(self, killed_by_storm) :
        self.allow_storms = True
        self.killed_by_storm = killed_by_storm
