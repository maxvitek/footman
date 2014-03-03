from __future__ import absolute_import
import wolframalpha
from yapsy.IPlugin import IPlugin

from footman.settings import WOLFRAM_ALPHA_API_KEY


class WolframAlphaPlugin(IPlugin):
    """
    This is the Wolfram Alpha plugin for general queries.  You must
    provide a setting for the WOLFRAM_ALPHA_API_KEY.  This plugin also
    depends on the Voice plugin.
    """
    def __init__(self):
        IPlugin.__init__(self)
        self.command_priority = 0
        self.client = wolframalpha.Client(WOLFRAM_ALPHA_API_KEY)
        self.voice = None

        self.commands = {
            '(?P<query>.*)': [
                {
                    'command': self.speak_query_result,
                    'args': (None,),
                    'kwargs': {},
                },
            ]
        }

    def query(self, query_dict, text):
        """
        WolfrAlpha method that queries the WolframAlpha computation knowledge
        engine.  If the text argument is provided, it is used, otherwise the
        method looks for a dictionary containing a 'query' key.
        """
        if text:
            query_text = text
        else:
            query_text = query_dict['query']

        result = self.client.query(query_text)
        return result

    def simple_query(self, query_dict, text):
        """
        The simple query takes the pod that WA thinks is most relevant.
        """
        if text:
            query_text = text
        else:
            query_text = query_dict['query']

        result = self.client.query(query_text)

        # return input pod as a title, then a pause, and then the most relevant result pod's text
        return result.pods[0].text + ',,,' + result.pods[1].text  # WA returns its best guess as the second pod

    def speak_query_result(self, query_dict, text):
        """
        Speak a query result.
        """
        if text:
            query_text = text
        else:
            query_text = query_dict['query']

        result = self.simple_query({}, query_text)

        if not self.voice:
            self.instantiate_voice()

        self.voice.say({}, result)
        return None

    def instantiate_voice(self):
        """
        We need to separately instatiate this so yapsy doesn't get confused.
        """
        from footman.plugins.voice import VoicePlugin
        self.voice = VoicePlugin()
        return None