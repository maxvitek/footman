import os

# task broker and results broker for footman's celery worker
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://user:password@host:port/vhost')

# command keyword to invoke the footman
COMMAND_KEYWORD = os.getenv('COMMAND_KEYWORD', 'Marvin')

# wolfram alpha plugin ------------/
# api key for wolfram alpha plugin
WOLFRAM_ALPHA_API_KEY = os.getenv('WOLFRAM_ALPHA_API_KEY', '1234567890ABCDEF')

# voice plugin --------------------/
# voice id for voice plugin
VOICE_ID = os.getenv('VOICE_ID', 'com.apple.speech.synthesis.voice.oliver.premium')

# pyobjc path for voice plugin -- OS X specific -- this is a hideous thing to have to have in settings
PYOBJC_PATH = os.getenv('PYOBJC_PATH', '/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/PyObjC')

# nest plugin ---------------------/
# nest login info
NEST_USER = os.getenv('NEST_USER', 'user@email.com')
NEST_PASSWD = os.getenv('NEST_PASSWD', 'p455wd')