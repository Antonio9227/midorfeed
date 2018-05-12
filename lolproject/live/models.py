from django.db import models
from time import time


# Create your models here.

# summoner model from database
class Summoner(models.Model):
    accountId = models.BigIntegerField(primary_key=True, null=False)
    profileIconId = models.IntegerField(null=False)
    name = models.CharField(max_length=25, null=False)
    summonerLevel = models.BigIntegerField()
    revisionDate = models.BigIntegerField()

    lastUpdate = models.BigIntegerField()
    favChamp = models.IntegerField()

    def __str__(self):
        return self.name
