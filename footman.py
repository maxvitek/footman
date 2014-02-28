__author__ = 'maxvitek'
# -*- coding: utf-8 -*-
from termcolor import colored
import subprocess
from footman.util import wipe
from footman.command import detect_command
from footman.llt import LongListener
from footman.config import COMMAND_KEYWORD
from pyfiglet import Figlet


def header():
    subprocess.call(['clear'])
    f = Figlet(font='slant')
    print('')
    print(colored(f.renderText(COMMAND_KEYWORD), 'red', attrs=['bold']))
    print('')
    print('')


def prompt():
    while True:
        print(colored('Status: ', 'white') + colored('Listening', 'green', attrs=['bold']))
        print('\n\n\n\n\n\n\n\n')
        ll = LongListener(vis=True, silence_threshold=2500)
        speech = ll.listen()
        wipe(30)

        print(colored('Status: ', 'white') + colored('Executing Command', 'green'))
        detect_command(speech)
        wipe(1)

if __name__ == '__main__':
    header()
    prompt()