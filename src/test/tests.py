import unittest
import httpx
from src.mapping.mapping import Mapping


class MappingTests(unittest.TestCase):

    def test_get_pokemon_translation(self):
        pokemon_name = 'charizard'
        mapping = Mapping()
        status, response = mapping.get_pokemon_translation(pokemon_name)
        if response.status_code == 200:
            status, response = True, response.json()
            self.assertTrue(status) and self.assertIsInstance(response, list)
        else:
            status, response = False, response
            self.assertAlmostEqual(response.status_code, 429)


class ProxyTests(unittest.TestCase):

    def test_get(self):
        url = 'https://pokeapi.co/api/v2/pokemon-species/'
        ssl_config = httpx.create_ssl_context()
        response = httpx.get(url, verify=ssl_config)
        if response.status_code == 200:
            status, response = True, response.json()
        else:
            status, response = False, response
        self.assertIsInstance(response['results'], list) and self.assertTrue(status)

    def test_post(self):
        ssl_config = httpx.create_ssl_context()
        url = 'https://api.funtranslations.com/translate/shakespeare.json?text='
        data = {'text': 'spanish'}
        response = httpx.post(url, verify=ssl_config, data=data)
        if response.status_code == 200:
            status, response = True, response.json()
            self.assertTrue(status) and self.assertIsInstance(response, list)
        else:
            status, response = False, response
            self.assertAlmostEqual(response.status_code, 429)
