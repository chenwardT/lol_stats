from django.db import models

# Create your models here.

class Summoner(models.Model):
    summoner_id = models.IntegerField()
    name = models.CharField(max_length=16)
    profile_icon_id = models.IntegerField()
    revision_date = models.IntegerField()
    summoner_level = models.IntegerField()
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
        return '{str.name}, {str.title} ({str.champion_id})'.format(str=self)

class Item(models.Model):
    item_id = models.IntegerField()
    description = models.CharField(max_length=1024)
    name = models.CharField(max_length=32)
    plain_text = models.CharField(max_length=256, blank=True, null=True)
    group = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return '{str.name} ({str.item_id})'.format(str=self)