import logging
from yapsy.IPlugin import IPlugin
from footman.settings import COMMANDLINE_COMMANDS
import subprocess


class WemoPlugin(IPlugin):
    """
    A plugin that allows for execution of arbitrary commandline tools.
    """
    def __init__(self):
        IPlugin.__init__(self)
        self.command_priority = 1
        self.log = logging.getLogger(__name__)
        self.voice = None

        self.commands = {}

        for comm in COMMANDLINE_COMMANDS:
            self.commands[comm['regex']] = [
                {
                    'command': self.command,
                    'args': (None,),
                    'kwargs': {
                        'command': comm['command'],
                        'success_message': comm['success_message'],
                        'read_output': comm['read_output'],
                    },
                    'command_priority': 0,
                }
            ]

    def command(self, command_dict, comm_text, command=None, success_message=None, failure_message=None, read_output=False):
        """
        Execute the command and report on the results
        """
        if not self.voice:
            self.instantiate_voice()

        if command:
            output = subprocess.check_output(command)

            if output:
                if success_message:
                    self.voice.say({}, success_message)
                else:
                    self.voice.say({}, 'Command execution succeeded.')

                if read_output:
                    self.voice.say({}, output)

            else:
                if failure_message:
                    self.voice.say({}, failure_message)
                else:
                    self.voice.say({}, 'Command execution failed.')


        return None

    def instantiate_voice(self):
        """
        We need to separately instatiate this so yapsy doesn't get confused.
        """
        from footman.plugins.voice import VoicePlugin
        self.voice = VoicePlugin()
        return None
