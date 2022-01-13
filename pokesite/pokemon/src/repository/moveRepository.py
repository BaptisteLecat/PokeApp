from pokemon.src.model.PokemonListed import *
from pokemon.src.model.MoveComplete import *
import requests
import json

def fetchMove(url : str) -> MoveComplete:
    assert isinstance(url, str)
    result = requests.get(url)
    result.raise_for_status()   
    return move_complete_from_dict(json.loads(result.text))
