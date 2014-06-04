.. lol_stats documentation master file, created by
   sphinx-quickstart on Wed Jun  4 02:34:09 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome! This is the documentation for lol_stats.
=================================================

lol_stats is a website that aims to provide unique insight into the competitive multiplayer game `League of Legends <http://leagueoflegends.com>`_, developed by Riot Games.
Through querying the official `League of Legends API <http://developer.riotgames.com/>`_ it accesses historical match data which can be used to find patterns and make distinctions that may not be apparent to players/spectators of the game.

Background
----------

Currently, this is a educational project whose immediate benefit is familiarizing myself with or furthering knowledge in several topics:

- the website is built on ``Django``, a Python web framework

- programmatic interaction with a rate-limited REST API (devs start with a 10req/10s key, to be upgraded upon application acceptance)

	+ I employ and have been updating a clone of `RiotWatcher <https://github.com/pseudonym117/Riot-Watcher>`_, a thin wrapper for the game's API

		* ``RiotWatcher`` makes use of the ``requests`` library

- asynchronous tasks

	+ waiting on the API response takes time, so async website design is necessary

		* backend work to be achieved via ``Celery``, a distributed task queue

		* frontend async will be implemented as AJAX calls via ``jQuery``

		* HTTP PUSH to be performed via `Nginx HTTP Push Module <https://pushmodule.slact.net/>`_

		* Django model data store is exposed via a RESTful API using ``Django REST Framework``

- caching to prevent unnecessary API requests

	+ currently employing a SQL DB, with an eye towards moving some things to in-memory caches e.g. ``memcached``

Analytical techniques will follow once core site functionality regarding retrieval and storage of data from Riot's official API is solidified.


Contents
========

.. toctree::
   :maxdepth: 2

   lol_stats/modules
   api/modules
   champion/modules
   item/modules
   summoner/modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Source Code
-----------

- Bitbucket: https://bitbucket.org/kreychek/lol_stats


License
-------

	lol_stats is a website that provides data aggregation and analysis
	functionality for Riot Games' League of Legends.
	This project and its author are not affiliated with Riot Games.
	Copyright (C) 2014 Edward Chen

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as
	published by the Free Software Foundation, either version 3 of the
	License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.

	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
