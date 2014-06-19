import json

from rest_framework import viewsets
from rest_framework import generics
from celery.result import AsyncResult
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from api.serializers import *


# class SummonerViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     API endpoint that allows summoners to be viewed.
#     """
#     queryset = Summoner.objects.all()
#     serializer_class = SummonerSerializer


class SummonerList(generics.ListAPIView):
    """
    API endpoint that allows summoners to be viewed.
    """
    serializer_class = SummonerSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned summoners to a given region or name,
        by filtering against a `region` and/or `name` query parameter in the URL.
        """
        queryset = Summoner.objects.all()
        region = self.request.QUERY_PARAMS.get('region', None)
        name = self.request.QUERY_PARAMS.get('name', None)

        if region is not None:
            queryset = queryset.filter(region__iexact=region)
        if name is not None:
            queryset = queryset.filter(name__iexact=name)

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
        data = 'Invalid request type.'

    return HttpResponse(json.dumps(data), content_type='application/json')