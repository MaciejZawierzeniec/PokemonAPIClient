from typing import Dict, Optional, List

import requests


class PokeClient:
    def __init__(self, poke_url: str):
        self.url = poke_url

    def get_pokemons(self, limit: int = 100, offset: int = 0) -> Optional[Dict]:
        payload = {'limit': limit, 'offset': offset}
        response = requests.get(f'{self.url}/pokemon/', params=payload)
        if response.ok:
            return response.json()
        else:
            print(response.status_code)

    def get_all_pokemons_while(self) -> Optional[List[Dict]]:
        response = self.get_pokemons()
        _offset = 0
        all_pokemons = []
        while response['results']:
            all_pokemons.extend(response['results'])
            _offset += 100
            response = self.get_pokemons(offset=_offset)
        return all_pokemons

    def get_all_pokemons_next(self):
        response = self.get_pokemons()
        all_pokemons = response['results']
        while response['next']:
            response = requests.get(response['next']).json()
            all_pokemons.extend(response['results'])
        print(all_pokemons)

    def get_all_pokemons_for(self):
        pokemon_no = self.get_pokemons(limit=1)['count']
        all_pokemons = []
        for offset in range(0, pokemon_no, 100):
            all_pokemons.extend(self.get_pokemons(offset=offset).get('results', []))
        return all_pokemons


client = PokeClient(poke_url='https://pokeapi.co/api/v2')
print(client.get_all_pokemons_for())
