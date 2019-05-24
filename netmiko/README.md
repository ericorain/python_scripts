# Netmiko

A bunch of examples using netmiko

**Example of script: netmiko_show_ip_interface_brief.py**

```
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
```

**Usage:**

```
python netmiko_show_ip_interface_brief.py 192.168.0.100 cisco cisco
```


**Result:**

```
d:\>python netmiko_show_ip_interface_brief.py 192.168.0.100 cisco cisco
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        unassigned      YES NVRAM  administratively down down
FastEthernet1/0        unassigned      YES NVRAM  administratively down down
Ethernet2/0            unassigned      YES NVRAM  administratively down down
Ethernet2/1            192.168.0.100   YES NVRAM  up                    up
Ethernet2/2            unassigned      YES NVRAM  administratively down down
Ethernet2/3            unassigned      YES NVRAM  administratively down down
Ethernet3/0            unassigned      YES NVRAM  administratively down down
Ethernet3/1            unassigned      YES NVRAM  administratively down down
Ethernet3/2            unassigned      YES NVRAM  administratively down down
Ethernet3/3            unassigned      YES NVRAM  administratively down down
Ethernet3/4            unassigned      YES NVRAM  administratively down down
Ethernet3/5            unassigned      YES NVRAM  administratively down down
Ethernet3/6            unassigned      YES NVRAM  administratively down down
Ethernet3/7            unassigned      YES NVRAM  administratively down down

d:\>
```

