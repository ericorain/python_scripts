#!/usr/bin/env python3

# Import Python library
import networkscan

# Main function
if __name__ == '__main__':

    # Define the network to scan
    my_network = "192.168.0.0/24"

    # Create the object
    my_scan = networkscan.Networkscan(my_network)

    # Display information
    print("Network to scan: " + str(my_scan.network))
    print("Prefix to scan: " + str(my_scan.network.prefixlen))
    print("Number of hosts to scan: " + str(my_scan.nbr_host))

    # Run the network scan
    print("Scanning hosts...")

    # Run the scan of hosts using pings
    my_scan.run()

    # Display information
    print("List of hosts found:")

    # Display the IP address of all the hosts found
    for i in my_scan.list_of_hosts_found:
        print(i)

    # Display information
    print("Number of hosts found: " + str(my_scan.nbr_host_found))

    # Write the file on disk
    res = my_scan.write_file()

    # Error while writting the file?
    if res:
        # Yes
        print("Write error with file " + my_scan.filename)

    else:
        # No error
        print("Data saved into file " + my_scan.filename)
