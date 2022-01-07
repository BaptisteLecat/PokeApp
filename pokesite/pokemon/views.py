from django.shortcuts import render, HttpResponse

import requests
import json
import sys
from pokemon.src.Pokemon import *


def index(request):
    result = requests.get('https://pokeapi.co/api/v2/pokemon/1')
    content = pokemon_from_dict(json.loads(result.text))
    return HttpResponse(content.name)
