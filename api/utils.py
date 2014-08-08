"""
Utility functions and constants for API module.
"""

from datetime import datetime, timedelta

import inflection
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from lol_stats.base import riot_api
from api.models import (
    Summoner,
    Player,
    RawStat,
    Game,
    Champion,
    Item,
    SummonerSpell,
    League,
    LeagueEntry,
    Team,
    MatchHistorySummary,
    Roster,
    TeamMemberInfo,
    TeamStatDetail)


## Constants ##

# Regions
BRAZIL = 'br'
EUROPE_NORDIC_EAST = 'eune'
EUROPE_WEST = 'euw'
KOREA = 'kr'
LATIN_AMERICA_NORTH = 'lan'
LATIN_AMERICA_SOUTH = 'las'
NORTH_AMERICA = 'na'
OCEANIa = 'oce'
RUSSIA = 'ru'
TURKEY = 'tr'

# Cache Durations
CACHE_SUMMONER = timedelta(seconds=10)  # Sensible value in production would be avg game length?

# Riot API
MAX_IDS = 40  # number of summoner IDs that can be queried at once


def get_summoner_by_name(summoner_name, region):
    """
    Get summoner info, by name, from Riot API, into cache.

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

        # if its cache time hasn't expired
        if datetime.now() < (summoner.last_update + CACHE_SUMMONER):
            # give the cached info
            print u'cache FRESH for summoner: {str}'.format(str=summoner.name)
            #return HttpResponse("%s" % summoner.name)

        # else the cached summoner object exists, but needs updating
        else:
            # TODO: Need to do API error checking here
            print u'cache STALE for summoner: {str}'.format(str=summoner.name)
            summoner_dto = riot_api.get_summoner(name=summoner_name.replace(' ', ''), region=region)
            print u'received summoner dto:', summoner_dto

            summoner.summoner_id = summoner_dto['id']
            summoner.name = summoner_dto['name']
            summoner.std_name = summoner_dto['name'].replace(' ', '').lower()
            summoner.profile_icon_id = summoner_dto['profileIconId']
            summoner.revision_date = summoner_dto['revisionDate']
            summoner.summoner_level = summoner_dto['summonerLevel']
            summoner.region = region

            print u'cache UPDATING entry for: {str}'.format(str=summoner.name)
            summoner.save()

    # we don't have this summoner in the cache, so grab it from API and create new entry
    else:
        print u'querying API for new summoner: {str}'.format(str=summoner_name)
        summoner_dto = riot_api.get_summoner(name=summoner_name.replace(' ', ''), region=region)
        print u'API result:', summoner_dto

        # TODO: Need to do API error checking here
        summoner = Summoner(summoner_id=summoner_dto['id'],
                            name=summoner_dto['name'],
                            std_name=summoner_dto['name'].replace(' ', '').lower(),
                            profile_icon_id=summoner_dto['profileIconId'],
                            revision_date=summoner_dto['revisionDate'],
                            summoner_level=summoner_dto['summonerLevel'],
                            region=region,
                            #last_update=datetime.now()
                            )
        summoner.save()


# TODO: should we ensure this is only called on cached summoners?
# Unused
# def get_summoner_by_id(summoner_ids, region):
#     """
#     Get one or more summoner info objects by ID from Riot API and insert them into DB.
#
#     Max summoners per request is 40 (MAX_ID).
#     """
#     summoners = riot_api.get_summoners(names=None, ids=summoner_ids, region=region)
#
#     num_sums = 0
#
#     for i, e in enumerate(summoners):
#         summoner = Summoner()
#         summoner.summoner_id = summoners[e]['id']
#         summoner.name = summoners[e]['name']
#         summoner.profile_icon_id = summoners[e]['profileIconId']
#         summoner.revision_date = summoners[e]['revisionDate']
#         summoner.summoner_level = summoners[e]['summonerLevel']
#         summoner.region = region
#         #summoner.last_update = datetime.now()
#         summoner.save()
#
#         num_sums = i
#
#     print 'Cached {} summoner DTOs'.format(num_sums + 1)  # add 1 b/c 0 indexing
#
#     return num_sums  # return code may be unused, will be > 0 if it got any summoner info though


