#!/usr/bin/env python3

# Python library import
from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
import sys,os,csv
import threading

# Declaration of constant values

# Version
VERSION = "1.0"

# csv filename
csv_file = "device.csv"

# txt filename
txt_file = "command.txt"

# default output csv filename
default_output_csv_file = "output.csv"


# Text color
COLOR_OK = '\033[92m'
COLOR_FAIL = '\033[91m'
COLOR_ENDC = '\033[0m'
COLOR_BLUE = '\033[96m'
COLOR_PINK = '\033[95m'


# Declaration of global variables

# Shared variable to lock printing output inside Nornir task (thread)
lock = threading.Lock()

# Function used to calculate the maximum number of commands sent per device then create a list with csv header names
def get_csv_header_command(result):

    # By default the number of commands is null
    max_number_of_commands = 0

    # Read each device result
    for device in result:

        #print(device)

        # By default the current device number of commands is null
        current_number_of_commands = 0

        # Read all commands of the device
        for _ in result[device][1:]:

            # For every command the current device number of commands is increased
            current_number_of_commands += 1

        # Is the current device number of commands is higher than the maximum number of commands so far?
        if current_number_of_commands > max_number_of_commands:

            # Yes

            # So that is the new maximum of commands found on all of the devices
            max_number_of_commands = current_number_of_commands


    #print(max_number_of_commands)

    # By default the list of csv header names is empty
    list_output = []

    # Add csv header names as much as the maximum number of commands found (i.e 4 commands founds = 4 command csv headers)
    for i in range(1,max_number_of_commands+1):
        list_output.append("CMD" + str(i))

    # Return a list with the csv header names
    return list_output




# Reading csv file function
def read_csv(csv_full_path, csv_filename):

    try:

        # Display message
        print("[+] Reading csv file (" + str(csv_filename) + ")...")


        # Open the file
        with open(csv_full_path) as csv_file:

            # Initilization of the dictionary
            dict_devices = {}

            # Initilization of the dictionary of the commands
            dict_commands = {}

            # Read the header and specify the delimiter
            csv_reader = csv.reader(csv_file, delimiter=',')

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
                    # {'my_device': {'hostname': '192.168.0.1','port': 22,'username': 'cisco','password': 'cisco','platform': 'cisco_ios'}}
                    dict_devices[str(row[0])] = {'hostname': str(row[1]),'port': 22,'username': str(row[2]),'password': str(row[3]),'platform': str(row[4])}
                    
                    # Save the content of commands into a dictionary
                    dict_commands[str(row[0])] = {'commands': str(row[5]).splitlines()}


    except Exception as e:

        # Error

        # Display message
        print("[+] Error while reading csv file " + str(csv_filename) + " [ " + COLOR_FAIL + "FAIL" + COLOR_ENDC + " ]\n" + str(e))

        # Exit program
        sys.exit(1)
        
    # Display message
    print("[+] csv file read. [ " + COLOR_OK + "OK" + COLOR_ENDC + " ]")
    
    # Return a dictionary with the devices and a dictionary with the commands
    return (dict_devices, dict_commands)



# nornir group of tasks function
def nornir_group_of_tasks(task, dict_of_commands):
    
    # Global variable used to not print the name of the device by 2 tasks at the same time
    global lock
    

    try:

        # Get list of commands for the current device
        list_of_commands = dict_of_commands[str(task.host)]['commands']

        # Run each command on a device one by one
        for cmd in list_of_commands:
            task.run(task=netmiko_send_command,command_string=cmd, name=cmd)

        # Message to display
        msg =  COLOR_ENDC + "{:<32}{:^8}".format(str(task.host)[:32],"[ " + COLOR_OK + "OK" + COLOR_ENDC + " ]")

    except Exception:

        # Message to display
        msg =  COLOR_ENDC + "{:<32}{:^8}".format(str(task.host)[:32],"[ " + COLOR_FAIL + "FAIL" + COLOR_ENDC + " ]")


    # Lock the output print for this task; other tasks must wait before printing output
    with lock:

        # Display message
        print(msg)
    

