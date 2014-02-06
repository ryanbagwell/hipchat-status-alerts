github-status-notifications
===========================

A simple Python script that sends a Hipchat message upon status changes

Installation
------------

Create a virtual environment, and install dependencies with pip::

    pip install -r requirements.txt

Configuration
-------------

Create a config.ini file in the project directory (a sample config.ini file is provided).

Available options::

    [HIPCHAT]
    API_TOKEN = 008c5926ca861023c1d2a36653fd88e2
    ROOM_ID = YOUR FAVORITE ROOM
    MESSAGE_FROM = Github
    NOTIFY = 1

    [MEMCACHE]
    SERVER_ADDRESS = 127.0.0.1
    SERVER_PORT = 11211
    CACHE_PREFIX = GITHUB_STATUS_NOTIFIER

Usage
-----

Set a cron job to call notify.py every so often. This will call the script every minute::

    * * * * * source /path/to/virtualenv/bin/activate && /path/to/notifier/notify/notify.py

Changes in Github status messages will be sent to the Hipchat room specified in your config file.