#!/usr/bin/env python3

# Import Python library
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_cli

# Main function
def main():

    # Device parameters
    h = {'my_device': {'hostname': '192.168.0.100','port': 22,'username': 'cisco','password': 'cisco','platform': 'ios'}}
    g = {}
    d = {}

    # Initialization of the Nornir object
    nr = InitNornir(inventory={"plugin": "nornir.plugins.inventory.simple.SimpleInventory","options": {"hosts": h, "groups": g, "defaults": d}})

    # Command to send to the device
    my_cli_command = "show version"

    # Runnning the CLI command
    result = nr.run(task=napalm_cli,commands=[my_cli_command])

    # Display result
    print(result["my_device"][0].result.get(my_cli_command))

# Main function call
if __name__ == '__main__':
    main()