from django.shortcuts import render, HttpResponse

import requests
import json


def index(request):
    yoko = requests.get('https://pokeapi.co/api/v2/pokemon?limit=10')
    content = yoko.text
    return HttpResponse(content)
