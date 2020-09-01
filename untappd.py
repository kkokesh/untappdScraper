#!/usr/bin/env python
"""
    Author: Micah Hoffman (@WebBreacher)
    Purpose: To look up a user on Untappd.com and provide drinking profile
"""

import argparse
# import geocoder
# import gmplot
# import googlemaps
import re
import requests
import time

from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from geocode_api_keys import *


####
# Functions
####

# Parse command line input
parser = argparse.ArgumentParser(description='Grab Untappd user activity')
parser.add_argument('-r', '--recent', action='store_true', help='Just dump the locations of the last beers they logged')
parser.add_argument('-u', '--user', required=True, help='Username to research')
args = parser.parse_args()


def get_mean(lst):
    return float(sum(lst) / len(lst))


def get_data_from_untappd(url):
    # Setting up and Making the Web Call
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        headers = {'User-Agent': user_agent}
        # Make web request for that URL and don't verify SSL/TLS certs
        response = requests.get(url, headers=headers, verify=False)
        return response.text

    except Exception as e:
        print('[!]   ERROR - Untappd issue: {}'.format(str(e)))
        exit(1)


def get_user_data(passed_user):
    # Parsing user information
    url = 'https://untappd.com/user/{}'.format(passed_user)
    print("\n[ ] USER DATA: Requesting {}".format(url))
    resp = get_data_from_untappd(url)
    html_doc = BeautifulSoup(resp, 'html.parser')
    user1 = html_doc.find_all('span', 'stat')
    if user1:
        return user1

def get_beers_data(passed_user):
    beers_drank = []
    # Parsing user beer information
    url = 'https://untappd.com/user/{}/beers'.format(passed_user)
    print("\n[ ] BEER CONSUMPTION DATA: Requesting {}".format(url))
    resp = get_data_from_untappd(url)
    html_doc = BeautifulSoup(resp, 'html.parser')
    beers = html_doc.find_all('abbr', 'date-time')
    for b in beers:
        beers_drank.append(b.text.strip())
    if beers_drank:
        return beers_drank


def get_beersonly_data(passed_user):
    beers_drank = []
    # Parsing user beer information
    url = 'https://untappd.com/user/{}/'.format(passed_user)
    print("\n[ ] BEER LOCATION DATA: Requesting {}\n".format(url))
    resp = get_data_from_untappd(url)
    html_doc = BeautifulSoup(resp, 'html.parser')
    beers = html_doc.find_all('div', 'checkin')
    for b in beers:
        beers_drank.append(b.text.strip())
    if beers_drank:
        return beers_drank

###########################
# Start
###########################

# Suppress HTTPS warnings
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

###############
# Get User info
###############
user = get_user_data(args.user)
if user:
    print('\n        {:>6}'.format(user[0].text))
    print('        {:>6}'.format(user[1].text))
  
