from django.db import models

# Create your models here.

class Summoner(models.Model):
    summoner_id = models.BigIntegerField()
    name = models.CharField(max_length=16)
    profile_icon_id = models.IntegerField()
    revision_date = models.BigIntegerField()
    summoner_level = models.IntegerField()  # 'long' in DTO, but we know it's <= 30
    region = models.CharField(max_length=4)
    last_update = models.DateTimeField()

    def __str__(self):
        return '{str.name} ({str.summoner_id})'.format(str=self)

class Champion(models.Model):
    champion_id = models.IntegerField()
    title = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    key = models.CharField(max_length=32)

    def __str__(self):
        return '{str.name} ({str.champion_id})'.format(str=self)

class Item(models.Model):
    item_id = models.IntegerField()
    description = models.CharField(max_length=1024)
    name = models.CharField(max_length=32)
    plain_text = models.CharField(max_length=256, blank=True, null=True)
    group = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return '{str.name} ({str.item_id})'.format(str=self)

class SummonerSpell(models.Model):
    spell_id = models.IntegerField()
    summoner_level = models.IntegerField()
    name = models.CharField(max_length=16)
    key = models.CharField(max_length=32)
    description = models.CharField(max_length=256)

    def __str__(self):
        return '{str.name} ({str.spell_id})'.format(str=self)

# placeholder
class Mastery(models.Model):
    pass

# placeholder
class Rune(models.Model):
    pass

# placeholder
class Realm(models.Model):
    pass

#
# Following 3 hold recent matches data (see RecentGamesDto on API ref)
#

class Player(models.Model):
    champion_id = models.ForeignKey(Champion)
    summoner_id = models.ForeignKey(Summoner)
    team_id = models.IntegerField()  # 100, 200
    participant = models.ForeignKey(Game)

class RawStat(models.Model):
    assists = models.IntegerField()
    barracks_killed = models.IntegerField()
    champions_killed = models.IntegerField()
    combat_player_score = models.IntegerField()
    consumables_purchased = models.IntegerField()
    damage_dealt_player = models.IntegerField()
    double_kills = models.IntegerField()
    first_blood = models.IntegerField()
    gold = models.IntegerField()
    gold_earned = models.IntegerField()
    gold_spent = models.IntegerField()
    item0 = models.IntegerField()
    item1 = models.IntegerField()
    item2 = models.IntegerField()
    item3 = models.IntegerField()
    item4 = models.IntegerField()
    item5 = models.IntegerField()
    item6 = models.IntegerField()
    items_purchased = models.IntegerField()
    killing_sprees = models.IntegerField()
    largest_critical_strike = models.IntegerField()
    largest_killing_spree = models.IntegerField()
    largest_multi_kill = models.IntegerField()
    legendary_items_created = models.IntegerField()  # Number of tier 3 items built.
    level = models.IntegerField()
    magic_damage_dealt_player = models.IntegerField()
    magic_damage_dealt_to_champions = models.IntegerField()
    magic_damage_taken = models.IntegerField()
    minions_denied = models.IntegerField()
    minions_killed = models.IntegerField()
    neutral_minions_killed = models.IntegerField()
    neutral_minions_killed_enemy_jungle = models.IntegerField()
    neutral_minions_killed_your_jungle = models.IntegerField()
    nexus_killed = models.BooleanField()  # Flag specifying if the summoner got the killing blow on the nexus.
    node_capture = models.IntegerField()
    node_capture_assist = models.IntegerField()
    node_neutralize = models.IntegerField()
    node_neutralize_assist = models.IntegerField()
    num_deaths = models.IntegerField()
    num_items_bought = models.IntegerField()
    objective_player_score = models.IntegerField()
    penta_kills = models.IntegerField()
    physical_damage_dealt_player = models.IntegerField()
    physical_damage_dealt_to_champions = models.IntegerField()
    physical_damage_taken = models.IntegerField()
    quadra_kills = models.IntegerField()
    sight_wards_bought = models.IntegerField()
    spell_1_cast = models.IntegerField()  # Number of times first champion spell was cast.
    spell_2_cast = models.IntegerField()  # Number of times second champion spell was cast.
    spell_3_cast = models.IntegerField()  # Number of times third champion spell was cast.
    spell_4_cast = models.IntegerField()  # Number of times fourth champion spell was cast.
    summon_spell_1_cast = models.IntegerField()
    summon_spell_2_cast = models.IntegerField()
    super_monster_killed = models.IntegerField()
    team = models.IntegerField()
    team_objective = models.IntegerField()
    time_played = models.IntegerField()
    total_damage_dealt = models.IntegerField()
    total_damage_dealt_to_champions = models.IntegerField()
    total_damage_taken = models.IntegerField()
    total_heal = models.IntegerField()
    total_player_score = models.IntegerField()
    total_score_rank = models.IntegerField()
    total_time_crowd_control_dealt = models.IntegerField()
    total_units_healed = models.IntegerField()
    triple_kills = models.IntegerField()
    true_damage_dealt_player = models.IntegerField()
    true_damage_dealt_to_champions = models.IntegerField()
    true_damage_taken = models.IntegerField()
    turrets_killed = models.IntegerField()
    unreal_kills = models.IntegerField()
    victory_point_total = models.IntegerField()
    vision_wards_bought = models.IntegerField()
    ward_killed = models.IntegerField()
    ward_placed = models.IntegerField()
    win = models.BooleanField()  # Flag specifying whether or not this game was won.

# FellowPlayer instances point to this to allow reverse-querying of participants
class Game(models.Model):
    champion_id = models.IntegerField()
    create_date = models.BigIntegerField()
    game_id = models.BigIntegerField()
    game_mode = models.CharField(max_length=16)
    game_type = models.CharField(max_length=16)
    invalid = models.BooleanField()
    ip_earned = models.IntegerField()
    level = models.IntegerField()
    map_id = models.IntegerField()
    spell_1 = models.IntegerField()
    spell_2 = models.IntegerField()
    stats = models.OneToOneField(RawStat)
    sub_type = models.CharField(max_length=24)
    team_id = models.IntegerField()