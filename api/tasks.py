"""
Celery tasks.
"""



from time import sleep
from datetime import datetime

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from api.models import Summoner
from api.utils import riot_api, CACHE_SUMMONER, get_recent_matches, get_league_by_summoner_id, get_teams_by_summoner_id

@shared_task
def async_get_summoner_by_name(summoner_name, region):
    """
    Get summoner info, by name, from Riot API, into cache.

    Specifically, it gets basic summoner data as well as match history (last 10 games).
    Riot API is only queried if Summoner object is older than `CACHE_SUMMONER`.
    """

    print('summoner_name =', summoner_name)
    print('region =', region)

    # First we convert `summoner_name` to formatted name.
    # To query a summoner by name, we must submit its standardized name.
    summoner_name = riot_api.get_summoner(name=summoner_name.replace(' ', '').lower(), region=region)['name']

    # At this point, all user inputted data has been cleaned:
    #   - Region is lowercase.
    #   - Name is lowercase and spaces stripped (standardized).

    # Then we query cache for extant summoner object, since we store formatted summoner names only.
    try:
        summoner = Summoner.objects.filter(region=region).get(name=summoner_name)
        summoner_known = True
        print('cache HIT for summoner search: {str}'.format(str=summoner_name))
    except ObjectDoesNotExist:  # no matching summoner found in DB
        summoner_known = False
        print('cache MISS for summoner search: {str}'.format(str=summoner_name))

    # if we already know about this summoner
    if summoner_known:
        #print u'cache entry age: {age}'.format(age=str(datetime.now() - summoner.last_update))

        # If its cache time hasn't expired...
        if datetime.now() < (summoner.last_update + CACHE_SUMMONER):
            # We don't actually do anything here, since cache is fresh.
            # give the cached info
            print('cache FRESH for summoner: {str}'.format(str=summoner.name))
            #return HttpResponse("%s" % summoner.name)

        # Else the cached summoner object exists, but needs updating.
        else:
            # TODO: Need to do API error checking here
            print('cache STALE for summoner: {str}'.format(str=summoner.name))
            summoner_dto = riot_api.get_summoner(name=summoner_name.replace(' ', '').lower(), region=region)
            print('received summoner dto:', summoner_dto)

            summoner.summoner_id = summoner_dto['id']
            summoner.name = summoner_dto['name']
            summoner.std_name = summoner_dto['name'].replace(' ', '').lower()
            summoner.profile_icon_id = summoner_dto['profileIconId']
            summoner.revision_date = summoner_dto['revisionDate']
            summoner.summoner_level = summoner_dto['summonerLevel']
            summoner.region = region

            print('cache UPDATING entry for: {str}'.format(str=summoner.name))
            summoner.save()

            print('Getting recent matches for', summoner.name, '(' + region + ')')
            get_recent_matches(summoner_id=summoner.summoner_id, region=region)
            print('Getting leagues...')
            get_league_by_summoner_id(summoner_id=summoner.summoner_id, region=region)
            print('Getting teams...')
            get_teams_by_summoner_id(summoner_id=summoner.summoner_id, region=region)

    # We don't have this summoner in the cache, so grab it from API and create new entry.
    else:
        print('querying API for new summoner: {str}'.format(str=summoner_name))
        summoner_dto = riot_api.get_summoner(name=summoner_name.replace(' ', '').lower(), region=region)
        print('API result:', summoner_dto)

        # TODO: Need to do API error checking here
        summoner = Summoner(summoner_id=summoner_dto['id'],
                            name=summoner_dto['name'],
                            std_name=summoner_dto['name'].replace(' ', '').lower(),
                            profile_icon_id=summoner_dto['profileIconId'],
                            revision_date=summoner_dto['revisionDate'],
                            summoner_level=summoner_dto['summonerLevel'],
                            region=region)
        summoner.save()

        print('Getting recent matches for', summoner.name, '(' + region + ')')
        get_recent_matches(summoner_id=summoner.summoner_id, region=region)
        print('Getting leagues...')
        get_league_by_summoner_id(summoner_id=summoner.summoner_id, region=region)
        print('Getting teams...')
        get_teams_by_summoner_id(summoner_id=summoner.summoner_id, region=region)