# Main function
def main(dict_of_devices, dict_of_commands, csv_output = "", quiet_mode = 0):

    # Device parameters
    #h = {'my_device': {'hostname': '192.168.0.1','port': 22,'username': 'cisco','password': 'cisco','platform': 'cisco_ios'}}
    h = dict_of_devices
    g = {}
    d = {}


    # Initialization of the Nornir object
    nr = InitNornir(inventory={"plugin": "nornir.plugins.inventory.simple.SimpleInventory","options": {"hosts": h, "groups": g, "defaults": d}},logging={"enabled": False})

    # Display message
    print("[+] Running commands on devices...") 

    # Runnning the commands with nornir
    result = nr.run(task=nornir_group_of_tasks, dict_of_commands=dict_of_commands)

    # Get the name of commands for the csc header
    list_csv_header_command = get_csv_header_command(result)
    
    # Display message
    if quiet_mode == 0:
        print("[+] Results of the commands on devices:") 
    
    # Definition of a list storing the content of the results (used for the csv output file)
    list_csv_output = []

    # Display the results
    for device in result:

        # Display device name
        if quiet_mode == 0:
            print(COLOR_BLUE + device + " " + '*' * (79 - len(device)) + COLOR_ENDC)

        # Save device name into a dictionary (later saved into the list of results)
        dict_line = {"Device": device}

        index = 0

        # Get each command the appropriated result in a loop
        for data in result[device][1:]:

            # Get command name
            cmd = data.name

            # Get command result
            res = data.result

            # Display the command
            if quiet_mode == 0:
                print(COLOR_PINK + "--- " + str(cmd) + COLOR_ENDC)

            # Display the result of that command
            if quiet_mode == 0:
                print(str(res))

            # Saving the command and its result into a dictionary
            #dict_line[cmd] = str(res)
            x = list_csv_header_command[index]

            #print(x)
            dict_line[x] = str(res)

            # Next index for the csv header element
            index += 1

        # Saving the current row into the list of results
        list_csv_output.append(dict_line)

    # Results to save into a csv file?
    if csv_output:
        
        # Yes

        # Display message
        print("[+] Saving results into csv file (" + str(csv_output) + ")...")
    
        try:

            # Creation of the results csv file
            with open(csv_output, 'w', newline='') as csvfile:
                
                # Defining the header
                fieldnames = ["Device"]# + list_of_commands

                for i in list_csv_header_command:
                    fieldnames.append(i)

                # csv file object
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Saving the headinr into the csv file
                writer.writeheader()

                # Saving result sinto the csv file
                #writer.writerow({"Device": "RIEN"})
                for row in list_csv_output:
                    writer.writerow(row)

        except Exception as e:

            # Error

            # Display message
            print("[+] Error while writting csv file " + str(csv_output) + " [ " + COLOR_FAIL + "FAIL" + COLOR_ENDC + " ]\n" + str(e))

            # Exit program
            sys.exit(1)

        # Display message
        print("[+] csv file writting successfully. [ " + COLOR_OK + "OK" + COLOR_ENDC + " ]") 





# Main function call
if __name__ == '__main__':

    # No csv output file by default
    csv_output = ""

    # No quiet mode by default
    quiet_mode = 0

    # Optional argument in command line ?
    if (len(sys.argv) > 1):
    
        # Yes

        # Command-line parameters

        # Next parameter is not the output filenane
        next_param = 0

        # Read parameters
        for arg in sys.argv[1:]:

            if arg.lower() == "-g":

                # Generate csv file and txt file

                # Generating csv file

                # Display message
                print("[+] Generating \"" + csv_file + "\" file....")

                try:

                    # Create the csv file with a content
                    with open(csv_file, "w") as file:
                        file.write("hostname,ip,login,password,platform,commands\nSwitch01,192.168.0.1,cisco,cisco,cisco_ios,show arp")

                except Exception as e:

                    # Error

                    # Display message
                    print("[+] Error while creating csv file \"" + str(csv_file) + "\" [ " + COLOR_FAIL + "FAIL" + COLOR_ENDC + " ]\n" + str(e))

                    # Exit program
                    sys.exit(1)     

                # Display message
                print("[+] \"" + str(csv_file) + "\" file created successfully. [ " + COLOR_OK + "OK" + COLOR_ENDC + " ]") 

                # Exit program
                sys.exit(0)


        
            elif arg.lower() == "-h":

                # Command-line help

                # Display message
                print("Usage: dandy [-g] [-h] [-q] [-v] [-w [output]]\n")
                print("Options: ")
                print("  -g\t\tGenerate \"" + csv_file + "\" file. Warning: overwrite existing file")
                print("  -h\t\tHelp")
                print("  -q\t\tQuiet mode. Results are not displayed")
                print("  -v\t\tVersion")
                print("  -w [output]\tWrite csv output file. \"output\" is the name of the file and is optional. Default filename: \"" + default_output_csv_file + "\"")

                # Exit program
                sys.exit(0)

            elif arg.lower() == "-v":

                # Command-line version

                # Display version
                print("dandy " + VERSION)

                # Exit program
                sys.exit(0)

            elif arg.lower() == "-q":

                # Quiet mode: no result printed out on screen

                # Quiet mode enabled
                quiet_mode = 1
            
            elif next_param !=0:

                # A second parameter is expected

                # Expecting the output filename
                if next_param == 1:

                    # Yes
                    
                    # So the current parameter is the output filename
                    csv_output = str(arg)

            if arg.lower() == "-w":

                # csv output file to be used

                # Next parameter can be the output filename
                next_param = 1

                # Results will be stored into a csv file
                csv_output = default_output_csv_file
             
            else:

                # No other parameter expected
                next_param = 0



    # Get path of the script
    script_path = sys.path[0]

    # Path of the csv file in the same directory as the script
    csv_full_path = os.path.join(script_path, csv_file)

    # Read csv file
    dict_of_devices, dict_of_commands = read_csv(csv_full_path, csv_file)

    # Run main function
    main(dict_of_devices, dict_of_commands, csv_output, quiet_mode)