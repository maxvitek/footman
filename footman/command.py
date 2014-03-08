import re
from collections import OrderedDict
import logging
from yapsy.PluginManager import PluginManager

from settings import COMMAND_KEYWORD


class CommandControl(object):
    """
    This class collects all of the available commands
    from the plugins, handles a few special ones, and
    then detects
    """
    def __init__(self):
        self.manager = None
        self.commands = []
        self.command_execution = False
        self.log = logging.getLogger(__name__)
        self.root_logger = logging.getLogger().setLevel(logging.INFO)

    def collect_commands(self):
        self.manager = PluginManager()
        self.manager.setPluginPlaces(['footman/plugins'])
        self.manager.collectPlugins()

        for plugin in sorted(self.manager.getAllPlugins(), key=lambda p: p.plugin_object.command_priority, reverse=True):
            self.log.debug('Plugin loaded: ' + plugin.name)

            # this does some fancy stuff to give effect to the command priority that appears in the first command
            # in each command group.
            # it should probably be refactored due to the fact that it's hard to understand.

            plugin_commands = OrderedDict(sorted(plugin.plugin_object.commands.items(),
                                                 key=lambda c: c[1][0]['command_priority'],
                                                 reverse=True))
            for command_group in plugin_commands:
                self.commands.append({
                    command_group: plugin_commands[command_group]
                })
            self.log.debug('Commands added: ' + str(len(plugin.plugin_object.commands)))

        return self

    def detect(self, data):
        self.log.debug('Speech detected: ' + str(data))
        if not data:
            pass
        else:
            # log entry
            for alt in data['result'][0]['alternative']:
                self.log.debug('Possible transcript: ' + alt['transcript'])

                if self.command_execution:
                    break

                # Check that the transcription is in the command form (keyword + command)
                pattern = re.compile(COMMAND_KEYWORD + ' ' + '(?P<command>.*)')
                supermatch = pattern.match(alt['transcript'])
                if supermatch:
                    # Everything that gets here is a command of some kind, we just need to match it:
                    self.log.debug('Supermatch: ' + str(supermatch.groupdict()))

                    if self.command_execution:
                        break

                    # Figure out which command it is
                    for command_group in self.commands:

                        if self.command_execution:
                            break

                        for command_array in command_group:
                            self.log.debug('Attempting Commandgroup Match: ' + command_array)

                            pattern = re.compile(command_array)
                            submatch = pattern.match(supermatch.groupdict()['command'].lower())
                            if submatch:
                                # Everything that gets here is a command of THIS kind
                                self.log.debug('Submatch: ' + str(submatch.groupdict()))

                                # all RE groups must be named!
                                if not submatch.groupdict():
                                    raise Exception('all re matches here must be named: %s' % command_array)

                                # this is our matched command, let's log it
                                self.log.info('Final: ' + alt['transcript'])

                                # execute command group
                                self.log.debug('Executing command group: ' + str(command_group[command_array]))

                                for command in command_group[command_array]:

                                    # add the dict of re matches as the first argument
                                    args = (submatch.groupdict(),) + command['args']
                                    kwargs = command['kwargs']

                                    # assemble command
                                    command['command'](*args, **kwargs)

                                    self.command_execution = True
                else:
                    self.log.info('No command keyword detected: %s' % COMMAND_KEYWORD)

    def direct_command(self, command_text):
        """
        To facilitate testing, we can contruct a google-like response
        containing arbitrary text.
        """

        direct_command = {
            'result':
                [
                    {
                        'alternative': [
                            {
                                'transcript': COMMAND_KEYWORD + ' ' + command_text
                            }
                        ]
                    }
                ]
        }

        self.detect(direct_command)
