from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from riot import riotapi
from live.models import Summoner
from champion.models import *
import random
import datetime
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
            summoner.favChamp = 0

        adjectives = ["Filthy", "Degenerate", "Disgusting", "Detestable", "Dirty", "Despicable",
                      "Awful", "Villainous", "Cheap"]

        exclamations = ["Imagine my shock.", "Yuck.", "I don't know what else I expected.",
                        "Srlsy?..", "Another one of those...", "Really?", "How impressive."]

        data["adjective"] = adjectives[(summoner.id + summoner.favChamp) % len(adjectives)]
        data["exclamation"] = exclamations[(summoner.id + summoner.favChamp) % len(exclamations)]
        data["title"] = summoner.name
        data["show_searchBar"] = False
        data['summoner'] = summoner
        data['status'] = self.status
        pdate = datetime.datetime.utcfromtimestamp(int(summoner.revisionDate) / 1000)
        data['onlineDate'] = pdate.strftime("%d %B %y")
        data['onlineTime'] = pdate.strftime("%H:%M:%S")
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


class SorryView(TemplateView):
    template_name = "sorry.html"


class RankView(TemplateView):
    template_name = "rank.html"
    sumId = ""

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        leagues = riotapi.league(self.sumId)

        icons = {
            'UNRANKED': 0,
            'BRONZE': 1,
            'SILVER': 2,
            'GOLD': 3,
            'PLATINUM': 4,
            'DIAMOND': 5,
            'MASTER': 6,
            'CHALLENGER': 7
        }
        if len(leagues) > 0:
            data['hasData'] = True

        for i in range(0, len(leagues)):
            leagues[i]['tierbg'] = icons[leagues[i]['tier']] * -64
            if "flex" in leagues[i]['queueType'].lower():
                leagues[i]['flexStatus'] = "[FLEX]"

        data['leagues'] = leagues
        return data

    def get(self, request):
        self.sumId = request.GET.get('summoner', False)

        return super().get(request)


class MasteryView(TemplateView):
    template_name = "mastery.html"
    sumId = ""

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["api_version"] = riotapi.version

        masteries = riotapi.champMastery(self.sumId)
        if len(masteries) > 0:
            data['hasData'] = True

        top = []

        for i in range(0, min(10, len(masteries))):
            champ = Champion.objects.get(key=masteries[i]['championId'])
            masteries[i]['icon'] = champ.id
            pdate = datetime.datetime.utcfromtimestamp(int(masteries[i]['lastPlayTime']) / 1000)

            masteries[i]['lastPlaydate'] = pdate.strftime("%d %B %y")
            masteries[i]['lastPlayhour'] = pdate.strftime("%H:%M:%S")
            masteries[i]['champName'] = champ.name
            top.append(masteries[i])

        data['masteries'] = top
        return data

    def get(self, request):
        self.sumId = request.GET.get('summoner', False)

        return super().get(request)


class HistoryView(TemplateView):
    template_name = "empty.html"
    sumId = ""

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        leagues = riotapi.league(self.sumId)

        icons = {
            'UNRANKED': 0,
            'BRONZE': 1,
            'SILVER': 2,
            'GOLD': 3,
            'PLATINUM': 4,
            'DIAMOND': 5,
            'MASTER': 6,
            'CHALLENGER': 7
        }
        for i in range(0, len(leagues)):
            leagues[i]['tierbg'] = icons[leagues[i]['tier']] * -64
            if "flex" in leagues[i]['queueType'].lower():
                leagues[i]['flexStatus'] = "[FLEX]"

        data['leagues'] = leagues
        return data

    def get(self, request):
        self.sumId = request.GET.get('summoner', False)

        return super().get(request)
