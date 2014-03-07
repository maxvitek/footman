__author__ = 'maxvitek'
import sys
import netifaces


def wipe(n):
    for nn in range(n):
        sys.stdout.write("\x1b[A")    # moves up a line
        sys.stdout.write("\r\x1b[K")  # clears the line


def get_ip_addresses(local=False):
    interfaces = netifaces.interfaces()
    result = []
    for i in interfaces:
        if i == 'lo':
            continue
        iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
        if iface != None:
            for j in iface:
                if not local and j['addr'] == '127.0.0.1':
                    continue
                else:
                    result.append(j['addr'])
    return result