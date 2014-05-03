# Lol_stats
Lol_stats is a website that aims to provide unique insight into the competitive multiplayer game "League of Legends", developed by Riot Games.
Through querying the official League of Legends API (http://developer.riotgames.com/) it accesses historical match data which can be used to find patterns and make distinctions that may not be apparent to players/spectators of the game.

## Developmental State
Currently, this is a educational project whose immediate benefit is familiarizing myself with several topics of personal interest:

- the website is built on Django, a Python web framework

- programmatic interaction with a rate-limited REST API (devs start with a 10req/10s key, to be upgraded upon application acceptance)

    + I employ `RiotWatcher`, a thin wrapper for the game's API (I have been performing incremental updates to keep up with Riot's API versioning)

        * `RiotWatcher` makes use of the `requests` library

- asynchronous tasks

    + waiting on the API response takes time, so async website design is necessary

        * backend work to be achieved via Celery distributed task queue

        * frontend async will be implemented as AJAX calls via jQuery

- caching to prevent unnecessary API requests

    + currently employing a SQL DB, with an eye towards moving some things to in-memory caches ex. memcached

Before I get to work into any analysis techniques, the plan is to first mimic the functionality of popular LoL websites such as http://www.lolking.net.

This project and its author are not affiliated with Riot Games.