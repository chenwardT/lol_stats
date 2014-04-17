import json
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from web.settings import riot_api
from api.models import *

##Constants

# Regions
NORTH_AMERICA = 'na'
EUROPE_WEST = 'euw'
EUROPE_NORDIC_EAST = 'eune'
BRAZIL = 'br'
LATIN_AMERICA_NORTH = 'lan'
LATIN_AMERICA_SOUTH = 'las'
KOREA = 'kr'

# Cache Duration
CACHE_SUMMONER = timedelta(seconds=10)

# testing stuff
def about(request):
    me = riot_api.get_summoner(name='ronfar')

    my_ranked_stats = riot_api.get_ranked_stats(me['id'])

    #return HttpResponse("%s" % json.dumps(my_ranked_stats, indent=5, sort_keys=True))
    #return HttpResponse("%s" % my_ranked_stats)
    champs = riot_api.static_get_champion_list()
    return HttpResponse("%s" % json.dumps(my_ranked_stats, indent=3))

# get summoner info from summoner name
def summoner_info(request, search_str, render_page=True):
    # placeholders for user input
    if not search_str:
        search_str = 'ronfar'
    search_region = NORTH_AMERICA

    # query DB (cache) for summoner info
    try:
        summoner = Summoner.objects.filter(region=search_region).get(name__iexact=search_str)
        summoner_known = True
        print 'cache HIT for summoner search: {str}'.format(str=search_str)
    except ObjectDoesNotExist:  # no matching summoner found in DB
        summoner_known = False
        print 'cache MISS for summoner search: {str}'.format(str=search_str)

    # if we already know about this summoner
    if summoner_known:
        print 'cache entry age: {age}'.format(age=str(datetime.now() - summoner.last_update))

        # and it's cache time hasn't expired
        if datetime.now() < (summoner.last_update + CACHE_SUMMONER):
            # give the cached info
            print 'cache FRESH for summoner: {str}'.format(str=summoner.name)
            #return HttpResponse("%s" % summoner.name)

        # cached summoner exists, but needs updating
        else:
            # TODO: Need to do API error checking here
            print 'cache STALE for summoner: {str}'.format(str=summoner.name)
            summoner_dto = riot_api.get_summoner(name=search_str.replace(' ',''), region=search_region)
            print 'received summoner dto:', summoner_dto

            summoner.summoner_id=summoner_dto['id']
            summoner.name=summoner_dto['name']
            summoner.profile_icon_id=summoner_dto['profileIconId']
            summoner.revision_date=summoner_dto['revisionDate']
            summoner.summoner_level=summoner_dto['summonerLevel']
            summoner.region=search_region
            summoner.last_update=datetime.now()

            print 'cache UPDATING entry for: {str}'.format(str=summoner.name)
            summoner.save()

    # we don't have this summoner in the cache, so grab it from API and create new entry
    else:
        print 'querying API for new summoner: {str}'.format(str=search_str)
        summoner_dto = riot_api.get_summoner(name=search_str.replace(' ',''), region=search_region)
        print 'API result:', summoner_dto

        # TODO: Need to do API error checking here
        summoner = Summoner(summoner_id=summoner_dto['id'],
                                name=summoner_dto['name'],
                                profile_icon_id=summoner_dto['profileIconId'],
                                revision_date=summoner_dto['revisionDate'],
                                summoner_level=summoner_dto['summonerLevel'],
                                region=search_region,
                                last_update=datetime.now())
        summoner.save()

    if render_page:
        return render(request, 'summoner_info.html', {'summoner': summoner})
    else:
        return

def champion_list(request):
    champs = riot_api.static_get_champion_list()

    return HttpResponse("%s" % json.dumps(champs, indent=3))

