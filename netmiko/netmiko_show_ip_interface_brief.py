#!/usr/bin/env python3

# Import Python library
import sys
from netmiko import ConnectHandler

my_device = {
    'device_type': 'cisco_ios',
    'ip':   '192.168.0.100',
    'username': 'cisco',
    'password': 'cisco',
    'port' : 22
}

# Main function
def my_netmiko_command(ip_param, login_param, password_param, port_param):

    # Gathering parameters
    my_device['ip'] = ip_param
    my_device['username'] = login_param
    my_device['password'] = password_param
    my_device['port'] = port_param

    # Connexion to the device
    net_connect = ConnectHandler(**my_device)

    # Sending command
    output = net_connect.send_command("show ip interface brief")

    # Display the output
    print(output)

# Main function call
if __name__ == '__main__':


    # Input parameters:
    # ip address, login, password, port (optional)
    #
    # Example:
    #
    # script 192.168.0.1 cisco cisco

    # Enough parameters?
    if (len(sys.argv) < 4):

        # No
        sys.exit("Not enough parameters to run the command")

    # Optional port argument in command line ?
    if (len(sys.argv) > 4):

        # Yes
        tcp_port = sys.argv[4]

    else:

        # No

        # Default port TCP 22
        tcp_port = 22


    # Run the function
    my_netmiko_command(sys.argv[1], sys.argv[2], sys.argv[3], tcp_port)