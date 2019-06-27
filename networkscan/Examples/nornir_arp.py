#!/usr/bin/env python3

# Import Python library
from nornir import InitNornir
from nornir.plugins.functions.text import print_title, print_result
from nornir.plugins.tasks import networking


# Main function
def main():

    # Create a Nornir object
    nr = InitNornir(
        core={"num_workers": 100},
        inventory={
            "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
            "options": {
                "host_file": "inventory/hosts.yaml",
                "group_file": "inventory/groups.yaml"
            }
        }
    )

    # Run Nornir task (here getting the ARP table of the devices)
    result = nr.run(task=networking.napalm_get,name=" ARP table ",getters=["arp_table"])

    # Display the result
    print_title("Display ARP table of the network devices")
    print_result(result)


# Main function call
if __name__ == '__main__':
    main()