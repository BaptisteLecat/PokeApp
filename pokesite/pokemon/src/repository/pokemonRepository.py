from pokemon.src.model.PokemonListed import *
from pokemon.src.model.Pokemon import *
import requests
import json

def fetchPokemonListed(url=None) -> PokemonListed:
    if(url != None):
        assert isinstance(url, str)
        result = requests.get(
            url)
    else:
        result = requests.get(
            'https://pokeapi.co/api/v2/pokemon?limit=10')
    return pokemon_listed_from_dict(json.loads(result.text))


def fetchPokemon(url=None, identifier=None) -> Pokemon:
    if(url != None):
        assert isinstance(url, str)
        result = requests.get(
            url)
    else:
        if(identifier != None):
            result = requests.get('https://pokeapi.co/api/v2/pokemon/' + identifier)
            result.raise_for_status()   
    return pokemon_from_dict(json.loads(result.text))
