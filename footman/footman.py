from __future__ import absolute_import
# -*- coding: utf-8 -*-
from termcolor import colored
import subprocess
from pyfiglet import Figlet

from llt import LongListener

from footman.celery import app
from footman.util import wipe
from footman.command import CommandControl
from footman.settings import COMMAND_KEYWORD


def header():
    subprocess.call(['clear'])
    f = Figlet(font='slant')
    print('')
    print(colored(f.renderText(COMMAND_KEYWORD), 'red', attrs=['bold']))
    print('')
    print('')


def prompt():
    while True:
        ll = LongListener(vis=True, silence_threshold=5500)
        speech_data = ll.listen()
        process_speech.delay((speech_data))
        wipe(20)


@app.task
def process_speech(speech_data):
    ll = LongListener()
    speech = ll.transcribe(speech_data)
    cc = CommandControl().collect_commands()
    cc.detect(speech)

    return None


def main():
    header()
    prompt()


if __name__ == '__main__':
    main()