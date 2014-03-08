import pyttsx
import logging
from yapsy.IPlugin import IPlugin
from footman.settings import VOICE_ID, PYOBJC_PATH, COMMAND_KEYWORD
import sys
import re

if PYOBJC_PATH not in sys.path:
    sys.path.extend([PYOBJC_PATH])


class VoicePlugin(IPlugin):
    """
    Abstraction of the Voice plugin.  If the VOICE_ID setting is set
    the plugin will use it.  On OS X, PYOBJC_PATH must be set.
    """
    def __init__(self):
        IPlugin.__init__(self)
        self.command_priority = 1
        self.engine = pyttsx.init()
        self.log = logging.getLogger(__name__)
        if VOICE_ID:
            self.engine.setProperty('voice', VOICE_ID)

        self.commands = {
            'say (?P<speech>.*)': [
                {
                    'command': self.say,
                    'args': (None,),
                    'kwargs': {},
                    'command_priority': 0,
                }
            ]
        }

    def say(self, speech_dict, text):
        """
        Voice method that speaks text.  If the text argument is
        provided, it is used, otherwise the method looks for a
        dictionary containing a 'speech' key.
        """
        if text:
            speech_text = text
        else:
            speech_text = speech_dict['speech']

        speech_text = apply_replacements_to_abbreviations(speech_text)

        self.log.info(COMMAND_KEYWORD + ': ' + speech_text)

        self.engine.say(speech_text)
        self.engine.runAndWait()
        if self.engine._inLoop:
            self.engine.endLoop()

        return None


def apply_replacements_to_abbreviations(raw_text):
    regex_replacements = [
        ('(\s)ms(\s)', r'\1miliseconds\2'),
        ('Mbit/s', 'mega bits per second'),
        ('\n', ',,,\n'),
    ]

    text = raw_text

    for r in regex_replacements:
        text = re.sub(
            r[0], r[1],
            text
        )

    return text