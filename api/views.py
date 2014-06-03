from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets

from api.serializers import *
from api.utils import get_summoner_by_name, summoner_name_to_id, get_recent_matches, NORTH_AMERICA


class SummonerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows summoners to be viewed.
    """
    queryset = Summoner.objects.all()
    serializer_class = SummonerSerializer


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


def summoner_info(request, summoner_name, region=NORTH_AMERICA):
    """
    View to display summoner info given name and region.
    """
    summoner = get_summoner_by_name(summoner_name, region)

    return render(request, 'summoner_info.html', {'summoner': summoner})


def recent_games(request, summoner_name, region=NORTH_AMERICA):
    """
    View to display match history for last 10 games played, given a summoner name and region.
    """
    get_recent_matches(summoner_name_to_id(summoner_name, region), region)
    summoner = Summoner.objects.filter(name__iexact=summoner_name).get(region__iexact=region)
    games = summoner.game_set.all()


    print 'Recent matches found for {}: {}'.format(summoner_name, len(games))

    return render(request, 'match_history.html', {'summoner': summoner, 'games': games})


def view_items(request):
    """
    View to display all items.
    """
    items = Item.objects.all().order_by('item_id')

    return render(request, 'items.html', {'items': items})


def async_summoner_info(request):
    """
    Test view for an async summoner info page.
    """

    return render(request, 'async_summoner_info.html')


def ajax_summoner_info(request):
    """
    AJAX call for async_summoner_info().
    """

    #print 'AJAX summoner id: {}'.format(summoner_id)
    #print request

    print 'AJAX summoner id: {}'.format(request.POST.get('summoner_id'))

    #if request.is_ajax():
    try:
        response_data = serializers.serialize('json', Summoner.objects.filter(summoner_id=request.POST.get('summoner_id')))
    except ObjectDoesNotExist:
        print 'Summoner ID {} not cached!'.format(request.POST.get('summoner_id'))

    return HttpResponse(response_data, content_type='application/json')