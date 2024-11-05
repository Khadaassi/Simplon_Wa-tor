from enum import StrEnum

class ConfigField(StrEnum):
    FISH_POPULATION = "fish_population" 
    SHARK_POPULATION = "shark_population"
    REFRESH_LENGTH = "refresh_length"
    MAX_ITERATION = "max_iteration"
    WORLD_WIDTH = "world_width"
    WORLD_HEIGTH = "world_height"
    FISH_REPRO_TIME = "fish_repro_time"
    SHARK_REPRO_TIME = "shark_repro_time"
    SHARK_ENERGY ="shark_energy"
    SHARK_ENERGY_GAIN = "shark_energy_gain"
    ALLOW_MEGALODONS = "allow_megalodons"
    MEGALODON_EVOLUTION_THRESHOLD = "megalodon_evolution_threshold"
    ALLOW_PACMAN = "allow_pacman"