# convert summoner name to summoner ID via cache lookup, otherwise API call
def summoner_name_to_id(summoner_name, region):
    try:
        summoner = Summoner.objects.filter(region=region).get(name__iexact=summoner_name)
        print 'cache match FOUND for {str}'.format(str=summoner_name)
    except ObjectDoesNotExist:
        print 'cache match NOT FOUND for {str}'.format(str=summoner_name)
        print 'querying API...'
        summoner_info(request=None, search_str=summoner_name, render_page=False)
        print 'retrying cache with new data...'
        try:
            summoner = Summoner.objects.filter(region=region).get(name__iexact=summoner_name)
            print 'cache match FOUND for {str}'.format(str=summoner_name)
        except ObjectDoesNotExist:
            print 'no summoner found, even after querying API!'

    return summoner.summoner_id

## convert 1 or more summoner IDs to their summoner name(s)
## summoner_ids is expected to be a list of 1 or more summoner IDs
#  ON HOLD FOR NOW
#  TODO: add cache lookup, and maybe roll into other summoner lookup(s)
#def summoner_ids_to_name(summoner_ids, search_region):
#    summoners = riot_api.get_summoners(ids=summoner_ids, region=search_region)
#
#    for summoner_dto in summoners:
#        sum = Summoner(summoner_id=summoner_dto['id'],
#                            name=summoner_dto['name'],
#                            profile_icon_id=summoner_dto['profileIconId'],
#                            revision_date=summoner_dto['revisionDate'],
#                            summoner_level=summoner_dto['summonerLevel'],
#                            region=search_region,
#                            last_update=datetime.now())
#        sum.save()

# update the cache's list of champions and associated IDs from API
# TODO: handle versions
def update_champions():
    # get fresh champ list from API
    champs = riot_api.static_get_champion_list()

    # delete all champ data in cache
    Champion.objects.all().delete()

    # can this be more pythonic?
    for k in champs['data']:
        champ = Champion(champion_id=champs['data'][k]['id'],
                         title=champs['data'][k]['title'],
                         name=champs['data'][k]['name'],
                         key=champs['data'][k]['key'])
        champ.save()
    return

# TODO: handle version and optional fields
def update_items():
    items = riot_api.static_get_item_list()
    Item.objects.all().delete()

    for k in items['data']:
        # plaintext and group are not present for every item
        if 'plaintext' in items['data'][k]:
            plain_text = items['data'][k]['plaintext']
        else:
            plain_text = None

        if 'group' in items['data'][k]:
            group = items['data'][k]['group']
        else:
            group = None

        item = Item(item_id=items['data'][k]['id'],
                    description=items['data'][k]['description'],
                    name=items['data'][k]['name'],
                    plain_text=plain_text,
                    group=group)
        item.save()

# TODO: handle version and optional fields
def update_summoner_spells():
    spells = riot_api.static_get_summoner_spell_list()
    SummonerSpell.objects.all().delete()

    for k in spells['data']:
        sum_spell = SummonerSpell(spell_id=spells['data'][k]['id'],
                                  summoner_level=spells['data'][k]['summonerLevel'],
                                  name=spells['data'][k]['name'],
                                  key=spells['data'][k]['key'],
                                  description=spells['data'][k]['description'])
        sum_spell.save()

# get match history of last 10 games, given a summoner ID
# TODO: use regex to convert JSON attributes (camelCase) to model field names (camel_case)
#def get_recent_matches(summoner_id):
#    recent = riot_api.get_recent_games(summoner_id)
#
#    for match in recent['games']:
#        players
#        game = Game(champion_id=match['championId'],
#                    create_date=match['createDate'],
#                    )

def recent_games(request, summoner_name, region):
    sum_id = summoner_name_to_id(summoner_name, region)

    summoner = Summoner.objects.filter(name__iexact=summoner_name).get(region__iexact=region)
    games = summoner.game_set.all()

    matches = ()
    stats = {}  # RawStats (ex. penta_kills, damage dealt, etc)
    meta_stats = ()  # Game stats (ex. game mode, ip_earned, etc)

    # create a list (matches) of dicts (stats)
    for g in games:
        # first fill the dict with a match's stats
        stats = g.stats.__dict__.copy()
        meta_stats = g.__dict__.copy()