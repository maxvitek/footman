from __future__ import absolute_import
from cleverbot import Cleverbot
from yapsy.IPlugin import IPlugin
import memcache
import datetime
from footman.settings import MEMCACHED_HOST

mc = memcache.Client([MEMCACHED_HOST], debug=0)


class CleverbotChat(object):
    """
    Chat object which will be memcached
    """
    def __init__(self, data=None):
        self.chat_data = data
        self.last_update = datetime.datetime.now()
        self.expiration = self.last_update + datetime.timedelta(minutes=1)
        self.ready = False

    def expired(self):
        """
        Check expiration and returns True or False
        """
        if self.expiration < datetime.datetime.now():
            return True
        else:
            return False


class CleverbotPlugin(IPlugin):
    """
    Abstraction of the Cleverbot plugin.
    """
    def __init__(self):
        IPlugin.__init__(self)
        self.chat = mc.get('footman_chat')

        # are we in a chat?
        if self.chat and not self.chat.expired() and self.chat.ready:
            self.chat = CleverbotChat(self.chat.chat_data)
            self.command_priority = 10
            self.commands = {
                "(?P<chat>.*)": [
                    {
                        'command': self.chat_some,
                        'args': (None,),
                        'kwargs': {},
                        'command_priority': 0,
                    }
                ],
                "(?P<chat>end chat)": [
                    {
                        'command': self.chat_end,
                        'args': (None,),
                        'kwargs': {},
                        'command_priority': 1,
                    }
                ],
            }
        elif self.chat and not self.chat.expired() and not self.chat.ready:
            self.command_priority = 10
            self.commands = {
                "(?P<chat>.*)": [
                    {
                        'command': self.chat_idle,
                        'args': (None,),
                        'kwargs': {},
                        'command_priority': 0,
                    }
                ]
            }
        else:
            self.chat = CleverbotChat()
            self.command_priority = 1
            self.commands = {
                "(?P<chat>let's chat)": [
                    {
                        'command': self.chat_some,
                        'args': (None,),
                        'kwargs': {},
                        'command_priority': 0,
                    }
                ]
            }
        self.chatbot = Cleverbot()
        self.voice = None

    def chat_some(self, chat_dict, text):
        """
        Our chatty method
        """
        if text:
            chat_text = text
        else:
            chat_text = chat_dict['chat']

        reply = self.chatbot.ask(chat_text)

        if not self.voice:
            self.instantiate_voice()

        self.voice.say({}, reply)

        self.chat.chat_data = self.chatbot.data
        self.chat.ready = True
        mc.set('footman_chat', self.chat)
        return None

    def chat_idle(self, chat_dict, text):
        """
        Does nothing since the chat is already working on a reply.
        Limitations:  Currently loses the text
        """
        pass

    def chat_end(self, chat_dict, text):
        """
        Ends the chat session
        """
        self.voice.say({}, 'Ok.  Nice chatting with you.')
        mc.set('footman_chat', None)
        return None

    def instantiate_voice(self):
        """
        We need to separately instatiate this so yapsy doesn't get confused.
        """
        from footman.plugins.voice import VoicePlugin
        self.voice = VoicePlugin()
        return None
