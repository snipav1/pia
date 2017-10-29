# pia
Easy to use OpenVPN CLI


Setup:

    sudo pip install -r requirements.txt


Usage:

    - Connect using .ovpn conf file
    sudo ./pia.py --start=SiliconValley.ovpn

    - Stop ovpn process and verify vpn is off (Fill in ISP provider line #72)
    sudo ./pia.py --stop

    - Check if vpn is on (Fill in ISP provider in ip.py file on line #30)
    sudo ./pia.py --status
    
Optional:

Very useful if bash aliases are created
    
Modify .bashrc file with something like these Examples:
    
    alias pia-start-siliconvalley='sudo python /<path>/pia.py --start=SiliconValley.ovpn'
    alias pia-stop='sudo python /<path>/pia.py --stop'
    alias pia-status='sudo python /<path>/pia.py --status'
