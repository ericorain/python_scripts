#!/usr/bin/env python3

# Import Python library
from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command

# Main function
def main():

    # Cisco IOS device parameters
    h = {'device1': {'hostname': '192.168.0.100','port': 22,'username': 'cisco','password': 'cisco','platform': 'cisco_ios'}}
    g = {}
    d = {}

    # Initialization of the Nornir element
    r = InitNornir(inventory={"plugin": "nornir.plugins.inventory.simple.SimpleInventory","options": {"hosts": h, "groups": g, "defaults": d, }})
    
    # Command sent using Netmiko
    result = r.run(task=netmiko_send_command,command_string="show arp")

    # Display the result
    print(result['device1'][0])

# Main function call
if __name__ == '__main__':
    main()