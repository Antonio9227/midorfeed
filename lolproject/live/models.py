from django.db import models
from time import time


# Create your models here.

# summoner model from database
class Summoner(models.Model):
    id = models.BigIntegerField(primary_key=True, null=False)  # id of summoner
    profileIconId = models.IntegerField(null=False)  # id of summoner icon
    name = models.CharField(max_length=25, null=False)  # summoner name
    summonerLevel = models.BigIntegerField()  # level of the summoner
    revisionDate = models.BigIntegerField()  # last time the user was seen online

    lastUpdate = models.BigIntegerField()  # last time this entry was updated
    favChamp = models.IntegerField(null=True)  # favorite champ of the user

    def __str__(self):
        return self.name


# league maps up to date
class Map(models.Model):
    id = models.IntegerField(primary_key=True)  # id of the map
    name = models.CharField(max_length=30)  # name of the map

    def __str__(self):
        return self.name


# defines each league game mode
class GameMode(models.Model):
    mode = models.CharField(primary_key=True, max_length=20)  # game mode name (id)
    description = models.CharField(max_length=100)  # game mode description (short description)

    def __str__(self):
        return self.decription


# summoner spells
class SummonerSpell(models.Model):
    key = models.IntegerField(primary_key=True)  # id of spell
    id = models.CharField(max_length=20, default="UNKNOWN")  # internal name of spell
    name = models.CharField(max_length=20)  # name of spell
    description = models.CharField(max_length=150)  # what the spell does


# game type
class GameType(models.Model):
    id = models.IntegerField(primary_key=True)  # id of game type
    map = models.CharField(max_length=30)  # map name, better use the map model instead though
    description = models.CharField(max_length=50)  # game description
