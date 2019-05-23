#!/usr/bin/env python3

# Import Python library
from pyats.topology import loader

# Main function
def main():

    # Read the testbed.yaml file with the conection parameters (login, passwords, etc.)
    pyats_testbed = loader.load("testbed.yaml")

    # Select a device with its name
    ios1 = pyats_testbed.devices["R2"]

    # Connect to the device
    ios1.connect()

    # Run the command
    output = ios1.configure('''
        interface Ethernet2/0
            ip address 198.168.1.2 255.255.255.0
            no shut
    ''')

    # Display command output
    print("Command send:\n", output)

# Main function call
if __name__ == '__main__':
    main()