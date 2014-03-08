from ouimeaux.environment import Environment
import logging
from yapsy.IPlugin import IPlugin
import memcache
from footman.settings import MEMCACHED_HOST
from footman.util import get_ip_addresses


mc = memcache.Client([MEMCACHED_HOST], debug=0)


class WemoPlugin(IPlugin):
    """
    Abstraction of the Wemo plugin.
    """
    def __init__(self):
        IPlugin.__init__(self)
        self.command_priority = 1
        self.voice = None
        bind_port = 54321  # number
        host = get_ip_addresses()[0]  # we just grab the first one that isn't local
        while bind_port < 54329:
            bind = '{0}:{1}'.format(host, str(bind_port))
            try:
                self.env = Environment(bind=bind, with_subscribers=False)
                self.env.start()
                break
            except:
                bind_port += 1

        # retrieve or create device cache
        self.devices = mc.get('footman_wemo_cache')
        if not self.devices:
            self.env.discover(5)
            self.devices = self.env.list_switches()
            mc.set('footman_wemo_cache', self.devices)
        self.log = logging.getLogger(__name__)

        self.commands = {
            '.*turn (?P<command>on|off).*(?P<device>' + '|'.join([d.lower() for d in self.devices]) + ').*': [
                {
                    'command': self.command,
                    'args': (None, None,),
                    'kwargs': {},
                    'command_priority': 0,
                }
            ]
        }

    def command(self, command_dict, comm_text, device_text):
        """
        Give the robot a command
        """

        if comm_text:
            command_text = comm_text
        else:
            command_text = command_dict['command']

        device_id_text = None

        if device_text:
            for d in self.devices:
                if d.lower() == device_text:
                    device_id_text = d
        else:
            for d in self.devices:
                if d.lower() == command_dict['device']:
                    device_id_text = d

        if not device_id_text:
            raise Exception('Device unknown')

        self.env.discover(5)

        switch = self.env.get_switch(device_id_text)

        if not self.voice:
            self.instantiate_voice()

        self.voice.say({}, 'Turning ' + command_text + ' the ' + device_id_text + '.')

        if command_text == 'on':
            switch.on()
        elif command_text == 'off':
            switch.off()

    def instantiate_voice(self):
        """
        We need to separately instatiate this so yapsy doesn't get confused.
        """
        from footman.plugins.voice import VoicePlugin
        self.voice = VoicePlugin()
        return None