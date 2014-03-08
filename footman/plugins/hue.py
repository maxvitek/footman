from phue import Bridge
import logging
from yapsy.IPlugin import IPlugin
from footman.settings import HUE_USER, HUE_IP_ADDRESS
from footman.settings import MEMCACHED_HOST
import memcache

mc = memcache.Client([MEMCACHED_HOST], debug=0)


class HuePlugin(IPlugin):
    """
    Abstraction of the Hue plugin.
    """
    def __init__(self):
        IPlugin.__init__(self)
        self.command_priority = 1
        self.log = logging.getLogger(__name__)
        self.voice = None
        self.bridge = None
        self.lights = mc.get('footman_lights')
        if not self.lights:
            self.bridge = Bridge(ip=HUE_IP_ADDRESS, username=HUE_USER)
            self.api_data = self.bridge.get_api()
            self.lights = [self.api_data['lights'][key]['name'] for key in self.api_data['lights'].keys()]
            mc.set('footman_lights', self.lights)

        self.commands = {
            '.*(?P<command>turn on|turn off|dim|bright|crazy).*(?P<light>' + '|'.join([l.lower() for l in self.lights]) +
            '|all).*light.*': [
                {
                    'command': self.command,
                    'args': (None, None,),
                    'kwargs': {},
                    'command_priority': 0,
                }
            ]
        }

    def command(self, command_dict, comm_text, light_text):
        """
        Give the robot a command
        """

        if comm_text:
            command_text = comm_text
        else:
            command_text = command_dict['command']

        if light_text:
            light_id_text = light_text
        else:
            light_id_text = command_dict['light']

        if not self.voice:
            self.instantiate_voice()

        if not self.bridge:
            self.bridge = Bridge(ip=HUE_IP_ADDRESS, username=HUE_USER)

        if light_id_text == 'all' and command_text == 'turn on':
            self.bridge.set_light([str(light) for light in self.lights], 'on', True)
            self.bridge.set_light([str(light) for light in self.lights], 'bri', 127)
            self.voice.say({}, 'All lights turned on')
        elif light_id_text == 'all' and command_text == 'turn off':
            self.bridge.set_light([str(light) for light in self.lights], 'on', False)
            self.voice.say({}, 'All lights turned off')
        elif light_id_text == 'all' and command_text == 'bright':
            self.bridge.set_light([str(light) for light in self.lights], 'on', False)
            self.bridge.set_light([str(light) for light in self.lights], 'bri', 254)
        elif light_id_text == 'all' and command_text == 'dim':
            self.bridge.set_light([str(light) for light in self.lights], 'on', False)
            self.bridge.set_light([str(light) for light in self.lights], 'bri', 25)
            self.voice.say({}, 'All lights dimmed')
        elif light_id_text == 'all' and command_text == 'crazy':
            self.bridge.set_light([str(light) for light in self.lights], 'on', False)
            self.bridge.set_light([str(light) for light in self.lights], 'effect', 'colorloop')
            self.voice.say({}, 'All lights rotating colors')
        elif command_text == 'turn on':
            for light in self.lights:
                if light.lower() == light_id_text:
                    self.bridge.set_light(str(light), 'on', True)
                    self.bridge.set_light(str(light), 'bri', 127)
                    self.voice.say({}, light + ' light turned on')
        elif command_text == 'turn off':
            for light in self.lights:
                if light.lower() == light_id_text:
                    self.bridge.set_light(str(light), 'on', False)
                    self.voice.say({}, light + ' light turned off')
        elif command_text == 'bright':
            for light in self.lights:
                if light.lower() == light_id_text:
                    self.bridge.set_light(str(light), 'bri', 254)
                    self.voice.say({}, light + ' light brightened')
        elif command_text == 'dim':
            for light in self.lights:
                if light.lower() == light_id_text:
                    self.bridge.set_light(str(light), 'bri', 25)
                    self.voice.say({}, light + ' light dimmed')
        elif command_text == 'crazy':
            for light in self.lights:
                if light.lower() == light_id_text:
                    self.bridge.set_light(str(light), 'effect', 'colorloop')
                    self.voice.say({}, light + ' light rotating colors')

        return None

    def instantiate_voice(self):
        """
        We need to separately instatiate this so yapsy doesn't get confused.
        """
        from footman.plugins.voice import VoicePlugin
        self.voice = VoicePlugin()
        return None
