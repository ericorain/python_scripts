# Dandy

Dandy is a python script that sends a group a CLI reading commands to network devices. It does not require programing language knowledge.

The script has not been designed to write configuration into devices (like "conf t" mode commands for Cisco devices); it has just been written for reading commands on network devices (like "show" commands for Cisco/Juniper/etc. devices).

The input data is actually a single csv file called "device.csv". The output is printed out on the screen and/or stored into a csv file.

---

## Compatibility

Dandy requires python 3.8.2 and the following python libraries:
- nornir 2.4.0 
- netmiko 3.0.0

It works on Windows 10 and Linux.

---

## Command line usage

### 1 - Running the script

Running the script is easy: just type the name of the script. Do not forget to fill the "device.csv" file before running the script.

>dandy.py

### 2 - Available options

Here are the available options for the software:
``` bash
C:\>dandy.py -h
Usage: dandy [-g] [-h] [-q] [-v] [-w [output]]

Options:
  -g            Generate "device.csv" file. Warning: overwrite existing file
  -h            Help
  -q            Quiet mode. Results are not displayed
  -s            Semicolon csv files are used. Comma csv file are used by default
  -v            Version
  -w [output]   Write csv output file. "output" is the name of the file and is optional. Default filename: "output.csv"
```

### 3 - Result

---

Below is an exemple of result you can get with that script. Please note that the parameter "-w" is not mandatory and creates a csv output file called "output.csv".

``` bat
C:\>dandy.py -w
[+] Reading csv file (device.csv)...
[+] csv file read. [ OK ]
[+] Running commands on devices...
SERVER2                         [ OK ]
SERVER1                         [ OK ]
[+] Results of the commands on devices:
SERVER1 ************************************************************************
--- whoami
root
--- wc /etc/hosts
        2         4        39 /etc/hosts
--- date
Sun Mar 15 19:33:08 CET 2020
SERVER2 ************************************************************************
--- whoami
root
--- wc /etc/hosts
        2         4        39 /etc/hosts
--- echo 123
123
[+] Saving results into csv file (output.csv)...
[+] csv file writting successfully. [ OK ]

C:\>
```

---

## "device.csv" csv file (input)

"device.csv" contains the list of the devices and the list of the commands to send to the devices. This file is mandatory. Comma (',') is the default delimiter for this file even though semicolon (';') can be used with "-s" command-line argument.

### 1 - The csv header

The header of the csv file is the following:

> hostname,ip,login,password,platform,commands

### 2 - The csv data

Data under each column of the header must match with the followin rules:

| header column  | Comments |
| -------------- | -------- |
| hostname       | This is the reference of the device. That name must be unique |
| ip             | IP address of the device |
| login          | Login used to access the device |
| password       | Password used to access the device |
| platform<BR><BR><BR><BR><BR><BR><BR><BR>| Specify the type of device that will receive the commands.<BR>"platform" accepts the following values:<BR>cisco_ios<BR>cisco_xe<BR>cisco_nxos<BR>juniper_junos<BR>linux |
| commands       | Command or list of commands to be sent to the devices |

Note:<BR>Other values should be working within "platform" column (like "aruba_os", "fortinet", "huawei" or "paloalto_panos"), but it has not been tested. The list of supported devices is available in the "CLASS_MAPPER_BASE" of "ssh_dispatcher.py" file of Netmiko library.


### 3 - Examples of "device.csv"

Here are some examples of "device.csv" csv file. The content is displayed for understanding how is made the csv file. It is easier of course to just use your favorite spreadsheet software (MS Excel, LibreOffice Calc, etc.) and fill the data.

Example 1: 1 command for 1 device
``` csv
hostname,ip,login,password,platform,commands
Switch01,192.168.0.1,cisco,cisco,cisco_ios,show arp
```
Example 2 : 1 command for several devices
``` csv
hostname,ip,login,password,platform,commands
Switch01,192.168.0.1,cisco,cisco,cisco_ios,show arp
Switch02,192.168.0.2,junos,junos,juniper_junos,show arp
Switch03,192.168.0.3,cisco,cisco,cisco_ios,show clock
```

Example 3 : several commands for several devices
``` csv
hostname,ip,login,password,platform,commands
Switch01,192.168.0.1,cisco,cisco,cisco_ios,"show inventory
show ip int brief"
Switch02,192.168.0.2,junos,junos,juniper_junos,show arp
Server01,192.168.0.3,root,password,linux,"whoami
pwd
echo 123"
```

Note:<BR>Juniper switches needs to get the whole command typed (i.e "show version" and not "sh ver") otherwise the result of the command may have part of the mission letters of the command (not a big deal though).


## "output.csv" csv file (output)

Using "-w" you can create a csv file with the output of the command.

Here is an example of what "output.csv" content could be after running the script:

**"device.csv" (input)**
```
hostname,ip,login,password,platform,commands
SERVER1,192.168.0.1,root,password,linux,"whoami
wc /etc/hosts
date"
SERVER2,192.168.0.2,root,password,linux,"whoami
wc /etc/hosts
echo 123"
```

**"output.csv" (output)**
```
Device,CMD1,CMD2,CMD3
SERVER1,root,        2         4        39 /etc/hosts,Mon Mar 16 08:01:34 CET 2020
SERVER2,root,        2         4        39 /etc/hosts,123
```

---

## Thanks

Thanks go to:
- David Barroso and all the Nornir Team
- Kirk Byers for Netmiko library
- Pascal Marcou and Daniel Jouannic (Orange France) for ideas and advices