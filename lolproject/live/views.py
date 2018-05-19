from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import CreateView
import requests
import json
from live.models import Summoner
from champion.models import Champion
from live.models import *

from riot import riotapi
from riot.riotapi import ParticipantDTO
from time import time

from django.http import JsonResponse


# Create your views here.


def LeagueView(request):
    # template_name = "json.html"
    id = request.GET.get("summoner")

    if not id:
        return JsonResponse({'error': 'summoner not specified.'})

    league = riotapi.league(id)

    tier = "UNRANKED"
    rank = ""
    league_name = ""

    for i in range(0, len(league)):
        if league[i].get('queueType') == "RANKED_SOLO_5x5":
            l = league[i]
            tier = l['tier']
            rank = l['rank']
            league_name = l['leagueName']

    summoner = riotapi.summonerById(id)

    if summoner == -1:  # protection in case shit hits the fan and some idiot plays with the request
        summoner = {'summonerLevel': -1}

    return JsonResponse({'tier': tier, 'rank': rank, 'leagueName': league_name, 'level': summoner['summonerLevel']})


class LiveGame(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        if not riotapi.is_key_valid():
            data["invalidKey"] = True

        sumName = self.request.GET.get('summoner', False)
        status = ""

        data["search_header"] = "Find who you're playing against."
        data["search_text"] = "See if you have any rights to call them noobs.";
        data["search_button"] = "Live Game"
        data["search_placeholder"] = "Summoner name"

        data["show_searchBar"] = True
        if not sumName:
            return data

        data["api_version"] = riotapi.version
        summoner = Summoner.objects.filter(name__iexact=sumName.lower()).first()

        # if summoner does not exists in db or was updated more than 1h ago
        if not summoner or (time() - summoner.lastUpdate > 3600):
            riotSum = riotapi.summonerByName(sumName)
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
        game = riotapi.activeGame(summoner.id)

        if game == -1:
            status = "Summoner is currently not in any active game"
            data['show_searchBar'] = True
        else:
            p = game['participants']
            team1 = []
            team2 = []

            for i in range(0, len(p)):
                participant = ParticipantDTO(p[i])
                if participant.summonerId == summoner.id:
                    participant.focus = 1

                if participant.teamId == 100:
                    team1.append(participant)
                else:
                    team2.append(participant)

            data['team1'] = team1
            data['team2'] = team2
            data['gameLength'] = game['gameLength']
            config = GameType.objects.get(id=int(game['gameQueueConfigId']))
            data['gameType'] = config.description
            data['map'] = Map.objects.get(id=int(game['mapId'])).name
            data['gameStartTime'] = game['gameStartTime']
            data['title'] = summoner.name
            data['show_searchBar'] = False

        data['status'] = status

        return data


class DEBUG(TemplateView):
    template_name = "debug.html"

    def get_context_data(self, **kwargs):
        r = requests.get("https://api.myjson.com/bins/g2x7e");
        data = json.loads(r.content)

        for i in range(0, len(data)):
            s = data[i]
            # gameType.objects.create(id=int(s['id']), map=s['map'], description=s['desc'])

        # GameMode.objects.create(mode="CLASSIC", description="")
        # GameMode.objects.create(mode="ODIN", description="Dominion")
        # GameMode.objects.create(mode="ARAM", description="ARAM")
        # GameMode.objects.create(mode="TUTORIAL", description="Tutorial")
        # GameMode.objects.create(mode="URF", description="Ultra Rapid Fire")
        # GameMode.objects.create(mode="DOOMBOTSTEEMO", description="Teemo DoomBots")
        # GameMode.objects.create(mode="ONEFORALL", description="One for all")
        # GameMode.objects.create(mode="ASCENSION", description="Ascension")
        # GameMode.objects.create(mode="FIRSTBLOOD", description="First Blood")
        # GameMode.objects.create(mode="KINGPORO", description="King Poro")
        # GameMode.objects.create(mode="SIEGE", description="Nexus Siege")
        # GameMode.objects.create(mode="ASSASSINATE", description="Blood Hunt")
        # GameMode.objects.create(mode="ARSR", description="All Random Summoner's Rift")
        # GameMode.objects.create(mode="DARKSTAR", description="Dark Star: Singularity")
        # GameMode.objects.create(mode="STARGUARDIAN", description="Star Guardian Invasion")
        # GameMode.objects.create(mode="PROJECT", description="PROJECT: Hunter's")

        # Map.objects.create(id=1, name="Summoner's Rift (Summer)")
        # Map.objects.create(id=2, name="Summoner's Rift (Autumn)")
        # Map.objects.create(id=3, name="The Proving Grounds")
        # Map.objects.create(id=4, name="Twisted Treeline (Original)")
        # Map.objects.create(id=8, name="The Crystal Scar")
        # Map.objects.create(id=10, name="Twister Treeline")
        # Map.objects.create(id=11, name="Summoner's Rift")
        # Map.objects.create(id=12, name="Howling Abyss")
        # Map.objects.create(id=14, name="Butcher's Bridge")
        # Map.objects.create(id=16, name="Cosmic Ruins")
        # Map.objects.create(id=18, name="Valoran City Park")
        # Map.objects.create(id=19, name="Substructure 43")

        return super().get_context_data(**kwargs);
