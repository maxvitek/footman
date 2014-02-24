__author__ = 'maxvitek'
from plugins.yweather import get_weather

COMMANDS={
    'unleash the robots': [['say', '"unleash the robots"']],
    'turn on the bedroom tv': [
        ['say', '"turning on the bedroom tv"'],
        ['ssh', 'hector', 'wemo', '-f', 'switch', 'bedroomtv', 'on']
    ],
    'turn off the bedroom tv': [
        ['say', '"turning off the bedroom tv"'],
        ['ssh', 'hector', 'wemo', '-f', 'switch', 'bedroomtv', 'off']
    ],
    'turn on the livingroom tv': [
        ['say', '"turning on the livingroom tv"'],
        ['ssh', 'hector', 'wemo', '-f', 'switch', 'bedroomtv', 'on']
    ],
    'turn off the livingroom tv': [
        ['say', '"turning off the livingroom tv"'],
        ['ssh', 'hector', 'wemo', '-f', 'switch', 'bedroomtv', 'off']
    ],
    'make the lights crazy': [
        ['say', '"making the lights crazy"'],
        ['python', 'plugins/hue.py', '1', 'crazy'],
        ['python', 'plugins/hue.py', '2', 'crazy'],
        ['python', 'plugins/hue.py', '3', 'crazy'],
    ],
    'turn on the lights': [
        ['say', '"turning on the lights"'],
        ['python', 'plugins/hue.py', '1', 'on'],
        ['python', 'plugins/hue.py', '2', 'on'],
        ['python', 'plugins/hue.py', '3', 'on'],
    ],
    'turn the lights on': [
        ['say', '"turning on the lights"'],
        ['python', 'plugins/hue.py', '1', 'on'],
        ['python', 'plugins/hue.py', '2', 'on'],
        ['python', 'plugins/hue.py', '3', 'on'],
    ],
    'turn the lights off': [
        ['say', '"turning off the lights"'],
        ['python', 'plugins/hue.py', '1', 'off'],
        ['python', 'plugins/hue.py', '2', 'off'],
        ['python', 'plugins/hue.py', '3', 'off'],
    ],
    'turn off the lights': [
        ['say', '"turning off the lights"'],
        ['python', 'plugins/hue.py', '1', 'off'],
        ['python', 'plugins/hue.py', '2', 'off'],
        ['python', 'plugins/hue.py', '3', 'off'],
    ],
    'dim the lights': [
        ['say', '"dimming the lights"'],
        ['python', 'plugins/hue.py', '1', 'dim'],
        ['python', 'plugins/hue.py', '2', 'dim'],
        ['python', 'plugins/hue.py', '3', 'dim'],
    ],
    'lights full': [
        ['say', '"full power to the lights"'],
        ['python', 'plugins/hue.py', '1', 'bright'],
        ['python', 'plugins/hue.py', '2', 'bright'],
        ['python', 'plugins/hue.py', '3', 'bright'],
    ],
    'get the weather': [
        ['say', get_weather()]
    ],
    'what is the weather': [
        ['say', get_weather()]
    ],
    "what's the weather": [
        ['say', get_weather()]
    ],
}