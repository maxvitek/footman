__author__ = 'maxvitek'
from termcolor import colored
import subprocess
import sys
from commander.voice import record, transcribe, detect_command


def header():
    subprocess.call(['clear'])
    print(colored("  _____            _     _                                    ", 'red', attrs=['bold']))
    print(colored(" |  __ \          (_)   | |                                   ", 'red', attrs=['bold']))
    print(colored(" | |  | |_ __ ___  _  __| |                                   ", 'red', attrs=['bold']))
    print(colored(" | |  | | '__/ _ \| |/ _` |                                   ", 'red', attrs=['bold']))
    print(colored(" | |__| | | | (_) | | (_| |                                   ", 'red', attrs=['bold']))
    print(colored(" |_____/|_|  \___/|_|\__,_|                       _           ", 'red', attrs=['bold']))
    print(colored("  / ____|                                        | |          ", 'red', attrs=['bold']))
    print(colored(" | |     ___  _ __ ___  _ __ ___   __ _ _ __   __| | ___ _ __ ", 'red', attrs=['bold']))
    print(colored(" | |    / _ \| '_ ` _ \| '_ ` _ \ / _` | '_ \ / _` |/ _ \ '__|", 'red', attrs=['bold']))
    print(colored(" | |___| (_) | | | | | | | | | | | (_| | | | | (_| |  __/ |   ", 'red', attrs=['bold']))
    print(colored("  \_____\___/|_| |_| |_|_| |_| |_|\__,_|_| |_|\__,_|\___|_|   ", 'red', attrs=['bold']))
    print(colored("                                                              ", 'red', attrs=['bold']))
    print(colored("                                                              ", 'red', attrs=['bold']))


def wipe(N):
    for n in range(N):
        sys.stdout.write("\x1b[A")
    for n in range(N):
        print('                                                            ')
    for n in range(N):
        sys.stdout.write("\x1b[A")


def prompt():
    print(colored('Status: ', 'white') + colored('Idle', 'yellow'))
    raw_input(colored("<Press Enter To Command>", 'yellow'))
    wipe(2)

    print(colored('Status: ', 'white') + colored('Listening', 'green', attrs=['bold']))
    speech = record()
    wipe(1)

    print(colored('Status: ', 'white') + colored('Processing', 'cyan'))
    transcription = transcribe(speech)
    wipe(1)

    print(colored('Status: ', 'white') + colored('Executing Command', 'green'))
    detect_command(transcription)
    wipe(1)

    prompt()

if __name__ == '__main__':
    header()
    prompt()