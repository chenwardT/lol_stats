import pprint
from datetime import datetime, timedelta

import inflection
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.core import serializers

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
CACHE_SUMMONER = timedelta(seconds=10)  # will be longer in production

# yield successive n-sized chunks from l
# l must be a list
def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

# debug: clear all DB objects related to recent match history
def reset_recent():
    Summoner.objects.all().delete()
    Player.objects.all().delete()
    RawStat.objects.all().delete()
    Game.objects.all().delete()

# get summoner info, by name, from Riot API, into cache
def get_summoner_by_name(summoner_name, region):
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
        print u'cache entry age: {age}'.format(age=str(datetime.now() - summoner.last_update))

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

            summoner.summoner_id=summoner_dto['id']
            summoner.name=summoner_dto['name']
            summoner.profile_icon_id=summoner_dto['profileIconId']
            summoner.revision_date=summoner_dto['revisionDate']
            summoner.summoner_level=summoner_dto['summonerLevel']
            summoner.region=region
            summoner.last_update=datetime.now()

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

    return summoner

# view to display summoner info given name, region
def summoner_info(request, summoner_name, region=NORTH_AMERICA):
    summoner = get_summoner_by_name(summoner_name, region)

    return render(request, 'summoner_info.html', {'summoner': summoner})

# get 1 or more summoner DTOs from API, put into cache
# max summoners per request is 40
def get_summoner_by_id(summoner_ids, region=NORTH_AMERICA):
    summoners = riot_api.get_summoners(names=None, ids=summoner_ids, region=region)

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

