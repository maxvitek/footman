from apex import Apex
from yapsy.IPlugin import IPlugin
from footman.settings import APEX_IP_ADDRESS


class ApexPlugin(IPlugin):
    """
    Abstraction of the Apex plugin.  APEX_IP_ADDRESS config setting
    be present
    """
    def __init__(self):
        IPlugin.__init__(self)
        self.command_priority = 1
        self.voice = None
        self.apex = None

        self.commands = {
            '.*(?P<command>turn on|turn off).*aquarium (?P<outlet>.*)': [
                {
                    'command': self.command,
                    'args': (None, None,),
                    'kwargs': {},
                    'command_priority': 0,
                }
            ]
        }

    def command(self, command_dict, comm_text, outlet_text):
        """
        Give the apex a command
        """

        if comm_text:
            command_text = comm_text
        else:
            command_text = command_dict['command']

        if outlet_text:
            outlet_id_text = outlet_text
        else:
            outlet_id_text = command_dict['outlet']

        if not self.voice:
            self.instantiate_voice()

        if command_text == 'turn on':
            a = Apex(APEX_IP_ADDRESS)
            a.set_outlet(outlet_id_text, 'on')
            self.voice.say({}, 'Turning on the aquarium ' + outlet_id_text)

        elif command_text == 'turn off':
            a = Apex(APEX_IP_ADDRESS)
            a.set_outlet(outlet_id_text, 'off')
            self.voice.say({}, 'Turning off the aquarium ' + outlet_id_text)

        return None

    def instantiate_voice(self):
        """
        We need to separately instatiate this so yapsy doesn't get confused.
        """
        from footman.plugins.voice import VoicePlugin
        self.voice = VoicePlugin()
        return None