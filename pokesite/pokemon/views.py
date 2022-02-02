from django.shortcuts import render, HttpResponse, HttpResponseRedirect

import requests
import json
import sys
from django.contrib import messages
from pokemon.models import *
from pokemon.src.model.Pokemon import *
from pokemon.src.model.PokemonListed import *
from pokemon.src.model.MoveComplete import *
from pokemon.src.repository.pokemonRepository import *
from pokemon.src.repository.moveRepository import *
from django.shortcuts import redirect


def index(request):
    result = requests.get('https://pokeapi.co/api/v2/pokemon/1')
    content = pokemon_from_dict(json.loads(result.text))
    return HttpResponse(content.name)


def pokemon(request, id):
    pokemon = fetchPokemon(None, id)
    listMoves = []
    if(len(pokemon.moves) > 3):
        for index in range(3):
            listMoves.append(fetchMove(pokemon.moves[index].move.url))
    context = {'pokemon': pokemon, 'listMoves': listMoves,
               'teams': Team.objects.all()}
    return render(request, 'pokemon/pokemon.html', context)


def pokemonAddToTeam(request, id):
    if request.method == 'POST':
        teamId = request.POST.get('teamId', None)
        if teamId != None:
            pokemon = fetchPokemon(None, id)
            resultTeam = Team.objects.filter(id=teamId)
            if len(resultTeam) > 0:
                resultPokemonSelected = PokemonSelected.objects.filter(
                    id=id, team=resultTeam[0])
                if len(resultPokemonSelected) <= 0:
                    # Le pokemon ne fait pas partie de la Team selectionnée, on l'ajoute.
                    pokemonUrl = pokemon.base_url+ str(pokemon.id)
                    newPokemonSelected = PokemonSelected(id=pokemon.id,
                        name=pokemon.name, url=pokemonUrl, team=resultTeam[0])
                    newPokemonSelected.save()
                    messages.success(
                        request, "Ce pokemon à été ajouté à votre Team!")
                else:
                    messages.error(
                        request, "Ce pokemon fait déjà partie de cette Team.")
            else:
                messages.error(
                    request, "Cette Team n'existe pas")
        else:
            messages.error(
                request, "Aucune Team sélectionnée.")
    else:
        messages.error(
            request, "Méthode HTTP inconnue.")
        
    return redirect("/")


def pokemonRemoveFromTeam(request, id):
    if request.method == 'POST':
        teamId = request.POST.get('teamId', None)
        if teamId != None:
            pokemon = fetchPokemon(None, id)
            resultTeam = Team.objects.filter(id=teamId)
            if len(resultTeam) > 0:
                resultPokemonSelected = PokemonSelected.objects.filter(
                    id=id, team=resultTeam[0])
                if len(resultPokemonSelected) > 0:
                    # Le pokemon fait partie de la Team selectionnée, on le supprime.
                    resultPokemonSelected[0].delete()
                    messages.success(
                        request, "Ce pokemon à été supprimé de votre Team!")
                else:
                    messages.error(
                        request, "Ce pokemon ne fait pas partie de cette Team.")
            else:
                messages.error(
                    request, "Cette Team n'existe pas")
        else:
            messages.error(
                request, "Aucune Team sélectionnée.")
    else:
        messages.error(
            request, "Méthode HTTP inconnue.")

    return redirect("/")


def list_pokemon(request):
    listPokemon = []
    next = request.GET.get('next', None)
    previous = request.GET.get('previous', None)
    search = request.GET.get('search', "")
    team = request.GET.get('team', "")

    previousPageUrl = request.session.get('previousPageUrl', None)
    nextPageUrl = request.session.get('nextPageUrl', None)

    selectedTeam = None

    if search != "" or team != "":
        if search != "":
            try:
                listPokemon.append(fetchPokemon(None, search.lower()))
            except:
                listPokemon = []
        else:
            try:
                selectedTeam = Team.objects.get(name=team)
                listPokemonTeam = PokemonSelected.objects.all().filter(
                    team=selectedTeam)
                for pokemonTeam in listPokemonTeam:
                    pokemon = fetchPokemon(pokemonTeam.url, None)
                    pokemon.team = selectedTeam
                    listPokemon.append(pokemon)
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

        for pokemonResult in pokemonResultListed.results:
            listPokemon.append(fetchPokemon(pokemonResult.url))

        request.session['previousPageUrl'] = pokemonResultListed.previous
        request.session['nextPageUrl'] = pokemonResultListed.next
        print(search)
        print(listPokemon[0].types[0].type.name)
    context = {'listPokemon': listPokemon, 'search': search, 'previousPageUrl': previousPageUrl,
               'nextPageUrl': nextPageUrl, 'teams': Team.objects.all(), 'selectedTeam': selectedTeam}

    return render(request, 'pokemon/index.html', context)
    # return HttpResponse(listPokemon[0].id)
