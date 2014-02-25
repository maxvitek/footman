__author__ = 'maxvitek'
import pyaudio
import requests
import json
from collections import deque
import math
import audioop
import wave
import subprocess
import os
from termcolor import colored
from commander.util import wipe, get_visualizer_character


class LongListener(object):
    """
    This is the listener object that can listen, transcribe, and return results
    """
    def __init__(self):
        """
        Set a bunch of constants
        """
        self.USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'
        self.SPEECH_API = {
            'url': 'https://www.google.com/speech-api/v2/recognize',
            'params': {
                'output': 'json',
                'key': 'AIzaSyCnl6MRydhw_5fLXIdASxkLJzcJh5iX0M4',
                'lang': 'en-US'
            },
            'headers': {
                'Content-type': 'audio/x-flac; rate=44100',
                'User-Agent': self.USER_AGENT,
            }
        }
        self.WAV_TO_FLAC_COMMAND = ['flac', '--best', '-f', '-s']
        self.CHUNK = 1024  # in bytes
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.WAVE_OUTPUT_FILENAME = "output"
        self.THRESHOLD = 2500  # The threshold intensity that defines silence
                          # and noise signal (an int. lower than THRESHOLD is silence).

        self.SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                           # only silence is recorded. When this time passes the
                           # recording finishes and the file is delivered.

        self.PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                          # is detected, how much of previously recorded audio is
                          # prepended. This helps to prevent chopping the beggining
                          # of the phrase.

        self.SAMPLE_SIZE = None

    def transcribe(self, speech):
        """
        Transcribes speech using the configured API
        """
        r = requests.post(self.SPEECH_API['url'], speech, params=self.SPEECH_API['params'], headers=self.SPEECH_API['headers'])

        if r.text.split('\n')[0] == u'{"result":[]}':
            text = r.text.split('\n')[1]  # TODO insert try block to catch a ValueError for empty results
        else:
            text = r.text.split('\n')[0]  # TODO insert try block to catch a ValueError for empty results

        try:
            data = json.loads(text)
        except ValueError:
            data = {}

        return data

    def listen(self):
        """
        Listen long time
        """
        p = pyaudio.PyAudio()
        self.SAMPLE_SIZE = p.get_sample_size(self.FORMAT)

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        frames = []
        rel = self.RATE / self.CHUNK
        slid_win = deque(maxlen=self.SILENCE_LIMIT * rel)
        #Prepend audio to give a little buffer of silence at the start
        prev_audio = deque(maxlen=self.PREV_AUDIO * rel)
        started = False
        finished = False
        first_pass = True

        while not finished:
            cur_data = stream.read(self.CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))

            # visual feedback
            if not first_pass:
                wipe(20)
            if first_pass:
                first_pass = False
            visual_waveform = [
                [get_visualizer_character(x, 2000) for x in slid_win],
                [get_visualizer_character(x, 1900) for x in slid_win],
                [get_visualizer_character(x, 1800) for x in slid_win],
                [get_visualizer_character(x, 1700) for x in slid_win],
                [get_visualizer_character(x, 1600) for x in slid_win],
                [get_visualizer_character(x, 1500) for x in slid_win],
                [get_visualizer_character(x, 1400) for x in slid_win],
                [get_visualizer_character(x, 1300) for x in slid_win],
                [get_visualizer_character(x, 1200) for x in slid_win],
                [get_visualizer_character(x, 1100) for x in slid_win],
                [get_visualizer_character(x, 1000) for x in slid_win],
                [get_visualizer_character(x, 900) for x in slid_win],
                [get_visualizer_character(x, 800) for x in slid_win],
                [get_visualizer_character(x, 700) for x in slid_win],
                [get_visualizer_character(x, 600) for x in slid_win],
                [get_visualizer_character(x, 500) for x in slid_win],
                [get_visualizer_character(x, 400) for x in slid_win],
                [get_visualizer_character(x, 300) for x in slid_win],
                [get_visualizer_character(x, 200) for x in slid_win],
                [get_visualizer_character(x, 100) for x in slid_win],
            ]
            colors = [
                'green',
                'green',
                'green',
                'green',
                'green',
                'green',
                'green',
                'green',
                'cyan',
                'cyan',
                'cyan',
                'cyan',
                'cyan',
                'cyan',
                'blue',
                'blue',
                'blue',
                'blue',
                'blue',
                'blue',
            ]
            for i in range(20):
                print(colored(''.join(visual_waveform[i]), colors[i]))

            if started:
                if sum([x > self.THRESHOLD for x in slid_win]):
                    frames.append(cur_data)
                else:
                    # The limit was reached, finish capture and deliver.
                    flac_data = self.flaccify(''.join(list(prev_audio) + frames))
                    # Send file to Google and get response
                    data = self.transcribe(flac_data)
                    finished = True
            else:
                if sum([x > self.THRESHOLD for x in slid_win]) > 0:
                    started = True
                else:
                    prev_audio.append(cur_data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        return data

    def flaccify(self, frames):
        wf = wave.open(self.WAVE_OUTPUT_FILENAME + ".wav", 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.SAMPLE_SIZE)
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        conversion_command = self.WAV_TO_FLAC_COMMAND
        conversion_command.append(self.WAVE_OUTPUT_FILENAME + '.wav')
        subprocess.call(conversion_command)

        with open(self.WAVE_OUTPUT_FILENAME + '.flac', 'rb') as f:
            speech = f.read()

        os.remove(self.WAVE_OUTPUT_FILENAME + '.wav')
        os.remove(self.WAVE_OUTPUT_FILENAME + '.flac')

        return speech
