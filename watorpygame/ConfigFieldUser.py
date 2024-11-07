from ConfigField import ConfigField

class ConfigFieldTranslator :
    def __init__(self):
        pass

    def get_label_text(self, field_key : ConfigField, display_zone : int =0 ) -> str:
        #if display_zone ==0 :
        display_texts = []
        match field_key :
            case ConfigField.FISH_POPULATION : display_texts = ["Population initiale de poissons"]
            case ConfigField.SHARK_POPULATION : display_texts = ["Population initiale de requins"]
            case ConfigField.REFRESH_LENGTH : display_texts = ["Durée d'une itération (sec)"]
            case ConfigField.MAX_ITERATION : display_texts = ["Nombre maximum d'itérations"]
            case ConfigField.WORLD_WIDTH : display_texts = ["Largeur du monde"]
            case ConfigField.WORLD_HEIGTH : display_texts = ["Hauteur du monde"]
            case ConfigField.FISH_REPRO_TIME : display_texts = ["Durée avant reproduction des poissons"]
            case ConfigField.SHARK_REPRO_TIME : display_texts = ["Durée avant reproduction des requins"]
            case ConfigField.SHARK_ENERGY : display_texts = ["Energie des requins"]
            case ConfigField.SHARK_ENERGY_GAIN : display_texts = ["Gain d'énergie pour les requins"]
            case ConfigField.ALLOW_MEGALODONS : display_texts = ["Existence des mégalodons"]
            case ConfigField.MEGALODON_EVOLUTION_THRESHOLD : display_texts = ["Seuil d'évolution des mégalodons"]
            case ConfigField.ALLOW_PACMAN : display_texts = ["Existence de pacman"]
            case ConfigField.ALLOW_STORMS : display_texts = ["Existence des tempêtes"]
            case _ : display_texts = ["champ inconnu"]

        return display_texts[0]

    def get_validation_function(self, field : ConfigField) -> object:
        match field :
            case ConfigField.FISH_POPULATION : return int 
            case ConfigField.SHARK_POPULATION : return int 
            case ConfigField.REFRESH_LENGTH : return float
            case ConfigField.MAX_ITERATION : return int
            case ConfigField.WORLD_WIDTH : return int 
            case ConfigField.WORLD_HEIGTH : return int 
            case ConfigField.FISH_REPRO_TIME : return int 
            case ConfigField.SHARK_REPRO_TIME : return int 
            case ConfigField.SHARK_ENERGY : return int 
            case ConfigField.SHARK_ENERGY_GAIN : return int 
            case ConfigField.ALLOW_MEGALODONS : return bool 
            case ConfigField.MEGALODON_EVOLUTION_THRESHOLD : return int 
            case ConfigField.ALLOW_PACMAN : return bool
            case ConfigField.ALLOW_STORMS : return bool
            case _ : return str