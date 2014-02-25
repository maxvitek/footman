__author__ = 'maxvitek'
from plugins.yweather import get_weather

WOLFRAM_ALPHA_API_KEY = 'Q9YE6Y-HRXTP4K8G9'

VOICE = 'Oliver'

COMMAND_KEYWORD = 'Jarvis'

COMMANDS = {
    'device status': [
        ['say', '-v', VOICE, '"getting device status"'],
        ['ssh', 'hector', 'wemo', '-f', '-v', 'status', '|', 'say', '-v', VOICE]
    ],
    'unleash the robots': [
        ['say', '-v', VOICE, '"unleashing the robots"'],
        ['python', 'plugins/roomba.py', '--clean']
    ],
    'dock the robots': [
        ['say', '-v', VOICE, '"docking the robots"'],
        ['python', 'plugins/roomba.py', '--dock']
    ],
    'turn on the office light': [
        ['say', '-v', VOICE, '"turning on the office light"'],
        ['ssh', 'hector', 'wemo', '-f', 'switch', 'officelight', 'on']
    ],
    'turn off the office light': [
        ['say', '-v', VOICE, '"turning off the office light"'],
        ['ssh', 'hector', 'wemo', '-f', 'switch', 'officelight', 'on']
    ],
    'turn on the bedroom tv': [
        ['say', '-v', VOICE, '"turning on the bedroom tv"'],
        ['ssh', 'hector', 'wemo', '-f', 'switch', 'bedroomtv', 'on']
    ],
    'turn off the bedroom tv': [
        ['say', '-v', VOICE, '"turning off the bedroom tv"'],
        ['ssh', 'hector', 'wemo', '-f', 'switch', 'bedroomtv', 'off']
    ],
    'turn on the livingroom tv': [
        ['say', '-v', VOICE, '"turning on the livingroom tv"'],
        ['ssh', 'hector', 'wemo', '-f', 'switch', 'bedroomtv', 'on']
    ],
    'turn off the livingroom tv': [
        ['say', '-v', VOICE, '"turning off the livingroom tv"'],
        ['ssh', 'hector', 'wemo', '-f', 'switch', 'bedroomtv', 'off']
    ],
    'make the lights crazy': [
        ['say', '-v', VOICE, '"making the lights crazy"'],
        ['python', 'plugins/hue.py', '1', 'crazy'],
        ['python', 'plugins/hue.py', '2', 'crazy'],
        ['python', 'plugins/hue.py', '3', 'crazy'],
    ],
    'turn on the lights': [
        ['say', '-v', VOICE, '"turning on the lights"'],
        ['python', 'plugins/hue.py', '1', 'on'],
        ['python', 'plugins/hue.py', '2', 'on'],
        ['python', 'plugins/hue.py', '3', 'on'],
    ],
    'turn the lights on': [
        ['say', '-v', VOICE, '"turning on the lights"'],
        ['python', 'plugins/hue.py', '1', 'on'],
        ['python', 'plugins/hue.py', '2', 'on'],
        ['python', 'plugins/hue.py', '3', 'on'],
    ],
    'turn the lights off': [
        ['say', '-v', VOICE, '"turning off the lights"'],
        ['python', 'plugins/hue.py', '1', 'off'],
        ['python', 'plugins/hue.py', '2', 'off'],
        ['python', 'plugins/hue.py', '3', 'off'],
    ],
    'turn off the lights': [
        ['say', '-v', VOICE, '"turning off the lights"'],
        ['python', 'plugins/hue.py', '1', 'off'],
        ['python', 'plugins/hue.py', '2', 'off'],
        ['python', 'plugins/hue.py', '3', 'off'],
    ],
    'dim the lights': [
        ['say', '-v', VOICE, '"dimming the lights"'],
        ['python', 'plugins/hue.py', '1', 'dim'],
        ['python', 'plugins/hue.py', '2', 'dim'],
        ['python', 'plugins/hue.py', '3', 'dim'],
    ],
    'lights full': [
        ['say', '-v', VOICE, '"full power to the lights"'],
        ['python', 'plugins/hue.py', '1', 'bright'],
        ['python', 'plugins/hue.py', '2', 'bright'],
        ['python', 'plugins/hue.py', '3', 'bright'],
    ],
    'get the weather': [
        ['say', '-v', VOICE, get_weather()]
    ],
    'what is the weather': [
        ['say', '-v', VOICE, get_weather()]
    ],
    "what's the weather": [
        ['say', '-v', VOICE, get_weather()]
    ],
}