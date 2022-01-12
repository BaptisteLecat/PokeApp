from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_pokemon, name="list_pokemon"),
    path('pokemons', views.list_pokemon, name="list_pokemon")
]
