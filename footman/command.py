from collections import defaultdict
import re

from logger import logger
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

    def collect_commands(self):
        self.manager = PluginManager()
        self.manager.setPluginPlaces(['footman/plugins'])
        self.manager.collectPlugins()

        for plugin in sorted(self.manager.getAllPlugins(), key=lambda p: p.plugin_object.command_priority, reverse=True):
            logger.debug('Plugin loaded: ' + plugin.name)
            self.commands.append(plugin.plugin_object.commands)
            logger.debug('Commands added: ' + str(len(plugin.plugin_object.commands)))

        return self

    def detect(self, data):
        logger.debug('Speech detected: ' + str(data))
        if not data:
            pass
        else:
            # log entry
            for alt in data['result'][0]['alternative']:
                logger.debug('Possible transcript: ' + alt['transcript'])

                if self.command_execution:
                    break

                # Check that the transcription is in the command form (keyword + command)
                pattern = re.compile(COMMAND_KEYWORD + ' ' + '(?P<command>.*)')
                supermatch = pattern.match(alt['transcript'])
                if supermatch:
                    # Everything that gets here is a command of some kind, we just need to match it:
                    logger.debug('Supermatch: ' + str(supermatch.groupdict()))

                    if self.command_execution:
                        break

                    # Figure out which command it is
                    for command_group in self.commands:

                        if self.command_execution:
                            break

                        for command_array in command_group:
                            logger.debug('Attempting Commandgroup Match: ' + command_array)

                            pattern = re.compile(command_array)
                            submatch = pattern.match(supermatch.groupdict()['command'])
                            if submatch:
                                # Everything that gets here is a command of THIS kind
                                logger.debug('Submatch: ' + str(submatch.groupdict()))

                                # all RE groups must be named!
                                if not submatch.groupdict():
                                    raise Exception('all re matches here must be named: %s' % command_array)

                                # this is our matched command, let's log it
                                logger.info('Final transcript: ' + alt['transcript'])

                                # execute command group
                                logger.info('Executing command group: ' + str(command_group[command_array]))

                                for command in command_group[command_array]:

                                    # add the dict of re matches as the first argument
                                    args = (submatch.groupdict(),) + command['args']
                                    kwargs = command['kwargs']

                                    # assemble command
                                    command['command'](*args, **kwargs)

                                    self.command_execution = True
