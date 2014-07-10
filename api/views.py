import json

from rest_framework import viewsets
from rest_framework import generics
from celery.result import AsyncResult
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from api.serializers import *


# class SummonerViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     API endpoint that allows summoners to be viewed.
#     """
#     queryset = Summoner.objects.all()
#     serializer_class = SummonerSerializer


class SummonerList(generics.ListAPIView):
    """
    API endpoint that allows summoners to be listed with optional
    filtering via `region` portion of the URL.
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
    API endpoint that allows a single summoner to be retrieved,
    as determined by the `region` and `name` portions of the URL.
    """
    serializer_class = SummonerSerializer
    lookup_url_kwarg = 'name'

    def get_object(self, queryset=None, format=None):
        queryset = Summoner.objects.all()
        region = self.kwargs['region']
        name = self.kwargs['name']

        queryset = queryset.filter(region__iexact=region).get(name__iexact=name)

        return queryset


class ChampionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows champions to be viewed.
    """
    queryset = Champion.objects.all()
    serializer_class = ChampionSerializer


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows items to be viewed.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class SummonerSpellViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows summoner spells to be viewed.
    """
    queryset = SummonerSpell.objects.all()
    serializer_class = SummonerSpellSerializer


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows players from specific games to be viewed.
    """
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class RawStatViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows statistics from specific games to be viewed.
    """
    queryset = RawStat.objects.all()
    serializer_class = RawStatSerializer


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows games to be viewed.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned Games by region and summoner name of owner,
        by filtering against a `region` and `name` query parameter in the URL.

        Can filter by `region`, or `region` & `name`.

        `name` is not case sensitive.
        """

        region = self.request.QUERY_PARAMS.get('region', None)
        name = self.request.QUERY_PARAMS.get('name', None)

        if region is not None:
            if name is not None:
                # If we have both a region and name to filter against.
                self.queryset = self.queryset.filter(summoner_id=Summoner.objects.filter(region=region).filter(name__iexact=name))
            else:
                # If we only have a region to filter against.
                self.queryset = self.queryset.filter(summoner_id=Summoner.objects.filter(region=region))

        return self.queryset

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