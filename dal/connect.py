
import configparser
import eia
import os
class  Api():
    def __init__(self):

        #encapsulation
        if os.name == 'nt': #for windows laptop version
            config = configparser.ConfigParser()
            config.read_file(open('dal/credentials.cfg')) #create file w/ EIA API key
            key = config['Common']['APIKEY'] #accessible only inside the constructor
        else:
            key = os.environ.get('EIA_APIKEY')
        self.api = eia.API(key)