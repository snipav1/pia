#!/usr/bin/python

import requests
from termcolor import colored


def bold_underline(str):
    return colored(str, attrs=['bold', 'underline'])

def on_green(str):
    return colored(str, 'cyan', 'on_green', attrs=['bold'])

def on_red(str):
    return colored(str, 'green', 'on_red', attrs=['bold'])

def check_vpn():

    r = requests.get('https://api.ipify.org?format=json')

    res = r.json()

    current_ip_address = res['ip']

    r = requests.get('https://ipapi.co/{}/json/'.format(current_ip_address))

    res2 = r.json()

    isp = res2['org']

    # Fill in provider here - Example: 'Comcast'
    if '<ISP_Provider>' in isp:
        print '\n----------------------------'
        print '{}'.format(on_red('\tVPN is OFF            '))
        print '----------------------------'
    else:
        print '\n----------------------------'
        print '{}'.format(on_green('\tVPN is ON           '))
        print '----------------------------'

    print '\n{}: {}\n'.format(bold_underline('IP Address'), current_ip_address)
    print '{}: {}\n'.format(bold_underline('Country'), res2['country'])
    print '{}: {}\n'.format(bold_underline('Region'), res2['region'])
    print '{}: {}\n'.format(bold_underline('City'), res2['city'])
    print '{}: {}\n'.format(bold_underline('ISP'), res2['org'])

