#! /usr/bin/env python

import memcache
import requests
import hipchat
import configparser
import os




class Notify(object):

    ALERT_COLORS = {
        'good': 'green',
        'minor': 'yello',
        'major': 'red',
    }

    def __init__(self):
        self.config = configparser.ConfigParser()

        self.config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

        self.memcache_options = self.config['MEMCACHE']

        self.hipchat_options = self.config['HIPCHAT']

        self.message_key = str("%s_last_message" % self.memcache_options.get('CACHE_PREFIX', 'GITHUB_STATUS_NOTIFIER'))

        self.cache = self._get_cache()


    def notify(self):

        """ Get the hipchat options """
        options = self.config['HIPCHAT']

        """ Get the latest status message """
        r = requests.get('https://status.github.com/api/last-message.json')

        """ Get the previously saved message """
        last_message = self.cache.get(self.message_key)

        """ Save the latest message to memory """
        self.cache.set(self.message_key, r.json())

        """ If we don't have a value for the last message,
            or if the message hasn't changed, stop here """
        if last_message is None or last_message == r.json(): return

        """ Now send a notification """
        hipster = hipchat.HipChat(token=self.hipchat_options.get('API_TOKEN'))

        parameters = {
            'room_id': self.hipchat_options.get('ROOM_ID'),
            'from': self.hipchat_options.get('MESSAGE_FROM', 'Github'),
            'message': r.json()['body'],
            'color': self.ALERT_COLORS[r.json()['status']],
            'notify': self.hipchat_options.get('NOTIFY', '0'),
        }

        hipster.method('rooms/message', method='POST', parameters=parameters)


    def _get_cache(self):

        servers = ['%s:%s' % (self.memcache_options.get('SERVER_ADDRESS'), self.memcache_options.get('SERVER_PORT')) ]

        return memcache.Client(servers)




n = Notify()
n.notify()











