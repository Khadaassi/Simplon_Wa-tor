from configparser import ConfigParser
from ConfigField import ConfigField

#_______________________________________________________________________________________
#
# region: Write Configuration file
#_______________________________________________________________________________________
def write_config():
    """
    Writes a default configuration file to config.ini
    """
    config = ConfigParser()

    config["world"] = {
        ConfigField.FISH_POPULATION.value : "500",
        ConfigField.SHARK_POPULATION.value : "200",
        ConfigField.REFRESH_LENGTH.value : "0.3",
        ConfigField.MAX_ITERATION.value : "100",
        ConfigField.WORLD_WIDTH.value : "40",
        ConfigField.WORLD_HEIGTH.value : "30",
        ConfigField.FISH_REPRO_TIME.value : "3",
        ConfigField.SHARK_REPRO_TIME.value : "3",
        ConfigField.SHARK_ENERGY.value : "2",
        ConfigField.SHARK_ENERGY_GAIN.value : "2",
        ConfigField.ALLOW_MEGALODONS.value : "False",
        ConfigField.MEGALODON_EVOLUTION_THRESHOLD.value : "15",
        ConfigField.ALLOW_PACMAN.value : "False",
        ConfigField.ALLOW_STORMS.value : "False"
    }

    with open("config.ini", "w") as configfile:
        config.write(configfile)

#_______________________________________________________________________________________
#
# region: Read Configuration file
#_______________________________________________________________________________________
def read_config()-> dict[ConfigField, bool|int|float|str]:
    """
    Reads the configuration file and returns a list of the values
    """
    config = ConfigParser()
    config.read("config.ini")

    section = "world"
    dictionary = {}
    
    int_fields = [ConfigField.FISH_POPULATION]
    int_fields.append(ConfigField.SHARK_POPULATION)
    float_fields = [ConfigField.REFRESH_LENGTH]
    int_fields.append(ConfigField.MAX_ITERATION)
    int_fields.append(ConfigField.WORLD_WIDTH)
    int_fields.append(ConfigField.WORLD_HEIGTH)
    int_fields.append(ConfigField.FISH_REPRO_TIME)
    int_fields.append(ConfigField.SHARK_REPRO_TIME)
    int_fields.append(ConfigField.SHARK_ENERGY)
    int_fields.append(ConfigField.SHARK_ENERGY_GAIN)
    bool_fields = [ConfigField.ALLOW_MEGALODONS]
    int_fields.append(ConfigField.MEGALODON_EVOLUTION_THRESHOLD)
    bool_fields.append(ConfigField.ALLOW_PACMAN)
    bool_fields.append(ConfigField.ALLOW_STORMS)

    for field_key in ConfigField :
        match field_key :
            case key if key in bool_fields : dictionary[field_key] = config.getboolean(section, field_key.value)
            case key if key in int_fields  : dictionary[field_key] = config.getint(section, field_key.value)
            case key if key in float_fields : dictionary[field_key] = config.getfloat(section, field_key.value)   # Fixed typo

    return dictionary
    
