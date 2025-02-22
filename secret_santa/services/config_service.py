import configparser

class ConfigService:
    __instance = None 

    def __init__(self):
        if ConfigService.__instance is not None:
            raise Exception("Singleton instance already exists")
        else:
            ConfigService.__instance = self
        self.__config = configparser.ConfigParser()
        self.__config_file = "config.properties"
        self._read_config()

    @staticmethod
    def get_instance():
        if ConfigService.__instance is None:
            ConfigService()
        return ConfigService.__instance

    def get_value(self, section, key):
        try:
            return self.__config[section][key]
        except KeyError as e:
            return None
    
    def _read_config(self):
        self.__config.read(self.__config_file)