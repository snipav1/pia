#!/usr/bin/python

# Author: Emmanuel A. Hernandez <@snipa.v1>.

import os
import sys
import subprocess
import argparse
import psutil
import signal
import requests
import time
from ip import check_vpn

""" 
    @author: Emmanuel Hernandez - @snipa.v1@gmail.com

    Easy to use cli to start and stop openvpn with its corresponding .ovpn files
    
    Usage:
        - Connect using .ovpn conf file
        sudo ./pia.py --start=SiliconValley.ovpn
        
        - Stop ovpn process and verify vpn is off (Fill in ISP provider line #72)
        sudo ./pia.py --stop
        
        - Check if vpn is on (Fill in ISP provider in ip.py file on line #30)
        sudo ./pia.py --status

"""

banner = r'''
------------------------------------------------------------
                    ______ _____  ___  
                    | ___ \_   _|/ _ \ 
                    | |_/ / | | / /_\ \
                    |  __/  | | |  _  |
                    | |    _| |_| | | |
                    \_|    \___/\_| |_/
                                             
------------------------------------------------------------
'''


parser = argparse.ArgumentParser()
parser.add_argument("--start",
                    dest="start",
                    help="Config file to use. Ex: SiliconValley.ovpn",
                    action='store')
parser.add_argument("--stop",
                    dest="stop",
                    help="Stop VPN.",
                    action='store_true')
parser.add_argument("--status",
                    dest="status",
                    help="Check status of VPN.",
                    action='store_true')
args = parser.parse_args()
start = args.start if args.start else None
stop = args.stop if args.stop else None
status = args.status if args.status else None

COMMAND = '/usr/sbin/openvpn /etc/openvpn/'


def check_root():
    if not os.geteuid() == 0:
        print('[.] Only root can run this script')
        print('[.] Exiting...')
        sys.exit()


def check_ip():
    print '\n[.] Checking if VPN is on..'
    r = requests.get('https://api.ipify.org?format=json')
    res = r.json()
    current_ip_address = res['ip']
    r2 = requests.get('https://ipapi.co/{}/json/'.format(current_ip_address))
    res2 = r2.json()
    isp = res2['org']
    return isp, current_ip_address


def vpn_on():
    isp, current_ip_address = check_ip()

    #Fill in provider here - Example: 'Comcast'
    if '<ISP_Provider>' in isp:
        print('[.] VPN is OFF')
        return False
    else:
        print '[.] VPN is on with IP Address: {}'.format(current_ip_address)
        return True


class Pia():
    def __init__(self, arg=None):
        self.arg = arg

    def vpn_start(self):
        bashCommand = COMMAND + self.arg
        print('[.] Connecting to {} VPN...\n'.format(self.arg))
        print('[.] bashCommand is: {}\n'.format(bashCommand))
        try:
            p = subprocess.Popen(['bash', '-c', bashCommand])
            print('PID is: {}'.format(p.pid))
        except ValueError as e:
            print 'Could not run openvpn command because of: {}'.format(e)
        time.sleep(8)
        print('\n[.] Connected to VPN! :)\n')

        print('[.] Done\n')

    # 1. Check if vpn is on, if on, Find PID, kill PID, and verify VPN is off
    def vpn_stop(self):
        if vpn_on():

            # 1. Find PID
            pid = ''
            print('[.] Stopping VPN...\n')
            for proc in psutil.process_iter():
                try:
                    pinfo = proc.as_dict(attrs=['pid', 'name'])
                except psutil.NoSuchProcess:
                    pass

                if 'openvpn' in pinfo['name']:
                    pid = pinfo['pid']

            # 2. kill pid
            os.kill(pid, signal.SIGKILL)

            # 3. Verify VPN is off
            print('[.] Checking VPN is off..')
            time.sleep(5)

            if not vpn_on:
                print('[.] VPN is still on!')
                print('[.] Exiting...')
                sys.exit()

            else:
                print('[.] VPN is off!')
                print('[%] Done!')

    @staticmethod
    def get_status():
        check_vpn()


def main(start=start, stop=stop, status=status):
    print '{}\n'.format(banner)
    print('[*] Emmanuel Hernandez\n\n')
    check_root()
    pia = Pia(start)
    if start:
        pia.vpn_start()
    elif stop:
        pia.vpn_stop()
    elif status:
        pia.get_status()
    else:
        print('[.] Please provide a flag')
        print(parser.print_help())


if __name__ == '__main__':
    main(start=start, stop=stop, status=status)
