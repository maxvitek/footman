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
            '.*(?P<command>turn on|turn off|dim|bright|crazy).*(?P<light>' + '|'.join([l for l in self.lights]) +
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
            self.bridge.set_light(self.lights, 'on', True)
            self.bridge.set_light(self.lights, 'bri', 127)
            self.voice.say({}, 'All lights turned on')
        elif light_id_text == 'all' and command_text == 'turn off':
            self.bridge.set_light(self.lights, 'on', False)
            self.voice.say({}, 'All lights turned off')
        elif light_id_text == 'all' and command_text == 'bright':
            self.bridge.set_light(self.lights, 'on', False)
            self.bridge.set_light(self.lights, 'bri', 254)
        elif light_id_text == 'all' and command_text == 'dim':
            self.bridge.set_light(self.lights, 'on', False)
            self.bridge.set_light(self.lights, 'bri', 25)
            self.voice.say({}, 'All lights dimmed')
        elif light_id_text == 'all' and command_text == 'crazy':
            self.bridge.set_light(self.lights, 'on', False)
            self.bridge.set_light(self.lights, 'effect', 'colorloop')
            self.voice.say({}, 'All lights rotating colors')
        elif command_text == 'turn on':
            self.bridge.set_light(light_id_text, 'on', True)
            self.bridge.set_light(light_id_text, 'bri', 127)
            self.voice.say({}, light_id_text + ' light turned on')
        elif command_text == 'turn off':
            self.bridge.set_light(light_id_text, 'on', False)
            self.voice.say({}, light_id_text + ' light turned off')
        elif command_text == 'bright':
            self.bridge.set_light(light_id_text, 'bri', 254)
            self.voice.say({}, light_id_text + ' light brightened')
        elif command_text == 'dim':
            self.bridge.set_light(light_id_text, 'bri', 25)
            self.voice.say({}, light_id_text + ' light dimmed')
        elif command_text == 'crazy':
            self.bridge.set_light(light_id_text, 'effect', 'colorloop')
            self.voice.say({}, light_id_text + ' light rotating colors')

        return None

    def instantiate_voice(self):
        """
        We need to separately instatiate this so yapsy doesn't get confused.
        """
        from footman.plugins.voice import VoicePlugin
        self.voice = VoicePlugin()
        return None


# # get the commandline arguments
# cmd = str(sys.argv)
# targetLight = sys.argv[1]
# targetCmd = sys.argv[2]
#
# # network setup
# hueURL = 'http://' + HUE_IP + '/api/' + HUE_USER + '/lights/'
#
# if targetCmd == 'off':
#     reqData = "{\"on\":false}"
# elif targetCmd == 'on':
#     reqData = "{\"on\":true, \"sat\":35, \"bri\":150,\"hue\":15000,\"effect\":\"none\"}"
# elif targetCmd == 'crazy':
#     reqData = "{\"on\":true, \"sat\":255, \"bri\":255,\"hue\":0,\"effect\":\"colorloop\"}"
# elif targetCmd == 'bright':
#     reqData = "{\"on\":true, \"sat\":35, \"bri\":255,\"hue\":15000,\"effect\":\"none\"}"
# elif targetCmd == 'dim':
#     reqData = "{\"on\":true, \"sat\":35, \"bri\":20,\"hue\":15000,\"effect\":\"none\"}"
# else:
#     reqData = "{}"
#
# requests.put(hueURL + targetLight + '/state',
#              data=reqData)
