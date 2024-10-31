from configparser import ConfigParser


def write_config():
    config = ConfigParser()

    config["world"] = {
        "fish_population": "500",
        "shark_population": "200",
        "refresh_length": "0.5",
        "world_width": "40",
        "world_height": "30",
        "fish_repro_time": "3",
        "shark_repro_time": "3",
        "shark_energy": "2",
        "shark_energy_gain": "2",
        "allow_megalodons": "False",
        "megalodon_evolution_threshold" : "10"
    }

    with open("config.ini", "w") as configfile:
        config.write(configfile)


def read_config():
    config = ConfigParser()
    config.read("config.ini")

    fish_population = config.getint("world", "fish_population")
    shark_population = config.getint("world", "shark_population")
    refresh_length = config.getfloat("world", "refresh_length")  # Fixed typo
    world_width = config.getint("world", "world_width")
    world_height = config.getint("world", "world_height")
    fish_repro_time = config.getint("world", "fish_repro_time")
    shark_repro_time = config.getint("world", "shark_repro_time")
    shark_energy = config.getint("world", "shark_energy")
    shark_energy_gain = config.getint("world", "shark_energy_gain")
    allow_megalodons = config.getboolean("world", "allow_megalodons")
    megalodon_evolution_threshold = config.getint("world", "megalodon_evolution_threshold")

    return [
        fish_population,
        shark_population,
        refresh_length,
        world_width,
        world_height,
        fish_repro_time,
        shark_repro_time,
        shark_energy,
        shark_energy_gain,
        allow_megalodons,
        megalodon_evolution_threshold
        ]
    
