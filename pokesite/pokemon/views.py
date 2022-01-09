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
    #context = {'year': year, 'article_list': a_list}
    #return render(request, 'news/year_archive.html', context)
    request.session['previousPageUrl'] = pokemonResultListed.previous
    request.session['nextPageUrl'] = pokemonResultListed.next
    return HttpResponse(listPokemon[0].id)
