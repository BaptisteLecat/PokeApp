from django.shortcuts import render, HttpResponse

import requests
import json
import sys
from pokemon.src.model.Pokemon import *
from pokemon.src.model.PokemonListed import *
from pokemon.src.repository.pokemonRepository import *

def index(request):
   result = requests.get('https://pokeapi.co/api/v2/pokemon/1')
   content = pokemon_from_dict(json.loads(result.text))
   return HttpResponse(content.name)


def list_pokemon(request):
    next = request.GET.get('next', None)
    previous = request.GET.get('previous', None)
    previousPageUrl = request.session.get('previousPageUrl', None)
    nextPageUrl = request.session.get('nextPageUrl', None)
    print(previousPageUrl)
    if (next == "true"):
        if(nextPageUrl != None):
            print(nextPageUrl)
            pokemonResultListed = fetchPokemonListed(nextPageUrl)
        else:
            pokemonResultListed = fetchPokemonListed()
    else:
        if (previous == "true"):
            if(previousPageUrl != None):
                pokemonResultListed = fetchPokemonListed(previousPageUrl)
            else:
                pokemonResultListed = fetchPokemonListed()
        else:
            del request.session['previousPageUrl']
            del request.session['nextPageUrl']
            pokemonResultListed = fetchPokemonListed()
    
    listPokemon = []
    
    for pokemonResult in pokemonResultListed.results :
        listPokemon.append(fetchPokemon(pokemonResult.url))
        
    request.session['previousPageUrl'] = pokemonResultListed.previous
    request.session['nextPageUrl'] = pokemonResultListed.next
    
    print(listPokemon[0].types[0].type.name)
    context = {'listPokemon': listPokemon}
    return render(request, 'pokemon/index.html', context)
    #return HttpResponse(listPokemon[0].id)
