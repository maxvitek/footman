__author__ = 'maxvitek'
import sys


def wipe(n):
    for nn in range(n):
        sys.stdout.write("\x1b[A")    # moves up a line
        sys.stdout.write("\r\x1b[K")  # clears the line