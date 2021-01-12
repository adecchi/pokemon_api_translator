import os
import configparser
import re
import methodtools

from src.proxy.requests import Request
from src.utils import get_logger


logger = get_logger(__name__)


class Mapping:
    def __init__(self):
        config = configparser.ConfigParser()
        try:
            config_path = os.path.join(os.path.dirname(__file__), '../config/config.ini')
            config.read(config_path)
        except Exception as ex:
            logger.error(f"Error reading config.ini file {ex}")

        self.POKEMON_API_URL = config['DEFAULT']['POKEMON_API_URL']
        self.SHAKESPEARE_API_URL = config['DEFAULT']['SHAKESPEARE_API_URL']
        self.POKEMON_API_DESCRIPTION = config['DEFAULT']['POKEMON_API_DESCRIPTION']
        self.POKEMON_API_LAN = config['DEFAULT']['POKEMON_API_LAN']

    def _get_pokemon(self, pokemon_name):
        try:
            req = Request()
            status, response = req.get(self.POKEMON_API_URL)
            if status:
                pokemons = response['results']
                for pokemon in pokemons:
                    if pokemon['name'] == pokemon_name:
                        return True, pokemon
                return False, "Pokemon Not Found"
            else:
                return status, response
        except Exception as ex:
            logger.error(f"Error calling _get_pokemon method with error: {ex}")

    def _get_pokemon_details(self, pokemon):
        try:
            req = Request()
            status, response = req.get(pokemon['url'])
            if status:
                details = response[self.POKEMON_API_DESCRIPTION]
                for details in details:
                    text = details['flavor_text']
                    pokemon_name = pokemon['name']
                    if details['language']['name'] == self.POKEMON_API_LAN:
                        validation = re.match(r'^{}'.format(pokemon_name), text, re.IGNORECASE)
                        if validation:
                            data = details['flavor_text']
                            return True, data
                return False, "Details not found for pokemon {}".format(pokemon['name'])
            else:
                return status, response
        except Exception as ex:
            logger.error(f"Error calling _get_pokemon_details method with error: {ex}")

    def _get_translator(self, pokemon_name):
        try:
            status, pokemon = self._get_pokemon(pokemon_name)
            if status:
                status, pokemon_details = self._get_pokemon_details(pokemon)
                if status:
                    url = self.SHAKESPEARE_API_URL
                    data_to_translate = dict()
                    data_to_translate['text'] = pokemon_details
                    req = Request()
                    status, response = req.post(url, data=data_to_translate)
                    if status:
                        data = response['contents']['translated']
                        return True, data
                    else:
                        return status, response
                else:
                    return status, pokemon_details
            else:
                return False, pokemon
        except Exception as ex:
            logger.error(f"Error calling _get_translator method with error: {ex}")

    @methodtools.lru_cache(maxsize=1000)
    def get_pokemon_translation(self, pokemon_name):
        status, pokemon = self._get_translator(pokemon_name)
        if status:
            return True, pokemon
        else:
            return False, pokemon

    def cache_status(self):
        try:
            data_cache_get = self.get_pokemon_translation.cache_info()
            if data_cache_get != '':
                response = dict()
                response['hits'] = data_cache_get[0]
                response['misses'] = data_cache_get[1]
                response['maxsize'] = data_cache_get[2]
                response['currsize'] = data_cache_get[3]
                return response
            else:
                response = dict()
                response['status'] = 'Empty'
                return response
        except Exception as ex:
            logger.error(f"Error getting cache statistics with error: {ex}")