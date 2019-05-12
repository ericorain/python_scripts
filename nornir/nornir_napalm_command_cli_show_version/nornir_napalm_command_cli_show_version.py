#!/usr/bin/env python3

# Import Python library
from nornir import InitNornir
from nornir.plugins.tasks.networking import napalm_cli


# Main function
def main():

    # Initialization of the Nornir object
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

    # Command to send to the device
    my_cli_command = "show version"


    hosts = nr.filter(type="network_device")

    # Runnning the CLI command
    result = hosts.run(task=napalm_cli,commands=[my_cli_command])

    # Display result
    print(result["device1"][0].result.get(my_cli_command))

# Main function call
if __name__ == '__main__':
    main()