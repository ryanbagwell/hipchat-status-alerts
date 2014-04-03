hipchat-status-alerts
===========================

A simple Python script that sends a Hipchat message upon status changes

Installation
------------

Create a virtual environment, and install dependencies with pip::

    pip install -r requirements.txt

Configuration
-------------

Create a config.ini file in the project directory (a sample config.ini file is provided).

Default options::

    [DEFAULTS]
    HIPCHAT_API_TOKEN = 008c5926ca861023c1d2a36653fd88e2
    HIPCHAT_ROOM_ID = YOUR FAVORITE ROOM
    HIPCHAT_NOTIFY = 1
    MEMCACHE_SERVER_ADDRESS = 127.0.0.1
    MEMCACHESERVER_PORT = 11211
    MEMCACHE_CACHE_PREFIX = GITHUB_STATUS_NOTIFIER

Then add the sites and services you want to check::

    [Github]
    MESSAGE_FROM = Github
    TIMEOUT = 10
    TYPE = Github

    [Google]
    HIPCHAT_MESSAGE_FROM = Google
    TYPE = HTTP
    URL = http://www.google.com

Any service-specific options will override the default options.

Currently, only two types of service checks are available: Github and HTTP


Usage
-----

Set a cron job to call notify.py every so often. This will call the script every minute::

    * * * * * source /path/to/virtualenv/bin/activate && /path/to/notifier/notify/notify.py

Changes in status messages will be sent to the Hipchat room specified in your config file.