# lol_stats
lol_stats is a website that aims to provide unique insight into the competitive multiplayer game [League of Legends](http://leagueoflegends.com), developed by Riot Games.
Through querying the official [League of Legends API](http://developer.riotgames.com/) it accesses historical match data which can be used to find patterns and make distinctions that may not be apparent to players/spectators of the game.

## Background
Currently, this is a educational project whose immediate benefit is familiarizing myself with or furthering knowledge in several topics:

- the website is built on `Django`, a Python web framework

- programmatic interaction with a rate-limited REST API (devs start with a 10req/10s key, to be upgraded upon application acceptance)

    + I employ and have been updating `RiotWatcher`, a thin wrapper for the game's API

        * `RiotWatcher` makes use of the `requests` library

- asynchronous tasks

    + waiting on the API response takes time, so async website design is necessary

        * backend work to be achieved via `Celery`, a distributed task queue

        * frontend async will be implemented as AJAX calls via `jQuery`

        * HTTP PUSH to be performed via [`Nginx` HTTP Push Module](https://pushmodule.slact.net/)
		
		* Django model data store is exposed via a RESTful API using `Django REST Framework`

- caching to prevent unnecessary API requests

    + currently employing a SQL DB, with an eye towards moving some things to in-memory caches e.g. `memcached`

Analytical techniques will follow once core site functionality regarding retrieval and storage of data from Riot's official API is solidified.

This project and its author are not affiliated with Riot Games.

## Documentation
Sphinx-generated docs written to [lol-stats.readthedocs.org](http://lol-stats.readthedocs.org) on pushes. Sometimes changes to code cause the autogen to fail; don't expect much yet.

## Notes
Python setup files (e.g., requirements.txt, MANIFEST.in, etc) should not be relied upon and are only included for readthedoc's virtualenv.