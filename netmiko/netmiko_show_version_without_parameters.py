#!/usr/bin/env python3

# Import Python library
import sys
from netmiko import ConnectHandler

my_device = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.0.100',
    'username': 'cisco',
    'password': 'cisco',
    'port' : 22
}

# Main function
def main():

    # Connexion to the device
    net_connect = ConnectHandler(**my_device)

    # Sending command
    output = net_connect.send_command("show version")

    # Display the output
    print(output)

# Main function call
if __name__ == '__main__':
    main()