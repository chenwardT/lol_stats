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

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'summoners': reverse('summoner-list', request=request, format=format),
        'champions': reverse('champion-list', request=request, format=format),
        'items': reverse('item-list', request=request, format=format),
        'spells': reverse('spell-list', request=request, format=format),
        'games': reverse('game-list', request=request, format=format),
        'stats': reverse('stat-list', request=request, format=format),
        'players': reverse('player-list', request=request, format=format)
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


# TODO: Fix this so DB queries aren't tripped up by "erroneous" whitespace in names,
#  a la Riot API behavior
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

        obj = get_object_or_404(queryset.filter(region__iexact=region), name__iexact=name)

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
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    paginate_by = 10

    def get_queryset(self):
        region = self.kwargs.get('region', None)
        name = self.kwargs.get('name', None)

        if region is not None:
            if name is not None:
                self.queryset = self.queryset.filter(
                    summoner_id=Summoner.objects.filter(region__iexact=region).filter(name__iexact=name))

        return self.queryset


class GameDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a match history to be retrieved.

    Match is specified by game_id portion of the URL.
    """
    queryset = RawStat.objects.all()
    serializer_class = RawStatSerializer

    def get_object(self):
        region = self.kwargs.get('region', None)
        game_id = self.kwargs.get('game_id', None)

        if region is not None:
            if game_id is not None:
                obj = get_object_or_404(Game, region=region, game_id=game_id)

                # Here we are assuming that every Game object has a related RawStat (.stats) object.
                return obj.stats


@csrf_exempt
def get_task_state(request):
    """
    A view to report task state, given a task ID (UUID), to an AJAX call.

    Returns the state or an error message as JSON.
    When "SUCCESS" is returned, page scripts know they can query and display the related results.
    """
    if request.is_ajax():
        if 'task_id' in request.POST.keys() and request.POST['task_id']:
            task_id = request.POST['task_id']
            task = AsyncResult(task_id)
            data = task.state
        else:
            data = 'No task_id in the request.'
    else:
        data = 'get_task_state(): Invalid request type.'

    return HttpResponse(json.dumps(data), content_type='application/json')
