
import configparser
import eia

class  Api():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read_file(open('dal/credentials.cfg'))
        #encapsulation
        key = config['Common']['APIKEY'] #accessible only inside the constructor
        self.api = eia.API(key)