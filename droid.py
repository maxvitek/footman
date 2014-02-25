__author__ = 'maxvitek'
# -*- coding: utf-8 -*-
from termcolor import colored
import subprocess
from commander.util import wipe
from commander.voice import record, transcribe, detect_command
from commander.llt import LongListener


def header():
    subprocess.call(['clear'])
    print('')
    print(colored(u"     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗", 'red', attrs=['bold']))
    print(colored(u"     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝", 'red', attrs=['bold']))
    print(colored(u"     ██║███████║██████╔╝██║   ██║██║███████╗", 'red', attrs=['bold']))
    print(colored(u"██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║", 'red', attrs=['bold']))
    print(colored(u"╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║", 'red', attrs=['bold']))
    print(colored(u" ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝", 'red', attrs=['bold']))
    print('')
    print('')


def prompt():
    print(colored('Status: ', 'white') + colored('Listening', 'green', attrs=['bold']))
    print('\n\n\n\n\n\n\n\n')
    ll = LongListener()
    speech = ll.listen()
    wipe(30)

    print(colored('Status: ', 'white') + colored('Executing Command', 'green'))
    detect_command(speech)
    wipe(1)

    prompt()

if __name__ == '__main__':
    header()
    prompt()