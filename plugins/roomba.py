__author__ = 'maxvitek'
import requests
import json
from optparse import OptionParser

ROOMBAS = [
    #'10.0.1.70',
    '10.0.1.71',
]


def telemetry(ip):
    r = requests.get('http://' + ip + '/roomba.json', auth=('admin', 'roombawifi'))
    return json.loads(r.text)


def clean(ip_list):
    responses = []
    for ip in ip_list:
        r = requests.get('http://' + ip + '/roomba.cgi?button=CLEAN', auth=('admin', 'roombawifi'))
        responses.append(r.text)
    return responses


def spot(ip_list):
    for ip in ip_list:
        requests.get('http://' + ip + '/roomba.cgi?button=SPOT', auth=('admin', 'roombawifi'))


def dock(ip_list):
    for ip in ip_list:
        requests.get('http://' + ip + '/roomba.cgi?button=DOCK', auth=('admin', 'roombawifi'))


def main():
    parser = OptionParser()
    parser.add_option('--clean', action='store_true', dest='clean', default=False)
    parser.add_option('--spot', action='store_true', dest='spot', default=False)
    parser.add_option('--dock', action='store_true', dest='dock', default=False)
    opts, args = parser.parse_args()

    if opts.clean:
        clean(ROOMBAS)

    if opts.spot:
        spot(ROOMBAS)

    if opts.dock:
        dock(ROOMBAS)

if __name__ == '__main__':
    main()
