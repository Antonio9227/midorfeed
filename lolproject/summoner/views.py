from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from riot import riotapi
from live.models import Summoner
from champion.models import *
import random
from time import time
import json


class SummonerView(TemplateView):
    template_name = "summoner.html"
    sumName = ""
    status = ""

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        data["search_header"] = "League stalk simulator 2018"
        data["search_text"] = "It's like you went on a long romantic walk in the park with the summoner you're " \
                              "stalking... But only you know about it"
        data["search_button"] = "Search"
        data["search_placeholder"] = "Summoner name"

        data["show_searchBar"] = True
        if not self.sumName:
            return data

        data["api_version"] = riotapi.version
        summoner = Summoner.objects.filter(name__iexact=self.sumName.lower()).first()

        # if summoner does not exists in db or was updated more than 1h ago
        if not summoner or (time() - summoner.lastUpdate > 3600):
            riotSum = riotapi.summonerByName(self.sumName)
            if riotSum == -1:
                data['status'] = "Summoner not found. Try again?"
                data['show_searchBar'] = True
                return data
            else:
                if summoner:
                    summoner.delete()
                s = Summoner(id=riotSum['id'], profileIconId=riotSum['profileIconId'],
                             name=riotSum['name'], summonerLevel=riotSum['summonerLevel'],
                             revisionDate=riotSum['revisionDate'], lastUpdate=time())
                s.save()
                summoner = s
                print("new summoner:" + s.name)

        if not summoner.favChamp:
            mastery = riotapi.champMastery(summoner.id)
            if len(mastery) > 0:
                mastery = mastery[0]
                if len(mastery) > 0:
                    summoner.favChamp = int(mastery['championId'])
                    summoner.save()

        if summoner.favChamp:
            champ = Champion.objects.get(key=summoner.favChamp)
            data["background"] = "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" \
                                 + champ.id + "_0.jpg"
            data["mainchamp"] = champ.name
        else:
            data["mainchamp"] = "Nothing"
            summoner.favChamp=0

        adjectives = ["Filthy", "Degenerate", "Disgusting", "Detestable", "Dirty", "Despicable",
                      "Awful", "Villainous", "Cheap"]

        exclamations = ["Imagine my shock.", "Yuck.", "I don't know what else I expected.",
                        "Srlsy?..", "Another one of those...", "Really?", "How impressive."]

        data["adjective"] = adjectives[(summoner.id + summoner.favChamp) % len(adjectives)]
        data["exclamation"] = exclamations[(summoner.id + summoner.favChamp) % len(exclamations)]
        data["title"]=summoner.name
        data["show_searchBar"] = False
        data['summoner'] = summoner
        data['status'] = self.status

        return data

    def get(self, request):
        self.status = ""
        self.sumName = request.GET.get('summoner', False)

        if not self.sumName:
            self.sumName = request.GET.get('name', False)

        # if summoner name was not provided via GET var, skip everything below
        if not self.sumName:
            self.status = ""
            return super().get(request)

        return super().get(request)
