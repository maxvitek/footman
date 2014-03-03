import pyttsx
from yapsy.IPlugin import IPlugin
from footman.settings import VOICE_ID, PYOBJC_PATH
import sys

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
        if VOICE_ID:
            self.engine.setProperty('voice', VOICE_ID)

        self.commands = {
            'say (?P<speech>.*)': [
                {
                    'command': self.say,
                    'args': (None,),
                    'kwargs': {},
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

        self.engine.say(speech_text)
        self.engine.runAndWait()
        if self.engine._inLoop:
            self.engine.endLoop()

        return None