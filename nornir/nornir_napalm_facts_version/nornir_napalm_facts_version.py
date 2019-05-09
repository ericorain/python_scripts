#!/usr/bin/env python3

# Import Python library
from nornir import InitNornir
from nornir.plugins.functions.text import print_title
from nornir.plugins.tasks import networking


# Main function
def main():

    # Get information from inventory files
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


    # Select only the network devices
    hosts = nr.filter(type="network_device")

    # Get facts
    result = hosts.run(task=networking.napalm_get, name=" Get facts ", getters=["facts"])

    # Get the first key (the one of the first host)
    key1 = list(result)[0]

    # Get values for the first key (first host)
    values1 = result[key1][0]

    # Get host name
    myhost = values1.result["facts"]["hostname"]

    # Get os version
    hostversion = values1.result["facts"]["os_version"]

    # Display a title
    print_title("Display network devices os version")

    # Print result
    print("host: [", myhost, "] version :\n", hostversion)


# Main function call
if __name__ == '__main__':
    main()