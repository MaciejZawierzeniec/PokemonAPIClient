import json
from typing import Dict, Optional, List

import requests

from decorators import assert_endpoint_exists
from endpoints import ENDPOINTS


class PokeClient:
    def __init__(self, poke_url: str):
        self.url = poke_url

    def get_pokemons(self, limit: int = 100, offset: int = 0) -> Optional[Dict]:
        return self._get(endpoint=ENDPOINTS['pokemon'], limit=limit, offset=offset)

    def get_all_pokemons(self) -> Optional[List[Dict]]:
        return self._get_all(endpoint=ENDPOINTS['pokemon'])

    def get_pokemon(self, url: str) -> Optional[Dict]:
        return self._get_by_url(url)

    @assert_endpoint_exists
    def _get(self, endpoint: str, limit: int = 100, offset: int = 0) -> Optional[Dict]:
        payload = {'limit': limit, 'offset': offset}
        response = requests.get(f'{self.url}/{endpoint}/', params=payload)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def _get_by_url(self, url: str) -> Optional[Dict]:
        response = requests.get(url)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def _get_all(self, endpoint: str) -> Optional[List[Dict]]:
        items_count = self._get(endpoint=endpoint, limit=1)['count']
        all_items = []
        for offset in range(0, items_count, 100):
            all_items.extend(self._get(endpoint=endpoint, limit=100, offset=offset).get('results', []))
        return all_items


client = PokeClient(poke_url='https://pokeapi.co/api/v2')
all_pokemons = client.get_pokemons(limit=5)['results']

all_pokemons_details = []
for pokemon in all_pokemons:
    pokemon_data = client.get_pokemon(url=pokemon['url'])
    all_pokemons_details.append(pokemon_data)

with open('all_pokemons_details.jsonl', 'w') as outfile:
    for pokemon in all_pokemons_details:
        json.dump(pokemon, outfile)
        outfile.write('\n')
