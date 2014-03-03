from __future__ import absolute_import
from nest import Nest
from yapsy.IPlugin import IPlugin

from footman.settings import NEST_USER, NEST_PASSWD


class NestPlugin(IPlugin):
    """
    This plugin interfaces with the unofficial Nest api using the
    python Nest-API package.
    """
    def __init__(self):
        IPlugin.__init__(self)
        self.command_priority = 2
        self.nest = None
        self.voice = None

        self.commands = {
            'what.*(?P<nest_temp>indoor temp).*': [
                {
                    'command': self.get_temp,
                    'args': (None,),
                    'kwargs': {},
                }
            ],
            'what.*(?P<nest_hum>indoor humid).*': [
                {
                    'command': self.get_humidity,
                    'args': (None,),
                    'kwargs': {},
                }
            ],
            'what.*(?P<nest_cond>indoor condition).*': [
                {
                    'command': self.get_conditions,
                    'args': (None,),
                    'kwargs': {},
                }
            ],
            'set.*indoor temp.*to (?P<set_nest_temp>\d*).*': [
                {
                    'command': self.set_temp,
                    'args': (None,),
                    'kwargs': {},
                }
            ],
        }

    def initialize(self):
        self.nest = Nest(NEST_USER, NEST_PASSWD)

    def get_temp(self, command_dict, text):
        """
        Get the Nest's indoor temperature
        """
        if text:
            command_text = text
        else:
            command_text = command_dict['nest_temp']

        if not self.nest:
            self.initialize()

        if not self.voice:
            self.instantiate_voice()

        response_text = 'the temperature in the house is ' + str(self.nest.temperature) + ' degrees Fahrenheit'

        self.voice.say({}, response_text)
        return None

    def get_humidity(self, command_dict, text):
        """
        Get the Nest's indoor humidity
        """
        if text:
            command_text = text
        else:
            command_text = command_dict['nest_hum']

        if not self.nest:
            self.initialize()

        if not self.voice:
            self.instantiate_voice()

        response_text = 'the humidity in the house is ' + str(self.nest.humidity) + ''

        self.voice.say({}, response_text)
        return None

    def get_conditions(self, command_dict, text):
        """
        Get the Nest's indoor temperature and humidity
        """
        if text:
            command_text = text
        else:
            command_text = command_dict['nest_cond']

        if not self.nest:
            self.initialize()

        if not self.voice:
            self.instantiate_voice()

        response_text = 'the temperature in the house is ' + str(self.nest.temperature) + ' degrees Fahrenheit, ' + \
            'and the humidity is ' + str(self.nest.humidity) + ''

        self.voice.say({}, response_text)
        return None

    def set_temp(self, command_dict, text):
        """
        Set the Nest's indoor temperature target
        """
        if text:
            command_text = text
        else:
            command_text = command_dict['set_nest_temp']

        if not self.nest:
            self.initialize()

        if not self.voice:
            self.instantiate_voice()

        response_text = 'setting the house temperature to ' + command_text + ' degrees Fahrenheit'

        self.nest.set_target_temperature(int(command_text))

        self.voice.say({}, response_text)
        return None

    def instantiate_voice(self):
        """
        We need to separately instatiate this so yapsy doesn't get confused.
        """
        from footman.plugins.voice import VoicePlugin
        self.voice = VoicePlugin()
        return None