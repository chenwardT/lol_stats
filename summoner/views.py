from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from rest_framework import serializers
from api.models import Summoner
from api.utils import NORTH_AMERICA, get_recent_matches, summoner_name_to_id, get_summoner_by_name


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


def async_summoner_info(request):
    """
    Test view for an async summoner info page.
    """
    return render(request, 'async_summoner_info.html')


def ajax_summoner_info(request):
    """
    AJAX call for async_summoner_info().
    """
    print 'AJAX summoner id: {}'.format(request.POST.get('summoner_id'))

    try:
        response_data = serializers.serialize('json', Summoner.objects.filter(summoner_id=request.POST.get('summoner_id')))
        response_ok = True
    except ObjectDoesNotExist:
        print 'Summoner ID {} not cached!'.format(request.POST.get('summoner_id'))

    if response_ok:
        return HttpResponse(response_data, content_type='application/json')
    else:
        return HttpResponseNotFound('Page not found.')