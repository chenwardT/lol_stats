"""
Views for the API module.

Contains a API root view function as well as Django REST Framework generic class-based views.
Also contains an AJAX view for getting the state of a Celery task.
"""

import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
# from django.core.exceptions import ObjectDoesNotExist
from celery.result import AsyncResult
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

from api.serializers import *
from api.utils import standardize_name

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'summoners': reverse('summoner-list', request=request, format=format),
        'champions': reverse('champion-list', request=request, format=format),
        'items': reverse('item-list', request=request, format=format),
        'spells': reverse('spell-list', request=request, format=format),
        'games': reverse('game-list', request=request, format=format),
        'stats': reverse('stat-list', request=request, format=format),
        'players': reverse('player-list', request=request, format=format),
        'leagues': reverse('league-list', request=request, format=format),
        'league-entries': reverse('league-entry-list', request=request, format=format),
        'teams': reverse('team-list', request=request, format=format),
        'rosters': reverse('roster-list', request=request, format=format),
        'teammemberinfo': reverse('teammemberinfo-list', request=request, format=format),
    })


class SummonerList(generics.ListAPIView):
    """
    API endpoint that allows summoners to be listed.

    Optionally allows for filtering via the `region` portion of the URL.
    """
    serializer_class = SummonerSerializer
    paginate_by = 10

    def get_queryset(self, format=None):
        """
        This view returns a list of all summoners for a region
        as determined by the `region` portion of the URL.
        """
        queryset = Summoner.objects.all()

        if 'region' in self.kwargs:
            region = self.kwargs['region']
            queryset = queryset.filter(region__iexact=region)

        return queryset


class SummonerDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a summoner to be retrieved.

    Summoner is specified by `region` and `name` portions of the URL.
    """
    serializer_class = SummonerSerializer

    def get_object(self, queryset=None, format=None):
        queryset = Summoner.objects.all()
        region = self.kwargs['region']
        name = self.kwargs['name']
        name = standardize_name(name)

        obj = get_object_or_404(queryset.filter(region__iexact=region), std_name=name)

        return obj


class ChampionList(generics.ListAPIView):
    """
    API endpoint that allows champions to be listed.
    """
    queryset = Champion.objects.all()
    serializer_class = ChampionSerializer


class ChampionDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a champion to be retrieved.

    Champion is specified by `name` portion of the URL.
    """
    queryset = Champion.objects.all()
    serializer_class = ChampionSerializer

    def get_object(self, queryset=None):
        name = self.kwargs.get('name', None)

        if name is not None:
            obj = get_object_or_404(self.queryset, name__iexact=name)

        return obj


class ItemList(generics.ListAPIView):
    """
    API endpoint that allows items to be listed.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows an item to be retrieved.

    Item is specified by the `name` portion of the URL.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get_object(self, queryset=None):
        name = self.kwargs.get('name', None)

        if name is not None:
            obj = get_object_or_404(self.queryset, name__iexact=name)

        return obj


class SummonerSpellList(generics.ListAPIView):
    """
    API endpoint that allows summoner spells to be listed.
    """
    queryset = SummonerSpell.objects.all()
    serializer_class = SummonerSpellSerializer


class SummonerSpellDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a spell to be retrieved.

    Spell is specified by the `name` portion of the URL.
    """
    queryset = SummonerSpell.objects.all()
    serializer_class = SummonerSpellSerializer

    def get_object(self, queryset=None):
        name = self.kwargs.get('name', None)

        if name is not None:
            obj = get_object_or_404(self.queryset, name__iexact=name)

        return obj


class PlayerList(generics.ListAPIView):
    """
    API endpoint that allows match participants to be listed.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    # def get_queryset(self):
    #     self.queryset = self.queryset.order_by('team_id')
    #     return self.queryset


class PlayerDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a match participant to be retrieved.

    Participant is specified by the `name` portion of the URL.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def get_object(self, queryset=None):
        name = self.kwargs.get('name', None)

        if name is not None:
            obj = get_object_or_404(self.queryset, name__iexact=name)

        return obj


class RawStatList(generics.ListAPIView):
    """
    API endpoint that allows statistics from games to be viewed.
    """
    queryset = RawStat.objects.all()
    serializer_class = RawStatSerializer


class RawStatDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows statistics from a game to be retrieved.

    Statistics are specified by related game via the `game_id` portion of URL.
    """
    queryset = RawStat.objects.all()
    serializer_class = RawStatSerializer

    def get_object(self):
        game_id = self.kwargs.get('game_id', None)

        if game_id is not None:
            obj = get_object_or_404(Game, game_id=game_id)

            # Here we are assuming that every Game object has a related RawStat (.stats) object.
            return obj.stats