def summoner_name_to_id(summoner_name, region):
    """
    Convert summoner name to summoner ID via DB lookup, otherwise query from Riot API.
    """
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
            return 0

    return summoner.summoner_id


def chunks(l, n):
    """
    Yield successive n-sized chunks from l.

    l must be a list.
    """
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def reset_recent():
    """
    Clear all DB objects related to recent match history.

    Debugging function.
    """
    Summoner.objects.all().delete()
    Player.objects.all().delete()
    RawStat.objects.all().delete()
    Game.objects.all().delete()


def update_champions():
    """
    Update the DB table containing champion info from Riot API.
    """
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


def update_items():
    """
    Update the DB table containing item info from Riot API.
    """
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


def update_summoner_spells():
    """
    Update the DB table containing summoner spell info from Riot API.
    """
    spells = riot_api.static_get_summoner_spell_list()
    SummonerSpell.objects.all().delete()

    for k in spells['data']:
        sum_spell = SummonerSpell(spell_id=spells['data'][k]['id'],
                                  summoner_level=spells['data'][k]['summonerLevel'],
                                  name=spells['data'][k]['name'],
                                  key=spells['data'][k]['key'],
                                  description=spells['data'][k]['description'])
        sum_spell.save()


def update_static_data():
    """
    Update the DB with all static data from Riot API.
    """
    update_champions()
    update_items()
    update_summoner_spells()


def get_recent_matches(summoner_id, region):
    """
    Retrieves game data for last 10 games played by a summoner, given a summoner ID and region.
    """

    #print 'get_recent_matches()', summoner_id, region

    recent = riot_api.get_recent_games(summoner_id, region)

    # First make a set of the associated summoner IDs (a set cannot have duplicate entries).
    unique_players = set()
    for g in recent['games']:
        if 'fellowPlayers' in g:
            for p in g['fellowPlayers']:
                unique_players.add(p['summonerId'])

    # Now we take note of any summoner IDs we already have cached (so we can remove them).
    to_remove = set()
    for p in unique_players:
        try:
            Summoner.objects.filter(region=region).get(summoner_id=p)
            to_remove.add(p)
        except ObjectDoesNotExist:
            pass

    # Remove the already cached summoner IDs from the working set.
    for p in to_remove:
        unique_players.remove(p)

    player_list = list(unique_players)  # make a list of the set, so we can call chunks() on it

    # Don't forget, we have to check for the summoner ID whose history we're examining as well!
    try:
        Summoner.objects.filter(region=region).get(summoner_id=summoner_id)
    except ObjectDoesNotExist:  # if it isn't cached, and it isn't in the list yet, add it
        if summoner_id not in player_list:
            player_list.append(summoner_id)

    query_list = list(chunks(player_list, MAX_IDS))  # query_list now holds a list of lists of at most MAX_ID elements

    # Now ask the API for info on summoners, at most MAX_ID at a time.
    #print 'Now asking for participants...'
    summoner_dto = []
    for i in query_list:
        summoner_dto.append(riot_api.get_summoners(ids=i, region=region))

    #print 'Done getting participants!'

    # TODO: This part is sometimes getting duplicate summoners! (fixed?)
    # Now put those summoner DTOs in the cache.
    for chunk in summoner_dto:
        for player in chunk:
            # for v in chunk[player]:
            #     print v, len(v)
            #print u'ADDING summoner {}'.format(chunk[player]['name'])
            summoner = Summoner(summoner_id=chunk[player]['id'],
                                name=chunk[player]['name'],
                                std_name=chunk[player]['name'].replace(' ', '').lower(),
                                profile_icon_id=chunk[player]['profileIconId'],
                                revision_date=chunk[player]['revisionDate'],
                                summoner_level=chunk[player]['summonerLevel'],
                                region=region)

            # Sometimes requests will go out synchronously for the same summoner.
            # This means the cache is not hit and a double query for a single summoner occurs.
            # Duplicate summoners are prevented via the unique_together constraint on summoner_id and region,
            # which will throw IntegrityError and prevent the dupe from being made.
            try:
                #print summoner.name, len(summoner.name)
                summoner.save()
            except IntegrityError:
                pass

    # Requires summoners (as well as all related field values) to be cached before-hand (summoner caching done above).
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
                    region=region,
                    champion_key=Champion.objects.get(champion_id=match['championId']).key)

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
                                    participant_of=game)
                    player.save()
        else:  # if it didn't save, we can get rid of the stats object too.
            stats.delete()


