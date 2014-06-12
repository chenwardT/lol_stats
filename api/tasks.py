from __future__ import absolute_import

from time import sleep
from datetime import datetime

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist

from api.models import Summoner
from api.utils import riot_api, CACHE_SUMMONER

@shared_task
def add(x, y):
    return x + y

@shared_task
def async_get_summoner_by_name(summoner_name, region):
    """
    Get summoner info, by name from Riot API, into cache.

    Returns a Summoner object.
    """
    # first we query cache for extant summoner object
    try:
        summoner = Summoner.objects.filter(region=region).get(name__iexact=summoner_name)
        summoner_known = True
        print u'cache HIT for summoner search: {str}'.format(str=summoner_name)
    except ObjectDoesNotExist:  # no matching summoner found in DB
        summoner_known = False
        print u'cache MISS for summoner search: {str}'.format(str=summoner_name)

    # if we already know about this summoner
    if summoner_known:
        #print u'cache entry age: {age}'.format(age=str(datetime.now() - summoner.last_update))

        # and it's cache time hasn't expired
        if datetime.now() < (summoner.last_update + CACHE_SUMMONER):
            # give the cached info
            print u'cache FRESH for summoner: {str}'.format(str=summoner.name)
            #return HttpResponse("%s" % summoner.name)

        # cached summoner object exists, but needs updating
        else:
            # TODO: Need to do API error checking here
            print u'cache STALE for summoner: {str}'.format(str=summoner.name)
            summoner_dto = riot_api.get_summoner(name=summoner_name.replace(' ',''), region=region)
            print u'received summoner dto:', summoner_dto

            summoner.summoner_id = summoner_dto['id']
            summoner.name = summoner_dto['name']
            summoner.profile_icon_id = summoner_dto['profileIconId']
            summoner.revision_date = summoner_dto['revisionDate']
            summoner.summoner_level = summoner_dto['summonerLevel']
            summoner.region = region
            summoner.last_update = datetime.now()

            print u'cache UPDATING entry for: {str}'.format(str=summoner.name)
            summoner.save()

    # we don't have this summoner in the cache, so grab it from API and create new entry
    else:
        print u'querying API for new summoner: {str}'.format(str=summoner_name)
        summoner_dto = riot_api.get_summoner(name=summoner_name.replace(' ',''), region=region)
        print u'API result:', summoner_dto

        # TODO: Need to do API error checking here
        summoner = Summoner(summoner_id=summoner_dto['id'],
                            name=summoner_dto['name'],
                            profile_icon_id=summoner_dto['profileIconId'],
                            revision_date=summoner_dto['revisionDate'],
                            summoner_level=summoner_dto['summonerLevel'],
                            region=region,
                            last_update=datetime.now())
        summoner.save()

    sleep(5)