class GameList(generics.ListAPIView):
    """
    API endpoint that allows match history to be viewed.

    Optionally allows filtering by `region` and `name` (via URL portions) of
    the summoner who the game(s) belong to.

    Games are ordered chronologically, by most recent first.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    paginate_by = 10

    def get_queryset(self):
        region = self.kwargs.get('region', None)
        name = self.kwargs.get('name', None)

        if region is not None:
            if name is not None:
                name = standardize_name(name)
                self.queryset = self.queryset.filter(
                    summoner_id=Summoner.objects.filter(region__iexact=region).filter(
                        std_name=name)).order_by('-create_date')

        return self.queryset


class GameDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a match history to be retrieved.

    Match is specified by `region` and `game_id` portion of the URL.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_object(self):
        region = self.kwargs.get('region', None)
        game_id = self.kwargs.get('game_id', None)

        if region is not None:
            if game_id is not None:
                obj = get_object_or_404(Game, region_iexact=region, game_id=game_id)

                return obj


class LeagueList(generics.ListAPIView):
    """
    API endpoint that allows leagues to be viewed.

    Optionally allows filtering by `region`.
    """
    queryset = League.objects.all()
    serializer_class = LeagueSerializer
    paginate_by = 10

    def get_queryset(self):
        region = self.kwargs.get('region', None)

        if region is not None:
            self.queryset = self.queryset.filter(region__iexact=region)

        return self.queryset


class LeagueDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a league to be retrieved.

    Selected via `region`, `queue`, `tier` and `name` URL params.
    """
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

    def get_object(self, queryset=None):
        region = self.kwargs.get('region', None)
        queue = self.kwargs.get('queue', None)
        tier = self.kwargs.get('tier', None)
        name = self.kwargs.get('name', None)

        print region + queue + tier + name

        if region is not None:
            if queue is not None:
                if tier is not None:
                    if name is not None:
                        obj = self.queryset.filter(
                            region__iexact=region).filter(
                            queue=queue).filter(
                            tier=tier).get(
                            name=name)

                        return obj


class LeagueEntryList(generics.ListAPIView):
    """
    API endpoint that allows league entries to be viewed.

    Optionally allows filtering by `region`.
    """
    queryset = LeagueEntry.objects.all()
    serializer_class = LeagueEntrySerializer
    paginate_by = 10

    def get_queryset(self):
        region = self.kwargs.get('region', None)

        if region is not None:
            self.queryset = self.queryset.filter(league__region__iexact=region)

            return self.queryset


class LeagueEntryDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a league entry to be retrieved.

    Selected via `region` and `id` URL params. `id` corresponds to
    `player_or_team_id` field of LeagueEntry model.
    """
    queryset = LeagueEntry.objects.all()
    serializer_class = LeagueEntrySerializer

    def get_object(self, queryset=None):
        region = self.kwargs.get('region')
        id = self.kwargs.get('id')

        if id is not None:
            obj = self.queryset.filter(league__region__iexact=region).get(player_or_team_id=id)

        return obj


class TeamList(generics.ListAPIView):
    """
    API endpoint that allows team entries to be viewed.

    Optionally filtered by `region` URL param.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    paginate_by = 10

    def get_queryset(self):
        region = self.kwargs.get('region', None)

        if region is not None:
            self.queryset = self.queryset.filter(region__iexact=region)

        return self.queryset


class TeamDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a team entry to be retrieved.

    Selected via `region` and `full_id` URL params.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_object(self, queryset=None):
        region = self.kwargs.get('region', None)
        full_id = self.kwargs.get('full_id', None)

        if region is not None:
            if full_id is not None:
                obj = get_object_or_404(Team, region__iexact=region, full_id=full_id)

        return obj


class RosterList(generics.ListAPIView):
    """
    API endpoint that allows roster entries to be viewed.

    #Optionally filtered by `region` URL param.
    """
    queryset = Roster.objects.all()
    serializer_class = RosterSerializer
    paginate_by = 10

    def get_queryset(self):
        region = self.kwargs.get('region', None)

        if region is not None:
            self.queryset = self.queryset.filter(region__iexact=region)

        return self.queryset


class RosterDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a roster entry to be retrieved.

    #Selected via `region` and `full_id` URL params.
    """
    queryset = Roster.objects.all()
    serializer_class = RosterSerializer

    def get_object(self, queryset=None):
        region = self.kwargs.get('region', None)
        full_id = self.kwargs.get('full_id', None)

        if region is not None:
            if full_id is not None:
                obj = get_object_or_404(Roster, region__iexact=region, full_id=full_id)

        return obj
    

class TeamMemberInfoList(generics.ListAPIView):
    """
    API endpoint that allows TeamMemberInfo entries to be viewed.

    #Optionally filtered by `region` URL param.
    """
    queryset = TeamMemberInfo.objects.all()
    serializer_class = TeamMemberInfoSerializer
    paginate_by = 10

    def get_queryset(self):
        # region = self.kwargs.get('region', None)
        #
        # if region is not None:
        #     self.queryset = self.queryset.filter(region__iexact=region)

        return self.queryset


class TeamMemberInfoDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a TeamMemberInfo entry to be retrieved.

    #Selected via `region` and `full_id` URL params.
    """
    queryset = TeamMemberInfo.objects.all()
    serializer_class = TeamMemberInfoSerializer

    # def get_object(self, queryset=None):
    #
    #     # if region is not None:
    #     #     if full_id is not None:
    #     #         obj = get_object_or_404(TeamMemberInfo, region__iexact=region, full_id=full_id)
    #
    #     return obj


@csrf_exempt
def get_task_state(request):
    """
    AJAX view to report task state, given a task ID (UUID) in the POST body.

    Returns the state or an error message as JSON.
    When "SUCCESS" is returned, page scripts know they can query and display the related results.
    """

    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            # Strip double quotes that AngularJS adds.
            task_id = task_id.replace('"', '')
            task = AsyncResult(task_id)
            data = task.state
            print task_id
            print data
        else:
            data = 'No task_id in the request.'
    else:
        data = 'get_task_state(): Invalid request type.'

    return HttpResponse(json.dumps(data), content_type='application/json')
