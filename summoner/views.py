import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers
from celery.result import AsyncResult

from api.models import Summoner
from api.utils import NORTH_AMERICA, get_recent_matches, summoner_name_to_id, get_summoner_by_name
from api.tasks import async_get_summoner_by_name


# Unused.
# def summoner_info(request):
#     """
#     View to display summoner info given name and region.
#     """
#     #summoner = get_summoner_by_name(summoner_name, region)
#
#     #return render(request, 'summoner/summoner_base.html', {'summoner': summoner})
#
#     return render(request, 'summoner/summoner_base.html')


# Unused.
# def recent_games(request, summoner_name, region):
#     """
#     View to display match history for last 10 games played, given a summoner name and region.
#     """
#     get_recent_matches(summoner_name_to_id(summoner_name, region), region)
#     summoner = Summoner.objects.filter(name__iexact=summoner_name).get(region__iexact=region)
#     games = summoner.game_set.all()
#
#     print 'Recent matches found for {}: {}'.format(summoner_name, len(games))
#
#     return render(request, 'summoner/match_history.html', {'summoner': summoner, 'games': games})


# Unused.
# def async_summoner_info(request):
#     """
#     Test view for an async summoner info page.
#     """
#     return render(request, 'summoner/async_summoner_info.html')


# Unused.
# def ajax_summoner_info(request):
#     """
#     AJAX call for async_summoner_info().
#     """
#     print 'AJAX summoner id: {}'.format(request.POST.get('summoner_id'))
#
#     try:
#         response_data = serializers.serialize('json', Summoner.objects.filter(summoner_id=request.POST.get('summoner_id')))
#         response_ok = True
#     except ObjectDoesNotExist:
#         print 'Summoner ID {} not cached!'.format(request.POST.get('summoner_id'))
#         response_ok = False
#
#     if response_ok:
#         return HttpResponse(response_data, content_type='application/json')
#     else:
#         return HttpResponseNotFound('Summoner not found.')


@csrf_exempt
def ajax_query_start(request):
    """
    AJAX call to initiate async task of querying Riot API for summoner info.

    This calls a task that populates the DB with basic summoner info as well
    as adding the last 10 match histories to their game_set. It will not add matches
    that we already knew about (see `unique_together` constraint on Game model).

    Receives raw user input. Converts `region` to lowercase before passing to
    async_get_summoner_by_name task.

    Returns the task ID of the initiated task as JSON.
    """

    # when testing w/Adv Rest Client in chrome, must set header: X_REQUESTED_WITH = XMLHttpRequest
    if request.is_ajax():
        region = request.POST.get('region')
        summoner_name = request.POST.get('name')

        print 'body:', request.body
        print 'POST:', request.POST
        print 'region:', region
        print 'name:', summoner_name

        region = region.lower()     # ensure region is lowercase

        task = async_get_summoner_by_name.delay(summoner_name, region)
        request.session['task_id'] = task.id

        return HttpResponse(json.dumps(task.id), content_type='application/json')
    else:
        return HttpResponse('ajax_query_start(): Invalid request type.')