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

# get 1 or more summoner DTOs from API, put into cache
# max summoners per request is 40
def get_summoner_by_id(summoner_ids, region=NORTH_AMERICA):
    summoners = riot_api.get_summoners(names=None,ids=summoner_ids, region=region)

    num_sums = 0

    for i, e in enumerate(summoners):
        summoner = Summoner()
        summoner.summoner_id=summoners[e]['id']
        summoner.name=summoners[e]['name']
        summoner.profile_icon_id=summoners[e]['profileIconId']
        summoner.revision_date=summoners[e]['revisionDate']
        summoner.summoner_level=summoners[e]['summonerLevel']
        summoner.region=region
        summoner.last_update=datetime.now()
        summoner.save()

        num_sums = i

    print 'Cached {} summoner DTOs'.format(num_sums + 1)  # add 1 b/c 0 indexing

    return num_sums  # return code may be unused, will be > 0 if it got any summoner info though

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

    # can this be more pythonic? why doesn't ex. k['id'] work?
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
def get_recent_matches(summoner_id, region=NORTH_AMERICA):
    recent = riot_api.get_recent_games(summoner_id, region)

    # requires summoners (as well as all related field values) to be cached before-hand
    for match in recent['games']:
        # first fill in the simple stuff
        game = Game(summoner_id=Summoner.objects.get(summoner_id=summoner_id),
                    champion_id=Champion.objects.get(champion_id=match['championId']),
                    create_date=match['createDate'],
                    game_id=match['gameId'],
                    game_mode=match['gameMode'],
                    invalid=match['invalid'],
                    ip_earned=match['ipEarned'],
                    level=match['level'],
                    map_id=match['mapId'],
                    spell_1=SummonerSpell.objects.get(spell_id=match['spell1']),
                    spell_2=SummonerSpell.objects.get(spell_id=match['spell2']),
                    sub_type=match['subType'],
                    team_id=match['teamId'])

        # Here we check if a stat exists (e.g. won't exist if 0), if so, add to RawStat object
        # TODO: use regex to convert JSON attributes (camelCase) to model field names (camel_case)
        # for now, we just get some guaranteed stats
        stats = RawStat(gold=match['stats']['gold'],
                        level=match['stats']['level'],
                        time_played=match['stats']['timePlayed'],
                        win=match['stats']['win'])
        stats.save()

        ## if there were any other plays in this match
        #if 'fellowPlayers' in match:
        #    for p in match['fellowPlayers']:
        #
        #        # get fellow players into cache first, b/c we relate their Summoner objects here
        #        summoner_info(search_str=p[])
        #        player = Player(champion=Champion.objects.get(champion_id=p['championId']),
        #                        summoner=Summoner.objects.get)

# retrieve summoner info from API
def summoner_info_by_id(summoner_id, region=NORTH_AMERICA):
    sum = riot_api.get_summoner(id=summoner_id, region=region)


def recent_games(request, summoner_name, region=NORTH_AMERICA):
    #sum_id = summoner_name_to_id(summoner_name, region)

    summoner = Summoner.objects.filter(name__iexact=summoner_name).get(region__iexact=region)
    games = summoner.game_set.all()

    matches = []

    # create a list (matches) of dicts (stats)
    for g in games:
        stats = {}  # RawStats (ex. penta_kills, damage dealt, etc)
        meta_stats = {}  # Game stats (ex. game mode, ip_earned, etc)
        players = []  # Participating players

        # fill the dicts with the match info
        stats = g.stats.__dict__.copy()
        meta_stats = g.__dict__.copy()

        for i in g.player_set.all():
            players.append(i)

        # insert a dict of the stats into the match list
        #matches.append({'stats': stats, 'meta_stats': meta_stats, 'players': players})
        #matches.append({'stats': g.stats

    print 'Recent matches found for {}: {}'.format(summoner_name, len(matches))

    print 'matches: {}\nsummoner:{}'.format(matches, summoner)

    return render(request, 'match_history.html', {'matches': matches, 'summoner': summoner, 'games': games})