# summoner_ids is expected to be a list of 1 or more summoner IDs
# TODO: add cache lookup, and maybe roll into other summoner lookup(s)
#def summoner_ids_to_name(summoner_ids, search_region):
#    """
#    Convert one or more summoner IDs to summoner name(s).
#    """
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

def standardize_name(str):
    """
    Returns `str` as lowercase with spaces stripped.
    """
    return str.replace(' ', '').lower()


def get_league_by_summoner_id(summoner_id, region):
    """
    Gets league data, given a summoner ID and region, and stores it in the DB.

    Checks for a matching league in the DB and updates that if it exists,
    otherwise creates a new League.
    Matches are made by comparing: region, queue, name, and tier.

    League queries to the Riot API return the following data, with entries for each league that
    the summoner is involved in (ex. solo queue league, ranked team A league, ranked team B league, etc:
    -league name, ex. Orianna's Warlocks
    -league tier, ex. Bronze
    -league queue type, ex. Ranked Team 5v5
    -entries for every member of that league, be them summoners (for solo queue) or teams (for ranked team queue)
    -the participant ID, which is a summoner or team ID, used to locate the belonging entry in its respective league
    -each entry in that league then contains the following:
        -league points
        -flags for fresh blood, veteran, hot streak, inactive
        -player or team name
        -summoner or team ID
        -wins
        -division
    """
    # get_league() returns a dict with the keys being equal to the summoner_ids
    # We only ask for a single summoner's info here, so we only care about the one value.
    league_dto = riot_api.get_league(summoner_ids=[summoner_id], region=region)[str(summoner_id)]
    
    # league_dto is a list with elements for each ladder-team combination
    # ex. Solo Queue, Team A (5x5), Team B (5x5), Team C (3x3), etc
    for i in league_dto:
        league_ele = i

        # Keys of league_dto: tier, queue, participantId, name, entries
    
        # Can we match this data to an League in the DB?
        try:
            matching_league = League.objects.filter(
                region=region).filter(
                queue=league_ele['queue']).filter(
                name=league_ele['name']).get(
                tier=league_ele['tier'])
            matched = True
            print 'Found matching League: {} {} {} {}'.format(matching_league.region, matching_league.queue, matching_league.name, matching_league.tier)

        # We couldn't find a matching League, so we need to create one.
        except ObjectDoesNotExist:
            matched = False
            matching_league = League(region=region, queue=league_ele['queue'], name=league_ele['name'], tier=league_ele['tier'])
            print 'Creating new League: {} {} {} {}'.format(matching_league.region, matching_league.queue, matching_league.name, matching_league.tier)
            matching_league.save()
    
        # Now we handle the entries, which are players (solo queue) or teams (team queue)

        # Since this is an exhaustive list of participants in this league,
        # we replace all entries of this league with the fresh data.
        for j in matching_league.leagueentry_set.all():
            j.delete()

        for k in league_ele['entries']:
            # First we fill in the info we know will exist.
            new_entry = LeagueEntry(division=k['division'],
                                    is_fresh_blood=k['isFreshBlood'],
                                    is_hot_streak=k['isHotStreak'],
                                    is_inactive=k['isInactive'],
                                    is_veteran=k['isVeteran'],
                                    league_points=k['leaguePoints'],
                                    player_or_team_id=k['playerOrTeamId'],
                                    player_or_team_name=k['playerOrTeamName'],
                                    wins=k['wins'])

            # If the entry is in a series:
            if 'miniSeries' in k:
                new_entry.series_losses = k['miniSeries']['losses']
                new_entry.series_progress = k['miniSeries']['progress']
                new_entry.series_target = k['miniSeries']['target']
                new_entry.series_wins = k['miniSeries']['wins']

            new_entry.league = matching_league

            new_entry.save()

