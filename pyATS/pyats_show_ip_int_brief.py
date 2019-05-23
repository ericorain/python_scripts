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
    output = ios1.execute('show ip int brief')

    # Display command output
    print(output)

# Main function call
if __name__ == '__main__':
    main()