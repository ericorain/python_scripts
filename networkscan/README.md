# Networkscan

Networkscan is a fast host scanner written in python. It can be used in command line or as a python library.

The advantages of that program are:
- it can perform fast pings (thanks to the use of coroutines)
- it can be used as a command line program or as a python library
- it can create a list of IP address hosts as a output for easy IP address manipulation
- it can create a yaml host inventory compatible with Nornir

---

## Compatibility

Networkscan requires python 3 and the following python libraries:
- asyncio 
- ipaddress
- platform
- subprocess
- sys

It works on Windows and Linux.

---

## Installation

*To be completed*

---

## Command line usage

### 1 - Available options

Here are the available options for the software:
``` bash
(project1) [eorain@centos7 python]$ ./networkscan.py

Usage: networkscan.py network_to_scan [-h] [-q] [-m] [-w [hosts.yaml]]

Options :
    network_to_scan      The network or IP address to scan using fast pings.
                         Examples: "192.168.0.0/24", "10.0.0.1", "172.16.1.128/28", etc.
    -h                   Help
    -m                   Mute mode (nothing is displayed on screen)
    -q                   Quiet mode (just the list of hosts found is displayed)
    -w [hosts.yaml]      Write a yaml host file with an optional filename (default name is hosts.yaml)

(project1) [eorain@centos7 python]$
```

### 2 - How to scan a /24 network

> networkscan.py 192.168.0.0/24

``` bash
(project1) [eorain@centos7 python]$ ./networkscan.py 192.168.0.0/24
Network to scan: 192.168.0.0/24
Prefix to scan: 24
Number of hosts to scan: 254
Scanning hosts...
List of hosts found:
192.168.0.10
192.168.0.11
192.168.0.12
192.168.0.100
192.168.0.101
192.168.0.111
192.168.0.1
Number of hosts found: 7
(project1) [eorain@centos7 python]$
```

### 3 - How to scan a /28 network displaying just the name of the hosts (quiet mode)

> networkscan.py 192.168.0.0/28 -q

``` bash
(project1) [eorain@centos7 python]$ ./networkscan.py 192.168.0.0/28 -q
192.168.0.1
192.168.0.10
192.168.0.11
192.168.0.12
(project1) [eorain@centos7 python]$
```

### 4 - How to scan a /25 network then to save the list of hosts into a text file (quiet mode and redirection of the output into a file)

> networkscan.py 192.168.0.0/25 -q >inventory.txt

``` bash
(project1) [eorain@centos7 python]$ ./networkscan.py 192.168.0.0/25 -q >inventory.txt
(project1) [eorain@centos7 python]$
(project1) [eorain@centos7 python]$ cat inventory.txt
192.168.0.100
192.168.0.101
192.168.0.111
192.168.0.1
192.168.0.10
192.168.0.11
192.168.0.12
(project1) [eorain@centos7 python]$
```

### 4 - How to scan a /23 network then save the list of hosts into a yaml file compatible with Nornir syntax (mute mode and creation of a yaml file)

---

Please note that when no file is specified with the parameter "-w" then a "hosts.yaml" file is created by default. With the command "networkscan.py 192.168.0.0/23 -m -w foo.yaml" you do create a file named "foo.yaml".

---

> networkscan.py 192.168.0.0/23 -m -w

``` bash
(project1) [eorain@centos7 python]$ ./networkscan.py 192.168.0.0/23 -m -w
(project1) [eorain@centos7 python]$ ls hos*
hosts.yaml
(project1) [eorain@centos7 python]$
```

**hosts.yaml:**

``` yaml
---
device1:
    hostname: 192.168.0.1
    groups:
        - device_discovered

device2:
    hostname: 192.168.0.100
    groups:
        - device_discovered

device3:
    hostname: 192.168.0.101
    groups:
        - device_discovered

device4:
    hostname: 192.168.0.10
    groups:
        - device_discovered

device5:
    hostname: 192.168.0.11
    groups:
        - device_discovered

device6:
    hostname: 192.168.0.12
    groups:
        - device_discovered

device7:
    hostname: 192.168.0.111
    groups:
        - device_discovered

```

---

## Python library usage

### 1 - A simple script

The following script just scan a network then displays the list of host found.

**python script:**
``` python
#!/usr/bin/env python3

# Import Python library
import networkscan

# Main function
if __name__ == '__main__':

    # Define the network to scan
    my_network = "192.168.0.0/24"

    # Create the object
    my_scan = networkscan.Networkscan(my_network)

    # Run the scan of hosts using pings
    my_scan.run()

    # Display the IP address of all the hosts found
    for i in my_scan.list_of_hosts_found:
        print(i)

```

**output:**
```
192.168.0.100
192.168.0.101
192.168.0.111
192.168.0.1
192.168.0.10
192.168.0.11
192.168.0.12
```

### 2 - An advanced script

This script scan a network then it creates a yaml file with the list of hosts found.

write_file() method accepts two optional parameters: 

