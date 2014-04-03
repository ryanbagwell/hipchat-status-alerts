#! /usr/bin/env python
import memcache
import os
import checks
from config import HipchatConfigParser


class Notify(object):
    cache = None

    def __init__(self):
        self.config = HipchatConfigParser()

        self.config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))
        conf = self.config.as_dict()

        self.defaults = conf.pop('DEFAULTS')

        self.checks = conf

        for name, options in self.checks.items():
            options = dict(self.defaults.items() + options.items())
            options['name'] = name
            cls = getattr(checks, '%sCheck' % options['type'])
            obj = cls(self.get_cache(), options)



    def get_cache(self):

        servers = ['%s:%s' % (self.defaults['memcache_server_address'], self.defaults['memcache_server_port']) ]

        if self.cache:
            return self.cache

        self.cache = memcache.Client(servers)

        return self.cache


n = Notify()