# convert summoner name to summoner ID via cache lookup, otherwise API call
# TODO: should we ensure this is only called on cached summoners?
def summoner_name_to_id(summoner_name, region=NORTH_AMERICA):
    try:
        summoner = Summoner.objects.filter(region=region).get(name__iexact=summoner_name)
        print 'cache match FOUND for {str}'.format(str=summoner_name)
    except ObjectDoesNotExist:
        print 'cache match NOT FOUND for {str}'.format(str=summoner_name)

        print 'querying API for summoner by name: {}'.format(summoner_name)
        get_summoner_by_name(summoner_name=summoner_name, region=region)

        print 'retrying cache with new data...'
        try:
            summoner = Summoner.objects.filter(region=region).get(name__iexact=summoner_name)
            print 'retried cache match FOUND for {str}'.format(str=summoner_name)
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
# TODO: check DB for
def get_recent_matches(summoner_id, region=NORTH_AMERICA):
    MAX_IDS = 40  # number of summoner IDs that can be fed to get_summoners()
    recent = riot_api.get_recent_games(summoner_id, region)

    # first make a set of the associated summoner IDs (a set cannot have duplicate entries)
    unique_players = set()
    for g in recent['games']:
        for p in g['fellowPlayers']:
            unique_players.add(p['summonerId'])

    # now we take note of any summoner IDs we already have cached (so we can remove them)
    to_remove = set()
    for p in unique_players:
        try:
            Summoner.objects.filter(region=region).get(summoner_id=p)
            to_remove.add(p)
            #print u'Will REMOVE {} from unique_players'.format(Summoner.objects.filter(region=region).get(summoner_id=p))
        except ObjectDoesNotExist:
            pass
            #print 'Will retrieve new summoner info ({})'.format(p)

    # remove the already cached summoner IDs from the working set
    for p in to_remove:
        unique_players.remove(p)

    player_list = list(unique_players)  # make a list of the set, so we can call chunks() on it

    #pprint.pprint(sorted(player_list))

    # don't forget, we have to check for the summoner ID whose history we're examining as well!
    try:
        Summoner.objects.filter(region=region).get(summoner_id=summoner_id)
    except ObjectDoesNotExist:  # if it isn't cached, and it isn't in the list yet, add it
        if summoner_id not in player_list:
            player_list.append(summoner_id)

    # WE ALREADY DID THIS WTF
    # remove summonerIDs that we already have in the cache
    #for i in player_list:
    #    if len(Summoner.objects.filter(region=region).filter(summoner_id=i)):
    #        player_list.remove(i)

    query_list = list(chunks(player_list, MAX_IDS))  # query_list now holds a list of lists of at most MAX_ID elements

    # now ask the API for info on summoners, at most MAX_ID at a time
    summoner_dto = []
    for i in query_list:
        summoner_dto.append(riot_api.get_summoners(ids=i))

    #pprint.pprint(summoner_dto)

    # TODO: This part is sometimes getting duplicate summoners!
    # now put those summoner DTOs in the cache
    for chunk in summoner_dto:
        for player in chunk:
            #print u'ADDING summoner {}'.format(chunk[player]['name'])
            summoner = Summoner(summoner_id=chunk[player]['id'],
                                name=chunk[player]['name'],
                                profile_icon_id=chunk[player]['profileIconId'],
                                revision_date=chunk[player]['revisionDate'],
                                summoner_level=chunk[player]['summonerLevel'],
                                region=region,
                                last_update=datetime.now())

            # Sometimes requests will go out synchronously for the same summoner.
            # This means the cache is not hit and a double query for a single summoner occurs.
            # Duplicate summoners are prevented via the unique_together constraint on summoner_id and region,
            # which will throw IntegrityError and prevent the dupe from being made.
            try:
                summoner.save()
            except IntegrityError:
                pass

    # requires summoners (as well as all related field values) to be cached before-hand (summoner caching done above)
    for match in recent['games']:
        # first fill in the simple stuff
        game = Game(summoner_id=Summoner.objects.filter(region=region).get(summoner_id=summoner_id),
                    champion_id=Champion.objects.get(champion_id=match['championId']),
                    create_date=match['createDate'],
                    game_id=match['gameId'],
                    game_mode=match['gameMode'],
                    game_type=match['gameType'],
                    invalid=match['invalid'],
                    ip_earned=match['ipEarned'],
                    level=match['level'],
                    map_id=match['mapId'],
                    spell_1=SummonerSpell.objects.get(spell_id=match['spell1']),
                    spell_2=SummonerSpell.objects.get(spell_id=match['spell2']),
                    sub_type=match['subType'],
                    team_id=match['teamId'],
                    region=region)

        stats = RawStat()

        # Here we add stats that were returned (only stats that aren't None or 0 will be returned by API)
        for i in match['stats']:
            setattr(stats, inflection.underscore(i), match['stats'][i])

        stats.save()

        # associate the RawStat object with this game
        game.stats = stats

        game_saved = False

        # Ensures no dupes of Game (or any related objects).
        try:
            game.save()
            game_saved = True
        except IntegrityError:
            pass

        # if game saved, we're good and just need to add the participating players
        if game_saved:
            # associate each Player object with this game
            if 'fellowPlayers' in match:
                for p in match['fellowPlayers']:
                    player = Player(champion=Champion.objects.get(champion_id=p['championId']),
                                    summoner=Summoner.objects.filter(region=region).get(summoner_id=p['summonerId']),
                                    team_id=p['teamId'],
                                    participant=game)
                    player.save()
        else:  # if it didn't save, we can get rid of the stats object too.
            stats.delete()

def recent_games(request, summoner_name, region=NORTH_AMERICA):
    #sum_id = summoner_name_to_id(summoner_name, region)

    get_recent_matches(summoner_name_to_id(summoner_name, region), region)
    summoner = Summoner.objects.filter(name__iexact=summoner_name).get(region__iexact=region)
    games = summoner.game_set.all()

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

    print 'Recent matches found for {}: {}'.format(summoner_name, len(games))
    #print 'matches: {}\nsummoner:{}'.format(matches, summoner)

    return render(request, 'match_history.html', {'summoner': summoner, 'games': games})

def async_summoner_info(request):

    return render(request, 'async_summoner_info.html')

def ajax_summoner_info(request):

    #print 'AJAX summoner id: {}'.format(summoner_id)
    #print request

    print 'AJAX summoner id: {}'.format(request.POST.get('summoner_id'))

    #if request.is_ajax():
    try:
        response_data = serializers.serialize('json', Summoner.objects.filter(summoner_id=request.POST.get('summoner_id')))
    except:
        print 'Summoner ID {} not cached!'.format(request.POST.get('summoner_id'))

    return HttpResponse(response_data, content_type='application/json')