``` python
    def write_file(self, file_type = 0, filename = "hosts.yaml"):
        """ Method to write a file with the list of the detected hosts """

        # Input:
        #
        # - file_type (integer, optional): 0, Nornir file (default value)
        #                                  1, Text file as output file
        # - filename (string, optional): the name of the file to be written ("hosts.yaml" is the default value)
        #
        # Ouput:
        # A text file with the list of detected hosts ("hosts.yaml" is the default value)
        # return 0 if no error occured
```

**python script:**
``` python
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

```

---

## Performance

Here are the results I had with a single process with 1 second timeout ping using asyncio and without asyncio.


Number of hosts | 1 | 2 | 2 | 6 | 14 | 30 | 62 | 126 | 254 | 510 | 1022
| :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | :------------ | 
Network | /32 | /31 | /30 | /29 | /28 | /27 | /26 | /25 | /24 | /23 | /22
Networkscan (sec) | 0,184 | 1,178 | 1,163 | 1,213 | 1,232 | 1,411 | 1,951 | 2,23 | 5,104 | 7,055 | 18,196
Without asyncio (timeout 1 sec) | N/A | 1,136 | 1,115 | 5,485 | 10,194 | 26,852 | 67,258 | 130,334 | 253,168 | 321,908 | 865,858



## What's next with my Nornir yaml file?

When you scan a network you entered that command and get the folling output:

``` bash
(project1) [eorain@centos7 python]$ ./networkscan.py 192.168.0.96/28 -w
Network to scan: 192.168.0.96/28
Prefix to scan: 28
Number of hosts to scan: 14
Scanning hosts...
List of hosts found:
192.168.0.100
192.168.0.101
Number of hosts found: 2
Writting file
Data saved into file hosts.yaml
(project1) [eorain@centos7 python]$
 ```

The file hosts.yaml is created.

**hosts.yaml**
``` yaml
---
---
device1:
    hostname: 192.168.0.100
    groups:
        - device_discovered

device2:
    hostname: 192.168.0.101
    groups:
        - device_discovered

 ```

After scanning your network and creating a Nornir inventory file ("hosts.yaml") you might wonder what to do next. You can notice that the "hosts.yaml"  does not include the password, login and platform.

There are two cases:
- either all the devices are different devices with eventually different credentials
- or they are from the same type and have the credentials

### a) Different devices

In the first case you will have to fill the login, password and platform reference on all the devices. 3 fields are added:
- username
- password
- platform

Here is an example:

**hosts.yaml**
``` yaml
---
device1:
    hostname: 192.168.0.100
    username: cisco
    password: cisco
    platform: ios
    groups:
        - device_discovered

device2:
    hostname: 192.168.0.101
    username: juni
    password: per
    platform: junos
    groups:
        - device_discovered

 ```

### b) Same devices and same credentials

If you are in this situation things are easier. You probably noticed that all the devices belongs to the "device_discovered" group. You can create a group file with a reference to that group then to add the missing value to the group file (without change on the "hosts.yaml" file).

Here is an example with Cisco IOS equipements:

**groups.yaml**
``` yaml
---
device_discovered:
    username: cisco
    password: cisco
    platform: ios
```

### c) Ready to use Nornir

If you are done with a) or b) now you are ready to write your code with Nornir. It is better to put your yaml files into a folder (here "inventory" folder).

Just copy the content of the "nornir_arp.py" into a file.

**nornir_arp.py**

``` python
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
```

You should get that file structure:
``` bash
|--- nornir_arp.py
|--- inventory
|    --- groups.yaml
|    --- hosts.yaml
|
```

You can then run the program.

``` bash
(project1) [eorain@centos7 python]$ ./nornir_arp.py
**** Display ARP table of the network devices **********************************
 ARP table *********************************************************************
* device1 ** changed : False ***************************************************
vvvv  ARP table  ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'arp_table': [ { 'age': 2.0,
                   'interface': 'Ethernet2/0',
                   'ip': '192.168.0.1',
                   'mac': 'AC:74:99:B3:27:EF'},
                 { 'age': 10.0,
                   'interface': 'Ethernet2/0',
                   'ip': '192.168.0.11',
                   'mac': '8A:78:01:80:87:DD'},
                 { 'age': 0.0,
                   'interface': 'Ethernet2/0',
                   'ip': '192.168.0.100',
                   'mac': '8A:FF:18:CC:00:48'}]}
^^^^ END  ARP table  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* device2 ** changed : False ***************************************************
vvvv  ARP table  ** changed : False vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv INFO
{ 'arp_table': [ { 'age': 2.0,
                   'interface': 'Ethernet2/0',
                   'ip': '192.168.0.1',
                   'mac': 'AC:74:99:B3:27:EF'},
                 { 'age': 10.0,
                   'interface': 'Ethernet2/0',
                   'ip': '192.168.0.11',
                   'mac': '8A:78:01:80:87:DD'},
                 { 'age': 0.0,
                   'interface': 'Ethernet2/0',
                   'ip': '192.168.0.101',
                   'mac': '88:78:44:0A:DE:13'},
                 { 'age': 0.0,
                   'interface': 'Ethernet2/2',
                   'ip': '192.168.255.1',
                   'mac': '88:78:44:0A:DE:19'}]}
^^^^ END  ARP table  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
(project1) [eorain@centos7 python]$
```



