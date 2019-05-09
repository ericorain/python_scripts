#!/usr/bin/env python3

# Import Python library
from nornir import InitNornir
from nornir.plugins.functions.text import print_title, print_result
from nornir.plugins.tasks import networking


# Main function
def main():


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



    hosts = nr.filter(type="network_device")

    result = hosts.run(task=networking.napalm_get,name=" Get facts ",getters=["facts", "interfaces", "environment"])

    print_title("Display info about network devices")
    print_result(result)

    print(result["device1"][0].result.get("facts").get("os_version"))

# Main function call
if __name__ == '__main__':
    main()