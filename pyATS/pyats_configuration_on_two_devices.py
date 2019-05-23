#!/usr/bin/env python3

# Import Python library
from pyats.topology import loader

# Main function
def main():

    # Read the testbed.yaml file with the conection parameters (login, passwords, etc.)
    pyats_testbed = loader.load("testbed.yaml")

    # Device selection using hostname parameter
    ios1 = pyats_testbed.devices["R1"]
    ios2 = pyats_testbed.devices["R2"]

    # Connection
    ios1.connect()
    ios2.connect()

    # Run the command
    ios1.configure('''
        interface Ethernet2/0
            ip address 198.168.1.1 255.255.255.0
            no shut
    ''')

    ios2.configure('''
        interface Ethernet2/0
            ip address 198.168.1.2 255.255.255.0
            no shut
    ''')


# Main function call
if __name__ == '__main__':
    main()