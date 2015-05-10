# lol_stats
lol_stats is a website that aims to provide unique insight into the competitive multiplayer game [League of Legends](http://leagueoflegends.com), developed by Riot Games.
Through querying the official [League of Legends API](http://developer.riotgames.com/) it accesses historical match data which can be used to find patterns and make distinctions that may not be apparent to players/spectators of the game.

The associated [front-end](https://github.com/chenwardT/lol_stats-frontend), an AngularJS app that consumes the REST API this project exposes.

*Note: lol_stats is being completely rewritten as a separate project. This is due to significant changes in how Riot's data is represented and accessed, changes to libraries that were in use since last devoting serious effort to the project, and the desire to improve numerous aspects of my design.*

## Background

The site is built on `Django`, a Python web framework and pulls data from Riot Game's League of Legends REST API.

`RiotWatcher`, a thin wrapper for the Riot's API, depends on the `requests` library.

`Celery`, a distributed task queue, is used to wait on remote API responses.
        
Our stored data is exposed via `Django-Rest-Framework`.

A separate `AngularJS` SPA consumes our exposed data to produce the user-facing pages.

Analytical techniques to follow once functionality regarding retrieval, storage, and processing of data is solidified.

This project and its author are not affiliated with Riot Games.

## Documentation
Sphinx-generated docs written to [lol-stats.readthedocs.org](http://lol-stats.readthedocs.org) on pushes. Sometimes changes to code cause the autogen to fail; don't expect much yet.

## Setup
 
Vagrantfile + Cheffile forthcoming...

Root project name being the same as project settings dir ("lol_stats") has been known to cause problems.

###Environment Variables

The following env vars must be present:

`DJANGO_SECRET_KEY` - Django's secret key, used for various cyptographic functions

`RIOT_API_KEY` - your API key to access Riot's REST service

`LOL_STATS_DB_PASSWORD` - the password to the SQL DB


###Postgresql

Django is using `psycopg2` implementation of postgresql DB engine.
This package depends on `libpq-dev` and `python-dev`:
 
`apt-get install libpq-dev python-dev`

Port forwarding to VM's pgsql server is setup via this line in vagrantfile:

`config.vm.network :forwarded_port, guest: 5432, host: 5433`

When configuring VM's postgresql server, must edit postgresql.conf:

`listen_addresses = '*'      # Ensure we listen on all interfaces`

In pg_hba.conf, add a line:

`host    all     all     all     md5     # Accept connections from anywhere, using password auth`

###Celery

Celery is configured to use RabbitMQ's AMQP server:

`apt-get install rabbitmq-server`

## Notes
Python setup files (e.g., requirements.txt, MANIFEST.in, etc) should not be relied upon and are only included for readthedoc's virtualenv.

If you get Unauthorized (401) response codes from riotwatcher calls, ensure it's been updated (per call!) to match current Riot API version.

This product is not endorsed, certified or otherwise approved in any way by Riot Games, Inc. or any of its affiliates.
