from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_pokemon, name="list_pokemon"),
    path('pokemons/', views.list_pokemon, name="list_pokemon"),
    path('pokemons/<str:id>/', views.pokemon, name="pokemon"),
    path('pokemons/<str:id>/add-to-team/',
         views.pokemonAddToTeam, name="pokemonAddToTeam"),
    path('pokemons/<str:id>/remove-from-team/',
         views.pokemonRemoveFromTeam, name="pokemonRemoveFromTeam")
]
