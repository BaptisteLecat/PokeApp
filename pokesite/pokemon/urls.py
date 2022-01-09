from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('pokemons', views.list_pokemon, name="list_pokemon")
]
