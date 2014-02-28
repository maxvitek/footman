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
        r = requests.get('http://' + ip + '/rwr.cgi', params={'exec': '4'}, auth=('admin', 'roombawifi'))
        responses.append(r)
    return responses


def spot(ip_list):
    responses = []
    for ip in ip_list:
        r = requests.get('http://' + ip + '/rwr.cgi', params={'exec': '5'}, auth=('admin', 'roombawifi'))
        responses.append(r)
    return responses


def dock(ip_list):
    responses = []
    for ip in ip_list:
        r = requests.get('http://' + ip + '/rwr.cgi', params={'exec': '6'}, auth=('admin', 'roombawifi'))
        responses.append(r)
    return responses


def idle(ip_list):
    responses = []
    for ip in ip_list:
        r = requests.get('http://' + ip + '/rwr.cgi', params={'exec': '1'}, auth=('admin', 'roombawifi'))
        responses.append(r)
    return responses


def main():
    parser = OptionParser()
    parser.add_option('--clean', action='store_true', dest='clean', default=False)
    parser.add_option('--spot', action='store_true', dest='spot', default=False)
    parser.add_option('--dock', action='store_true', dest='dock', default=False)
    parser.add_option('--idle', action='store_true', dest='idle', default=False)
    opts, args = parser.parse_args()

    if opts.clean:
        clean(ROOMBAS)

    if opts.spot:
        spot(ROOMBAS)

    if opts.dock:
        dock(ROOMBAS)

    if opts.idle:
        idle(ROOMBAS)

if __name__ == '__main__':
    main()
