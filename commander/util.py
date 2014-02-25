__author__ = 'maxvitek'
import sys


def wipe(N):
    for n in range(N):
        sys.stdout.write("\x1b[A")
    for n in range(N):
        print('                                                                                                                                       ')
    for n in range(N):
        sys.stdout.write("\x1b[A")


def get_visualizer_character(N, level):
    q, r = divmod(N, level)
    if q > 10:
        return '|'
    if q > 0:
        return '|'
    else:
        return ' '