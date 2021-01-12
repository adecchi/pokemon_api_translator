from unittest import TestCase, mock

import requests
import requests_mock
import json
import os
from src.proxy.requests import Request


class TestRequest(TestCase):

    def test_get(Mocker):
        with requests_mock.Mocker() as m:
            pokemon_species = os.path.join(os.path.dirname(__file__), 'samples/pokemon-species.json')
            with open(pokemon_species, 'r') as json_data:
                data = json.load(json_data)
            m.get("https://pokeapi.co/api/v2/pokemon-species/", json=data)
            response = requests.get("https://pokeapi.co/api/v2/pokemon-species/")
            response = json.loads(response.text)
            assert len(response['results']) == len(data['results'])

    def test_post(Mocker):
        with requests_mock.Mocker() as m:
            pokemon_species = os.path.join(os.path.dirname(__file__), 'samples/api_funtranslations_com.json')
            with open(pokemon_species, 'r') as json_data:
                data = json.load(json_data)
            m.post("https://pokeapi.co/api/v2/pokemon-species/", json=data)
            response = requests.post("https://pokeapi.co/api/v2/pokemon-species/")
            response = json.loads(response.text)
            assert response['contents']['translated'] == data['contents']['translated']
