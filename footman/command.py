import pyaudio
import requests
import subprocess
from config import COMMANDS, COMMAND_KEYWORD, WOLFRAM_ALPHA_API_KEY, VOICE
from bs4 import BeautifulSoup
from logger import logger

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output"


def detect_command(data):
    match = False
    if not data:
        pass
    else:
        for alt in data['result'][0]['alternative']:
            for com in COMMANDS.keys():
                if alt['transcript'] == COMMAND_KEYWORD + ' ' + com:
                    match = True
                    logger.info('Command: ' + com)
                    for step in COMMANDS[com]:
                        subprocess.call(step)
                    break
            if match:
                break
        else:
            text = data['result'][0]['alternative'][0]['transcript'].split()
            if text[0] == COMMAND_KEYWORD:
                logger.info('General Query: ' + ' '.join(text[1:]))
                wolfram_query_params = {
                    'input': ' '.join(text[1:]),
                    'appid': WOLFRAM_ALPHA_API_KEY,
                }
                r = requests.get('http://api.wolframalpha.com/v2/query', params=wolfram_query_params)
                soup = BeautifulSoup(r.text)
                if soup.find(id='Result'):  # handles a clear result
                    results = soup.find(id='Result').plaintext.string
                elif soup.find(id='InstantaneousWeather:WeatherData'):  # handles a weather result
                    results = soup.find(id='InstantaneousWeather:WeatherData').plaintext.string
                elif soup.find(id='WeatherForecast:WeatherData'):
                    results = soup.find(id='WeatherForecast:WeatherData').plaintext.string
                elif soup.find(id='Definition:WordData'):
                    results = soup.find(id='Definition:WordData').plaintext.string
                else:
                    results = ''
                    print(soup.prettify())
                subprocess.call(['say', '-v', VOICE, results])

            else:
                logger.info('Missing Keyword: ' + ' '.join(text[0:]))

