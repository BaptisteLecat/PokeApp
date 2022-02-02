from os import name
from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class PokemonSelected(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    url = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
