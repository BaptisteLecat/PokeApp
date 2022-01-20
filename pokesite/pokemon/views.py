from django.shortcuts import render, HttpResponse

import requests
import json
import sys
from pokemon.src.model.Pokemon import *
from pokemon.src.model.PokemonListed import *
from pokemon.src.model.MoveComplete import *
from pokemon.src.repository.pokemonRepository import *
from pokemon.src.repository.moveRepository import *

def index(request):
   result = requests.get('https://pokeapi.co/api/v2/pokemon/1')
   content = pokemon_from_dict(json.loads(result.text))
   return HttpResponse(content.name)


def pokemon(request, id):
    pokemon = fetchPokemon(None, id)
    listMoves = [];
    if(len(pokemon.moves) > 0):
        for index in range(3):
            listMoves.append(fetchMove(pokemon.moves[index].move.url))
    print(listMoves[0].effect_entries[0].short_effect)
    context = {'pokemon': pokemon, 'listMoves': listMoves}
    return render(request, 'pokemon/pokemon.html', context)

def list_pokemon(request):
    listPokemon = []
    next = request.GET.get('next', None)
    previous = request.GET.get('previous', None)
    search = request.GET.get('search', "")
    
    previousPageUrl = request.session.get('previousPageUrl', None)
    nextPageUrl = request.session.get('nextPageUrl', None)
    
    if(search != ""):
        try:
            listPokemon.append(fetchPokemon(None, search.lower()))
        except:
            listPokemon = []
    else:
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
                if 'previousPageUrl' in request.session:
                    del request.session['previousPageUrl']
                if 'nextPageUrl' in request.session:
                    del request.session['nextPageUrl']
                pokemonResultListed = fetchPokemonListed()  
        
        for pokemonResult in pokemonResultListed.results :
            listPokemon.append(fetchPokemon(pokemonResult.url))
            
        request.session['previousPageUrl'] = pokemonResultListed.previous
        request.session['nextPageUrl'] = pokemonResultListed.next    
        print(search)
        print(listPokemon[0].types[0].type.name)
    context = {'listPokemon': listPokemon, 'search': search, 'previousPageUrl': previousPageUrl, 'nextPageUrl': nextPageUrl}
        
    return render(request, 'pokemon/index.html', context)
    #return HttpResponse(listPokemon[0].id)
