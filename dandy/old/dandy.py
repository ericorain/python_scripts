#!/usr/bin/env python3

# Python library import
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
import sys,os,csv

from nornir.plugins.functions.text import print_title, print_result


# Declaration of constant values

# csv filename
csv_file = "device.csv"

# txt filename
txt_file = "commands.txt"

# Text color
COLOR_OK = '\033[92m'
COLOR_FAIL = '\033[91m'
COLOR_ENDC = '\033[0m'
COLOR_DEVICE = '\033[0;36;40m'
COLOR_CMD = '\033[0;35;40m'




# Reading csv file function
def read_csv(csv_full_path, csv_filename):

    try:

        # Display message
        print("[+] Reading csv file (" + str(csv_filename) + ")...")


        # Open the file
        with open(csv_full_path) as csv_file:

            # Initilization of the dictionary
            dict_data = {}

            # Read the header and specify the delimiter
            csv_reader = csv.reader(csv_file, delimiter=';')

            # Specify if the first line is read (default = 1 = yes)
            first_line = 1
            
            # Read line by line the content of the csv file
            for row in csv_reader:

                # First line (the headers)?
                if first_line == 1:
                    
                    # Yes

                    # Nothing to do except specifying next line will not be the fiirst one any longer
                    first_line = 0
                    
                else:

                    # Not the first line

                    # Save the content of the csv line into a dictionary
                    # Here is an example of one line of that dictionary:
                    # {'my_device': {'hostname': '192.168.0.15','port': 22,'username': 'root','password': 'linux','platform': 'linux'}}
                    #dict = {str(row[0]): {'hostname': str(row[1]),'port': 22,'username': str(row[2]),'password': str(row[3]),'platform': str(row[4])}}
                    dict_data[str(row[0])] = {'hostname': str(row[1]),'port': 22,'username': str(row[2]),'password': str(row[3]),'platform': str(row[4])}
                    

                    # Then add the dictionary to the list
                    #list_of_data.append(dict)

    except Exception as e:

        # Error

        # Display message
        print("[+] Error while reading csv file " + str(csv_filename) + " [ " + COLOR_FAIL + "FAIL" + COLOR_ENDC + " ]\n" + str(e))

        # Exit program
        sys.exit(1)

    # Display message
    print("[+] csv file read. [ " + COLOR_OK + "OK" + COLOR_ENDC + " ]")
    
    # Return a dictionary with the data
    return dict_data


# Reading txt file function
def read_txt(txt_full_path, txt_filename):

    try:

        # Display message
        print("[+] Reading txt file (" + str(txt_filename) + ")...")

        # Open the file
        with open(txt_full_path) as txt_file:

            # Read the content and store the result into a list
            #list_of_commands = txt_file.readlines()
            list_of_commands = txt_file.read().splitlines()

    except Exception as e:

        # Error

        # Display message
        print("[+] Error while reading txt file " + str(txt_filename) + " [ " + COLOR_FAIL + "FAIL" + COLOR_ENDC + " ]\n" + str(e))

        # Exit program
        sys.exit(1)
    
    # Display message
    print("[+] txt file read. [ " + COLOR_OK + "OK" + COLOR_ENDC + " ]")

    # Return a dictionary with the data
    return list_of_commands


# nornir group of tasks function
def nornir_group_of_tasks(task, list_of_commands):
    
    #i = 1

    # Display device name
    print(str(task.host) + " ...", end = '')

    # Run each command on a device one by one
    for cmd in list_of_commands:
        task.run(task=netmiko_send_command,command_string=cmd)

        #print(i)
        #i = i + 1

    # Display message
    print("\t[ " + COLOR_OK + "OK" + COLOR_ENDC + " ]")


# Main function
def main(dict_of_devices, list_of_commands):

    # Device parameters
    #h = {'my_device': {'hostname': '192.168.0.15','port': 22,'username': 'root','password': 'linux','platform': 'linux'}}
    h = dict_of_devices
    g = {}
    d = {}

    # Initialization of the Nornir object
    nr = InitNornir(inventory={"plugin": "nornir.plugins.inventory.simple.SimpleInventory","options": {"hosts": h, "groups": g, "defaults": d}})

    # Command to send to the device
    #my_cli_command = "uname -a"
    #list_of_commands = ["uname -a","pwd"]

    # Display message
    print("[+] Running commands on devices...") 


    # Runnning the commands with nornir
    result = nr.run(task=nornir_group_of_tasks, list_of_commands=list_of_commands)

    # Display message
    print("[+] Results of the commands on devices:") 
    
    # Display the results
    for device in result:

        # Get device name
        device_name = str(result[device][0].host)

        # Display device name
        print(COLOR_DEVICE + device_name + " " + '*' * (79 - len(device_name)) + COLOR_ENDC)

        # Get each command the appropriated result in a loop
        for cmd,res in zip(list_of_commands,result[device][1:]):

            # Display the command
            print(COLOR_CMD + "--- " + str(cmd) + COLOR_ENDC)

            # Display the result of that command
            print(str(res))



# Main function call
if __name__ == '__main__':

    # Get path of the script
    script_path = sys.path[0]
    #print(script_path)


    # Path of the csv file in the same directory as the script
    csv_full_path = os.path.join(script_path, csv_file)
    

    #print(csv_full_path)

    # Read csv file
    dict_of_devices = read_csv(csv_full_path, csv_file)

    '''
    for element in dict_of_devices:
        print(element)
    '''

    # Path of the csv file in the same directory as the script
    txt_full_path = os.path.join(script_path, txt_file)

    # Read csv file
    list_of_commands = read_txt(txt_full_path, txt_file)

    '''
    for element in list_of_commands:
        print(element)
    '''


    # Run main function
    main(dict_of_devices, list_of_commands)

