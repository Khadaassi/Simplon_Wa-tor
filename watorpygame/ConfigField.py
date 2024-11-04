from enum import StrEnum

class ConfigField(StrEnum):
    FISH_POPULATION =  "Po-po-pop uh lation des poissons" 
    SHARK_POPULATION =  "shark_population"
    REFRESH_LENGTH = "refresh_length"
    WORLD_WIDTH = "world_width"
    WORD_HEIGTH = "world_height"
    FISH_REPRO_TIME = "fish_repro_time"
    SHARK_REPRO_TIME = "shark_repro_time"
    SHARK_ENERGY ="shark_energy"
    SHARK_ENERGY_GAIN = "shark_energy_gain"
    ALLOW_MEGALODONS = "allow_megalodons"
    MEGALODON_EVOLUTION_THRESHOLD = "megalodon_evolution_threshold"
    ALLOW_PACMAN = "allow_pacman"

def get_validation_function(field : ConfigField) -> object:
    match field :
        case ConfigField.FISH_POPULATION : return int 
        case ConfigField.SHARK_POPULATION : return int 
        case ConfigField.REFRESH_LENGTH : return float
        case ConfigField.WORLD_WIDTH : return int 
        case ConfigField.WORD_HEIGTH : return int 
        case ConfigField.FISH_REPRO_TIME : return int 
        case ConfigField.SHARK_REPRO_TIME : return int 
        case ConfigField.SHARK_ENERGY : return int 
        case ConfigField.SHARK_ENERGY_GAIN : return int 
        case ConfigField.ALLOW_MEGALODONS : return bool 
        case ConfigField.MEGALODON_EVOLUTION_THRESHOLD : return int 
        case ConfigField.ALLOW_PACMAN : return bool
        case _ : return str