def get_teams_by_summoner_id(summoner_id, region):
    """
    Get team data, given a summoner ID and region, and stores it in the DB.

    Each summoner can have 0 or more teams. This checks for matching teams in the DB
    and updates them if they are present, otherwise it creates a new team.
    Matches are made by comparing region and full_id.

    Team queries to the Riot API return the following data, per team:
    -timestamps for roster invites
    -timestamps for roster joins
    -summoner IDs for team roster
    -summoner ID for team owner
    -match summary for each game played
    -summary for overall performance in 5v5 and 3v3
    -team basic data (e.g. tag, name, etc)
    -timestamps for most recent game, team modified, team created
    """
    teams_dto = riot_api.get_teams_for_summoner(summoner_id, region)

    # teams_dto is a list that will contain an entry for each team the summoner is on.

    for team in teams_dto:
        # Can we match this data to a Team in the DB?
        try:
            matching_team = Team.objects.filter(region=region).get(full_id=team['fullId'])
            # We found a match, so set the working Team to that.
            print 'Found matching Team {} {}'.format(matching_team.region, matching_team.name)
            matched = True
            new_team = matching_team
        except ObjectDoesNotExist:
            # No match found, so create a new Team.
            matched = False
            print 'No matching team found. Creating a new Team...'
            new_team = Team()

        # We get all the Team data from Riot API call,
        # so we can delete everything and just create new models below.
        if matched:
            new_team.roster.delete()
            new_team.delete()

        # Set everything in the Team model that isn't a related field.
        new_team.create_date = team['createDate']
        new_team.full_id = team['fullId']
        new_team.last_game_date = team['lastGameDate']
        new_team.last_joined_ranked_team_queue_date = team['lastJoinedRankedTeamQueueDate']
        new_team.modify_date = team['modifyDate']
        new_team.name = team['name']
        new_team.last_join_date = team['lastJoinDate']
        new_team.second_last_join_date = team['secondLastJoinDate']
        new_team.third_last_join_date = team['thirdLastJoinDate']
        new_team.status = team['status']
        new_team.tag = team['tag']
        new_team.region = region

        # This leaves: roster, teamStatDetails, matchHistory.
        roster_dto = team['roster']
        team_stat_details_dto = team['teamStatDetails']
        match_history_dto = team['matchHistory']

        # Setup and save the Roster model.
        new_roster = Roster(owner_id=roster_dto['ownerId'])
        new_roster.save()

        # We can set the roster relation on the Team model now, and save it.
        new_team.roster = new_roster
        new_team.save()

        # Setup and save the TeamMemberInfo models for this Roster.
        for member in roster_dto['memberList']:
            new_member = TeamMemberInfo(invite_date=member['inviteDate'],
                                        join_date=member['joinDate'],
                                        player_id=member['playerId'],
                                        status=member['status'],
                                        roster=new_roster)
            new_member.save()

        # Setup and save the TeamStatDetail models for the Team.
        for stats in team_stat_details_dto:
            new_stats = TeamStatDetail(team_stat_type=stats['teamStatType'],
                                       average_games_played=stats['averageGamesPlayed'],
                                       wins=stats['wins'],
                                       losses=stats['losses'],
                                       team=new_team)
            new_stats.save()

        # Setup and save the MatchHistorySummary models for the Team.
        for match in match_history_dto:
            new_match = MatchHistorySummary(assists=match['assists'],
                                            date=match['date'],
                                            deaths=match['deaths'],
                                            game_id=match['gameId'],
                                            game_mode=match['gameMode'],
                                            invalid=match['invalid'],
                                            kills=match['kills'],
                                            map_id=match['mapId'],
                                            opposing_team_kills=match['opposingTeamKills'],
                                            opposing_team_name=match['opposingTeamName'],
                                            win=match['win'],
                                            team=new_team)
            new_match.save()

def reset_teams():
    """
    Clear all Team objects and children from DB.
    """
    # We (have to?) delete Roster separately because it is a one-to-one field related to by Team.
    Roster.objects.all().delete()
    # All of the Team child models are related to by the children to Team.
    Team.objects.all().delete()

def reset_leagues():
    """
    Clear all League objects and children from DB.
    """
    League.objects.all().delete()