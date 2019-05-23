# pyATS

All in all this framework is easy to use. I like it. Too bad it is only for Cisco devices.

**What I like**:
* Easy to retrieve information and to send commands
* Execution time is ok
* Sending configuration is easy

**What I do not like with this framework**:
* Only for Cisco devices
* The hostname must match with device name in the yaml file
* Display unecessary information on the screen while running a command


---

**Installation**:

```
pip install pyats
```

First thing to do is to create a testbed.yaml file that will contain the IP address, login, etc. of the devices. The name of the devices (here "R1" and "R2") **MUST** be the same as the hostname of the devices.

```
testbed:
    name: My_Testbed

devices:
    R1:
        os: ios
        type: ios
        tacacs:
            username: cisco
        passwords:
            tacacs: cisco
        connections:
            tacacs:
                protocol: ssh
                ip: 192.168.0.100
                port: 22
    R2:
        os: ios
        type: ios
        tacacs:
            username: cisco
        passwords:
            tacacs: cisco
        connections:
            tacacs:
                protocol: ssh
                ip: 192.168.0.101
                port: 22
```

1 - "show ip int brief"

Next an example to read data from a Cisco device:

```

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

```

The result:

```

(project1) [eorain@centos7 pyats]$ ./pyats_show_ip_int_brief.py
[2019-05-23 07:18:57,985] +++ R2 logfile /tmp/R2-default-20190523T071857983.log +++
[2019-05-23 07:18:57,986] +++ Unicon plugin ios +++
[2019-05-23 07:18:57,992] +++ connection to spawn: ssh -l cisco 192.168.0.101 -p 22, id: 140479944164856 +++
[2019-05-23 07:18:57,994] connection to R2
Password:

R2#
[2019-05-23 07:18:59,533] +++ initializing handle +++
[2019-05-23 07:18:59,534] +++ R2: executing command 'term length 0' +++
term length 0
R2#
[2019-05-23 07:18:59,616] +++ R2: executing command 'term width 0' +++
term width 0
R2#
[2019-05-23 07:18:59,658] +++ R2: executing command 'show version' +++
show version
```
*[...* *Removed* *...]*
```
Configuration register is 0x2102

R2#
[2019-05-23 07:18:59,756] +++ R2: config +++
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#no logging console
R2(config)#line console 0
R2(config-line)#exec-timeout 0
R2(config-line)#end
R2#
[2019-05-23 07:19:00,111] +++ R2: executing command 'show ip int brief' +++
show ip int brief
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        unassigned      YES NVRAM  administratively down down
FastEthernet1/0        unassigned      YES NVRAM  administratively down down
Ethernet2/0            unassigned      YES NVRAM  administratively down down
Ethernet2/1            192.168.0.101   YES NVRAM  up                    up
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
R2#
Interface              IP-Address      OK? Method Status                Protocol
FastEthernet0/0        unassigned      YES NVRAM  administratively down down
FastEthernet1/0        unassigned      YES NVRAM  administratively down down
Ethernet2/0            unassigned      YES NVRAM  administratively down down
Ethernet2/1            192.168.0.101   YES NVRAM  up                    up
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
(project1) [eorain@centos7 pyats]$

```

As we can see the code is very simple. The annoying issue is that thera are several commands displayed that are no use for the program such as a information text, configuration commands while doing a simple show command (!), "show version" is always displayed on the screen while it is not wanted and "show ip int brief" the command itself is diplayed on the screen twice.

2 - Configuratio on an interface

Let's send a list of commands to configure a Cisco interface:

>        interface Ethernet2/0
>            ip address 198.168.1.2 255.255.255.0
>            no shut

The second device ("R2") will get an interface configured. Here is the source code in pyATS:

```
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
```

The result:

```
(project1) [eorain@centos7 pyats]$ ./pyats_config_interface.py
[2019-05-23 07:34:35,503] +++ R2 logfile /tmp/R2-default-20190523T073435502.log +++
[2019-05-23 07:34:35,504] +++ Unicon plugin ios +++
[2019-05-23 07:34:35,512] +++ connection to spawn: ssh -l cisco 192.168.0.101 -p 22, id: 140204566378032 +++
[2019-05-23 07:34:35,514] connection to R2
Password:

R2#
[2019-05-23 07:34:36,919] +++ initializing handle +++
[2019-05-23 07:34:36,921] +++ R2: executing command 'term length 0' +++
term length 0
R2#
[2019-05-23 07:34:36,959] +++ R2: executing command 'term width 0' +++
term width 0
R2#
[2019-05-23 07:34:37,008] +++ R2: executing command 'show version' +++
show version
```
*[...* *Removed* *...]*
```
Configuration register is 0x2102

R2#
[2019-05-23 07:34:37,062] +++ R2: config +++
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#no logging console
R2(config)#line console 0
R2(config-line)#exec-timeout 0
R2(config-line)#end
R2#
[2019-05-23 07:34:37,264] +++ R2: config +++
config term
Enter configuration commands, one per line.  End with CNTL/Z.
R2(config)#
R2(config)#        interface Ethernet2/0
R2(config-if)#            ip address 198.168.1.2 255.255.255.0
R2(config-if)#            no shut
R2(config-if)#
R2(config-if)#end
R2#
Command send:

        interface Ethernet2/0
            ip address 198.168.1.2 255.255.255.0
            no shut


(project1) [eorain@centos7 pyats]$
```

Again unecessary text is displayed. But sending configuration to a Cisco device is quite easy with pyATS.
