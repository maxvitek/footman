__author__ = 'maxvitek'
from bs4 import BeautifulSoup
import requests


def get_weather():
    r = requests.get('http://weather.yahooapis.com/forecastrss?w=2379574')  # Chicago
    soup = BeautifulSoup(r.text)

    temp = soup.find_all('yweather:condition')[0]['temp']
    text = soup.find_all('yweather:condition')[0]['text']

    return "It's " + str(temp) + " degrees and " + text


if __name__ == '__main__':
    get_weather()