import requests
import hipchat
from requests.exceptions import Timeout, ConnectionError
import sys

class Check(object):
    """ A base class for a status check """

    message_from = 'Hipchat Alerts'

    timeout = 10

    @property
    def message_key(self):
        return str("HIPCHAT_STATUS_NOTIFICATIONS_%s" % self.name)

    def __init__(self, cache=None, options={}):

        self.cache = cache

        for k, v in options.items():
            setattr(self, k, v)

        self.log('Initializing status check for %s' % self.name)

        """ Get the latest status """
        current_status, color = self.check_status()

        """ Get the previously saved message """
        last_message = self.cache.get(self.message_key)

        """ Save the latest message to memory """
        self.cache.set(self.message_key, current_status)

        """ If we don't have a value for the last message,
            or if the message hasn't changed, stop here """
        if last_message is None or last_message == current_status:
            return

        self.notify(current_status, color)

    def check_status(self):
        """ The logic to check the status. Must return a
            tuple consisting of the message and the color """
	
        self.log('Getting the current status of %s' % self.name)

    def notify(self, message, color='green'):

        hipster = hipchat.HipChat(token=self.hipchat_api_token)

        parameters = {
            'room_id': self.hipchat_room_id,
            'from': self.hipchat_message_from,
            'message': message,
            'color': color,
            'notify': self.hipchat_notify,
        }

        hipster.method('rooms/message', method='POST', parameters=parameters)

    def log(self, message):
        
        if '--debug' not in sys.argv:
            return

        print message 


class GithubCheck(Check):
    """ Checks the latest Github status """

    """ A map of Github status codes to colors """

    ALERT_COLORS = {
        'good': 'green',
        'minor': 'yellow',
        'major': 'red',
    }

    def check_status(self):
        super(GithubCheck, self).check_status()

        """ Get the latest status message """
        r = requests.get('https://status.github.com/api/last-message.json')

        status = r.json()

        self.log('Current status of %s: %s' % (self.name, status))

        return status['body'], self.ALERT_COLORS[status['status']]


class HTTPCheck(Check):
    """ Checks an http connection """

    """ A list of valid response codes """
    valid_responses = [200]

    """ The url to check """
    url = None

    def check_status(self):

        """ Make a request and get the response """

        color = 'green'

        try:

            r = requests.get(self.url, timeout=int(self.timeout))

            r.status_code

            if r.status_code in self.valid_responses:
                color = 'green'
            elif r.status_code in [404, 500]:
                color = 'red'
            else:
                color = 'yellow'

            msg = '%s returned %s (%s)' % (self.name, r.status_code, self.url)

        except Timeout:
            msg = 'Connection to %s timed out' % self.url
            color = 'red'

        except ConnectionError:
            msg = "Can't connect to %s" % self.url
            color = 'red'

        self.log('Current status of %s: %s' % (self.name, msg))

        return msg, color
